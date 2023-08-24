import logging

class Parser:
    def __init__(self,yaml_file):
        self.yaml_file = yaml_file

    def temp_func(self):
        logging.info(f"value_file {self.yaml_file}") 
        return "temp func"

    def __str__(self):
        
        return "hello from Parser Class"
