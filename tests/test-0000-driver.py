from nose.tools import * 
from test_util import CommandLineT

class DriverTests(CommandLineT):
  def test_no_arguments(self):
    """ measureit should complain if called without arguments """
    r = self.run("measureIt", expect_error=True)

    assert "usage" in r.stderr, "Usage message should be printed"
    assert r.returncode != 0, "Return code should be != 0" 

  def test_no_output_rewrite(self):
    """ The output directory should not be overwriten """
    self.conf({"output_directory": "outdir",
               "modules" : {
                  "bootstrap" : {"executable":"/bin/false"},
                  "oracle" : {"executable":"/bin/false"},
                  "source" : {"executable":"/bin/false"},
                  "control" : {"executable":"/bin/false"},
               }})

    r = self.run("mkdir outdir")
    r = self.run("measureIt test.conf", expect_error=True)
    assert r.returncode != 0, "Return code should be != 0"
    assert "outdir" not in r.files_updated, "outdir should not be overwritten" 
    
  def test_output_rewrite(self):
    """ The output directory should be overwriten when 
        passing the --force_overwrite flag
    """
    self.conf({"output_directory": "outdir",
               "modules" : {
                  "bootstrap" : {"executable":"/bin/false"},
                  "oracle" : {"executable":"/bin/false"},
                  "source" : {"executable":"/bin/false"},
                  "control" : {"executable":"/bin/false"},
               }})

    r = self.run("mkdir outdir")
    r = self.run("measureIt test.conf --force_overwrite", expect_error=True)
    assert r.returncode != 0, "Return code should be != 0"
    assert "outdir" in r.files_updated, "outdir should be overwritten" 
    



