from random import randrange
import os


from kubernetes import client, config
from kubernetes.client import V1PodList, CoreV1Api, AppsV1Api
from kubernetes.config.config_exception import ConfigException


def create_deployment_object(
    job_name,
    container_image,
    container_port,
    image_pull_policy,
    namespace,
    requests={"cpu": 2, "memory": 100},
    limits={"cpu": 2, "memory": 100},
):
    """Creates a deployment object for a specific job and container image"""
    resources = client.V1ResourceRequirements(requests=requests, limits=limits)

    container = client.V1Container(
        name=job_name,
        image=container_image,
        # ports=[client.V1ContainerPort(container_port=container_port)],
        resources=resources,
        image_pull_policy=image_pull_policy,
    )

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"model": job_name}),
        spec=client.V1PodSpec(containers=[container]),
    )

    spec = client.V1DeploymentSpec(
        template=template, selector={"matchLabels": {"model": job_name}}
    )

    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(
            name=job_name, labels={"model": job_name}, namespace=namespace
        ),
        spec=spec,
    )
    return deployment


if __name__ == "__main__":
    config.load_config()
    dep = create_deployment_object(
        "ben-test",
        "nginx:latest",
        80,
        "",
        "default",
    )
    # print(dep)
    k8s_apps_v1 = client.AppsV1Api()
    resp = k8s_apps_v1.create_namespaced_deployment(body=dep, namespace="default")
# resp = k8s_apps_v1.create_namespaced_deployment(
#            body=dep, namespace="default")
