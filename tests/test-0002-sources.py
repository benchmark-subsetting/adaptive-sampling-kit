from nose.tools import * 
from test_util import CommandLineT

class BootstrapFileSource(CommandLineT):
  def test_missing_params(self):
    """ File source should print a message if parameters are missing """
    self.conf({"modules" : {
                  "source" : {"params": {}
               }}})
    r = self.run_module("source/file", "test.conf request sample", expect_error=True)
    assert r.stderr.find("data_file") != -1, "error message should mention data_file"

  def test_request(self):
    """ Source request should be fullfilled """
    card = 3
    self.conf({"modules" : {
                  "source" : {"params": {"data_file":"../test1.data"}
               }}})
    self.writefile("request", "\n".join(["5 3000", "3 2777", "8 2777"]))
    r = self.run_module("source/file", "test.conf request sample", expect_stderr=True)
    assert "sample" in r.files_created, "sample is created"
    sample = r.files_created["sample"]
    lines = [l for l in sample.bytes.split("\n") if l]
    sample_card = len(lines)
    assert sample_card == card, "we should get exactly 3 samples" 
    for l in lines:
      print l
      assert len(l.split()) == 3, "each line should have 3 elements)"

  def test_missing(self):
    """ Missing points should not be returned """
    card = 2
    self.conf({"modules" : {
                  "source" : {"params": {"data_file":"../test1.data"}
               }}})
    self.writefile("request", "\n".join(["5 3000", "3 2777", "100000000 2777"]))
    r = self.run_module("source/file", "test.conf request sample", expect_stderr=True)
    sample = r.files_created["sample"]
    lines = [l for l in sample.bytes.split("\n") if l]
    sample_card = len(lines)
    assert sample_card == card, "we should get exactly 2 samples" 
