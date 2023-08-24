import requests
import logging
import time
import re
import csv
from random import randrange


class BackendServiceAdapter:
  def __init__(self, value_file):
    self.value_file = value_file

  def demo(self):
        logging.info(f"value_file {self.value_file}") 
