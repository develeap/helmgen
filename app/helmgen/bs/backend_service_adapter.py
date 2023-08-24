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
