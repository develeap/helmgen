import logging
import yaml
from pathlib import Path
from helmgen.bs.backend_service_adapter import BackendServiceAdapter 

class Parser:
    def __init__(self,yaml_file):
        self.yaml_file = yaml_file
        self.backend = BackendServiceAdapter()
    def read_file(self) -> None: 
        logging.info(f"Parsing yaml file ==> {self.yaml_file}") 
        yaml_dict = yaml.safe_load(Path(self.yaml_file).read_text())

        print("======")
        for key in yaml_dict:
            print(f"On {key}")
            for i in yaml_dict[key]:
                if ("deployments" in key):
                    #self.backend.plan_deployment(i, True)
                    print(i)
                if ("ingresses" in key):
                    print("======ingress======")
                    print(i)
        print("======")


# if __name__ == "__main__":
#     a = Parser("./config-minimal.yml")
#     a.read_file()