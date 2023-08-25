import os
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException

NAMESPACE_FILE = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"


class BackendServiceAdapter:
    """Class which interacts with Kubernetes resources (Pod, Services, Deployments) through Python."""

    def __init__(self, config_path="~/.kube/config"):
        self.configuration = None  # will load defaults
        try:
            if config_path is not None:
                print(f"Trying to load K8s config from {config_path}")
                config.load_kube_config(config_file=config_path)
                # config_path = os.path.join(os.path.expanduser("~"), ".kube/config)")
            else:
                config.load_incluster_config()
        except ConfigException:
            # self.configuration = client.Configuration()
            print(
                "Failed to load K8s config from local file, trying to load from cluster"
            )
        self.core_api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()
        self.batch_api = client.BatchV1Api()
        self.networking_api = client.NetworkingV1Api()

    def plan_deployment(self, plan, apply=True):
        containers = []
        labels = {}
        for container in plan["spec"]["template"]["spec"]["containers"]:
            containers.append(
                client.V1Container(
                    name=container["name"],
                    image=container["image"],
                    # image_pull_policy="Never",
                    ports=[
                        client.V1ContainerPort(container_port=container["port"] or [])
                    ],
                )
            )
        # Template
        for label in plan["metadata"]["labels"]:
            labels.update(label)

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels=labels),
            spec=client.V1PodSpec(containers=containers),
        )
        # Spec
        spec = client.V1DeploymentSpec(
            replicas=plan["spec"]["replicas"] or 1,
            selector=client.V1LabelSelector(match_labels=labels),
            template=template,
        )
        # Deployment
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=plan["name"], labels=labels),
            spec=spec,
        )
        # Creation of the Deployment in specified namespacename
        # (Can replace "default" with a namespace you may have created)

        # print plan function
        print(deployment)
        if apply:
            self.apply_deployment(plan, deployment, namespace="default")

    def apply_deployment(self, plan, deployment, namespace="default"):
        self.apps_api.create_namespaced_deployment(namespace=namespace, body=deployment)
        self.plan_service(plan, apply=True)

    def plan_service(self, plan, apply=True):
        self.core_api = client.CoreV1Api()
        port_list = client.V1ServicePort(
            port=plan["spec"]["template"]["spec"]["container"][0],
            target_port=plan["spec"]["template"]["spec"]["container"][0],
        )

        svc = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(name=plan["name"]),
            spec=client.V1ServiceSpec(
                selector=plan["metadata"]["labels"], ports=[port_list]
            ),
        )
        # Creation of the Deployment in specified namespace
        # (Can replace "default" with a namespace you may have created)

        # print svc plan function
        print(svc)
        if apply:
            self.apply_service(svc)

    def apply_service(self, svc):
        self.core_api.create_namespaced_service(namespace="default", body=svc)

    def create_ingress_rules(self, plan):
        ingress_rules = {"http": [], "https": []}
        paths = []
        for rule in plan["rules"]:
            if rule[0] == "http":
                for path in rule[0]["paths"]:
                    new_path = client.V1HTTPIngressPath(
                        path=path["path"],
                        path_type=path["pathType"],
                        backend=client.V1IngressBackend(
                            service=client.V1IngressServiceBackend(
                                port=client.V1ServiceBackendPort(
                                    number=path["backend"]["service"]["port"],
                                ),
                                name=path["backend"]["service"]["name"],
                            )
                        ),
                    )
                    paths.append(new_path)
            ingress_rules[rule] = paths
            paths = []
        return ingress_rules

    def plan_ingress(self, plan, apply):
        rule_list = self.create_ingress_rules(plan)
        ingress = client.V1Ingress(
            api_version="networking.k8s.io/v1",
            kind="Ingress",
            metadata=client.V1ObjectMeta(
                name=plan["name"],
                # annotations={"nginx.ingress.kubernetes.io/rewrite-target": "/"},
            ),
            spec=client.V1IngressSpec(
                rules=[
                    client.V1IngressRule(
                        host=plan["host"],
                        http=client.V1HTTPIngressRuleValue(paths=rule_list["http"]),
                    )
                ]
            ),
        )
        # Creation of the Deployment in specified namespace
        # (Can replace "default" with a namespace you may have created)

        # add print ingress plan

        print(ingress)
        if apply:
            self.apply_ingress(ingress)

    def apply_ingress(self, ingress):
        self.networking_api.create_namespaced_ingress(namespace="default", body=ingress)

    def list_namespaced_pods(self, namespace) -> client.V1PodList:
        """Wrapper for CoreV1Api's list_namespaced_pod, returns the list of all pods in the namespace as V1PodList"""
        return self.core_api.list_namespaced_pod(namespace)

    def list_namespaced_deploys(self, namespace) -> client.V1PodList:
        """Wrapper for CoreV1Api's list_namespaced_pod, returns the list of all pods in the namespace as V1PodList"""
        return self.apps_api.list_namespaced_deployment(namespace)

    def demo(self):
        return self.value_file


if __name__ == "__main__":
    app = BackendServiceAdapter()
    app.create_deployment()
