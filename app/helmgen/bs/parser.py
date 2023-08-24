import logging
import yaml
from pathlib import Path

class Parser:
    def __init__(self,yaml_file):
        self.yaml_file = yaml_file

    def read_file(self) -> None: 
        logging.info(f"Parsing yaml file ==> {self.yaml_file}") 
        yaml_dict = yaml.safe_load(Path(self.yaml_file).read_text())

        print("======")
        for key in yaml_dict:
            print(f"On {key}")
            for i in yaml_dict[key]:
                if ("deployments" in key):
                    print("=======DEPLOYMENT=======")
                    print(i)
                if ("ingresses" in key):
                    print("======ingress======")
                    print(i)

        print("======")