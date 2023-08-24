import requests
import logging
import time
import re
import csv
from random import randrange


class BackendServiceAdapter:
  def __init__(self, cluster, value_file):
    self.cluster = cluster
    self.value_file = value_file

  def demo(self):
        return self.value_file


"""
Wrapper for Kubernetes client for communicating with Kubernetes
"""
import os

from flask import current_app
from kubernetes import client, config
from kubernetes.client import V1PodList, CoreV1Api, AppsV1Api
from kubernetes.config.config_exception import ConfigException

from CommonUtils.defs.decorators import Singleton
from server.src.config import DemystifyRunConfigs
from server.src.models_config import ModelDeploymentConfig

NAMESPACE_FILE = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"


class KubernetesApiClient():
    """ Singleton class which interacts with Kubernetes resources (Pod, Services, Deployments) through Python. """

    def __init__(self):
        self.configuration = None  # will load defaults
        try:
            if current_app.config["LOCAL_KUBE_CONFIG"] is not None:
                current_app.logger.info(f"Trying to load K8s config from {current_app.config['LOCAL_KUBE_CONFIG']}")
                config.load_kube_config(config_file=current_app.config["LOCAL_KUBE_CONFIG"])
            else:
                config.load_incluster_config()
        except ConfigException:
            if os.getenv("CONFIG", str(DemystifyRunConfigs.production.value)) == str(DemystifyRunConfigs.test.value):
                current_app.logger.info("Failed to load kubernetes config from default path, but running in test mode so no need")
                self.configuration = client.Configuration()
            else:
                current_app.logger.exception("Failed to load kubernetes config from default path")
                raise
        self._core_api_client = None
        self._core_v1_client = None

    def core_api_client(self) -> AppsV1Api:
        """ returns the AppsV1Api client (initializes it if needed) """
        if self._core_api_client is None:
            self._core_api_client = client.AppsV1Api(client.ApiClient(self.configuration))
        return self._core_api_client

    def core_v1_client(self) -> CoreV1Api:
        """ returns the CoreV1Api client (initializes it if needed) """
        if self._core_v1_client is None:
            self._core_v1_client = client.CoreV1Api(client.ApiClient(self.configuration))
        return self._core_v1_client

    def list_namespaced_pods(self, namespace) -> V1PodList:
        """ Wrapper for CoreV1Api's list_namespaced_pod, returns the list of all pods in the namespace as V1PodList """
        return self.core_v1_client.list_namespaced_pod(namespace)

    def get_namespaced_pod_by_job_name(self, namespace, job_name) -> V1PodList:
        """ Returns the list of pods in the namespace by the job name, as V1PodList """
        return self.core_v1_client.list_namespaced_pod(namespace, pretty=True, label_selector="model=" + job_name)

    def create_deployment_object(job_name, container_image):
        """ Creates a deployment object for a specific job and container image """
        current_app.logger.info(f"Deployment creation config - "
                                f"MODEL_REQUEST_CPU {ModelDeploymentConfig.MODEL_REQUEST_CPU}, "
                                f"MODEL_REQUEST_MEMORY {ModelDeploymentConfig.MODEL_REQUEST_MEMORY}, "
                                f"MODEL_LIMITS_CPU {ModelDeploymentConfig.MODEL_LIMITS_CPU}, "
                                f"MODEL_LIMITS_MEMORY {ModelDeploymentConfig.MODEL_LIMITS_MEMORY}, "
                                f"MODEL_DEPLOYMENT_NAMESPACE {ModelDeploymentConfig.MODEL_DEPLOYMENT_NAMESPACE}")
        resources = client.V1ResourceRequirements(requests={"cpu": ModelDeploymentConfig.MODEL_REQUEST_CPU,
                                                            "memory": ModelDeploymentConfig.MODEL_REQUEST_MEMORY},
                                                  limits={"cpu": ModelDeploymentConfig.MODEL_LIMITS_CPU,
                                                          "memory": ModelDeploymentConfig.MODEL_LIMITS_MEMORY})

        container = client.V1Container(name=job_name,
                                       image=container_image,
                                       ports=[client.V1ContainerPort(container_port=ModelDeploymentConfig.MODEL_CONTAINER_PORT)],
                                       resources=resources,
                                       image_pull_policy=ModelDeploymentConfig.MODEL_IMAGE_PULL_POLICY)

        template = client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(labels={"model": job_name}),
                                            spec=client.V1PodSpec(containers=[container]))

        spec = client.V1DeploymentSpec(template=template, selector={'matchLabels': {'model': job_name}})

        deployment = client.V1Deployment(api_version="apps/v1",
                                         kind="Deployment",
                                         metadata=client.V1ObjectMeta(name=job_name,
                                                                      labels={"model": job_name},
                                                                      namespace=ModelDeploymentConfig.MODEL_DEPLOYMENT_NAMESPACE),
                                         spec=spec)
        return deployment

    @staticmethod
    def create_service_object(job_name):
        """ Creates a service object for a given job name """
        spec = client.V1ServiceSpec(selector={"model": job_name},
                                    ports=[client.V1ServicePort(port=ModelDeploymentConfig.MODEL_CONTAINER_PORT,
                                                                target_port=ModelDeploymentConfig.MODEL_CONTAINER_PORT)])
        service = client.V1Service(api_version="v1",
                                   kind="Service",
                                   metadata=client.V1ObjectMeta(name=job_name, namespace=ModelDeploymentConfig.MODEL_DEPLOYMENT_NAMESPACE),
                                   spec=spec)
        return service


k8s_client = KubernetesApiClient()
