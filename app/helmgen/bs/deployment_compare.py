import subprocess
import yaml
from termcolor import colored

def extract_remote_deployment_info(deployment_name):
    try:
        remote_deployment_output = subprocess.check_output(["kubectl", "get", "deploy", deployment_name, "-oyaml"]).decode("utf-8")
        remote_deployment_data = yaml.safe_load(remote_deployment_output)

        extracted_data = []

        for item in remote_deployment_data.get("spec", {}).get("template", {}).get("spec", {}).get("containers", []):
            extracted_data.append({
                "name": remote_deployment_data.get("metadata", {}).get("name"),
                "spec": {
                    "template": {
                        "spec": {
                            "containers": [
                                {
                                    "image": item["image"],
                                    "port": item["ports"][0]["containerPort"] if item.get("ports") else None
                                }
                            ]
                        }
                    }
                }
            })

        return extracted_data

    except subprocess.CalledProcessError as e:
        print(f"Error retrieving remote deployment: {e}")
        return None

def main():
    try:
        with open('config-minimal.yml', 'r') as config_file:
            config_data = yaml.safe_load(config_file)

        for deployment in config_data.get('deployments', []):
            deployment_name = deployment['name']

            remote_deployment_info = extract_remote_deployment_info(deployment_name)

            if not remote_deployment_info:
                print(f"Failed to retrieve remote deployment information for {deployment_name}.")
                continue

            local_deployment_data = deployment.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])

            print(f"\nDifferences for deployment: {deployment_name}\n")

            print("Local YAML:")
            local_yaml = yaml.dump(local_deployment_data, default_flow_style=False)
            print(local_yaml)

            print("---")

            print("Remote YAML:")
            remote_yaml = yaml.dump(remote_deployment_info, default_flow_style=False)
            print(remote_yaml)

            print("---")

            print("Comparison:")
            all_keys_same = True
            for local_item, remote_item in zip(local_deployment_data, remote_deployment_info[0]['spec']['template']['spec']['containers']):
                print("Local Item:")
                print(yaml.dump(local_item, default_flow_style=False))
                print("Remote Item:")
                print(yaml.dump(remote_item, default_flow_style=False))

                keys_differ = False
                for key in local_item:
                    local_value = local_item[key]
                    remote_value = remote_item.get(key)

                    if local_value != remote_value:
                        keys_differ = True
                        diff = f"---\nDifference in key '{key}':\nLocal: {local_value}\nRemote: {remote_value}\n"
                        if remote_value:
                            print(colored(diff, 'red'))
                        else:
                            print(colored(diff, 'green'))

                if not keys_differ:
                    print(colored(f"All keys are same for {deployment_name}\n", 'green'))

            print("------------------------------------------------------------------------------")

    except Exception as e:
        print("An error occurred:")
        print(e)

if __name__ == "__main__":
    main()
