import os
import unittest
from scripttest import TestFileEnvironment 
import json


class CommandLineT(unittest.TestCase):
  def setUp(self):
    self.test_path = os.path.dirname(os.path.realpath(__file__))
    self.driver_path = os.path.realpath(os.path.join(self.test_path,".."))
    os.environ["DRIVERPATH"] = self.driver_path 
    if "PYTHONPATH" in os.environ:
        os.environ["PYTHONPATH"] += ":" + self.driver_path 
    else:
        os.environ["PYTHONPATH"] = self.driver_path 
    os.environ["PATH"] +=  ":" + self.driver_path 
    self.E = TestFileEnvironment("test-sandbox")
    self.run = self.E.run
    self.writefile = self.E.writefile
    self.clear = self.E.clear
  
  def run_module(self, module, args, **kwargs):
    m = os.path.join(self.driver_path, module)
    print m
    return self.run(m + " " + args, **kwargs)

  def conf(self, data, file_name="test.conf"):
    self.writefile("test.conf", 
                   json.dumps(data))
