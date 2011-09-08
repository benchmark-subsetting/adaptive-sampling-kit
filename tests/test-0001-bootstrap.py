from nose.tools import * 
from test_util import CommandLineT

class BootstrapRandomTests(CommandLineT):
  def test_random_missing_params(self):
    """ Random bootstrap should print a message if parameters are missing """
    self.conf({"modules" : {
                  "bootstrap" : {"params": {"data_file":"../test1.data"}
               }}})
    r = self.run_module("bootstrap/random", "test.conf sample", expect_error=True)
    assert "n" in r.stderr, "error message should mention n"

  def test_wrong_parameter(self):
    """ Random bootstrap should fail nicely when n is not integer """
    self.conf({"modules" : {
                  "bootstrap" : {"params": {"data_file":"../test1.data", "n":"boom"}
               }}})
    r = self.run_module("bootstrap/random", "test.conf sample", expect_error=True)
    assert r.stderr.find("int") != -1, "error message should mention expected type"
    assert "n" in r.stderr, "error message should mention n"
    
  def test_sampling(self):
    """ Random bootstrap should sample points """
    card = 17
    self.conf({"modules" : {
                  "bootstrap" : {"params": {"n":card, "data_file":"../test1.data"}
               }}})
    r = self.run_module("bootstrap/random", "test.conf sample")
    assert "sample" in r.files_created, "sample is created"
    sample = r.files_created["sample"]
    sample_card = len([l for l in sample.bytes.split("\n") if l])
    assert sample_card == card, "we should get exactly 17 samples" 

  def test_too_large_sampling(self):
    """ Asking more points than available in the file should fail """
    card = len(file("test1.data").readlines()) + 1 
    self.conf({"modules" : {
                  "bootstrap" : {"params": {"n":card, "data_file":"../test1.data"}
               }}})
    r = self.run_module("bootstrap/random", "test.conf sample", expect_error=True)
    assert r.stderr.find("Not enough points") != -1, "error message should mention expected type"

