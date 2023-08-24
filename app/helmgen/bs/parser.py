import logging
import yaml
from yaml.loader import BaseLoader
from pathlib import Path

class Parser:
    def __init__(self,yaml_file):
        self.yaml_file = yaml_file

    def read_file(self) -> None: 
        resources = []
        logging.info(f"Parsing yaml file ==> {self.yaml_file}") 
        yaml_dict = yaml.safe_load(Path(self.yaml_file).read_text())


        for key in yaml_dict:
            logging.info(f"Detected {key}")
            resources.append(key)

        return resources

    def __str__(self):
        return "hello from Parser Class"
