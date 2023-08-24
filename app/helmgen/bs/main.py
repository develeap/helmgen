from backend_service_adapter import BackendServiceAdapter

if __name__ == '__main__':
    backend = BackendServiceAdapter(config_path="~/.kube/config")
    # backend.create_deployment_object("test", "test")
    pods = backend.list_namespaced_deploys("default")
    print(pods)
