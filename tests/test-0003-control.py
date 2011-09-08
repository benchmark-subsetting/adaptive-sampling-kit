from nose.tools import * 
from test_util import CommandLineT

class ControlTests(CommandLineT):
    def test_points_control_stop(self):
        """ If enough points reached control should stop """
        self.conf({
            "output_directory" : "outdir", 
            "modules": {
            "control": {
            "executable": "control/points",
            "params": {"points" : 150}
            }}})

        r = self.run_module("control/points", "test.conf 1 ../test1.data fakemodel", expect_error=True)
        assert r.returncode == 254, "control should stop with 254 returncode"


    def test_points_control_continue(self):
        """ If not enough points reached control should continue """ 
        self.conf({
            "output_directory" : "outdir", 
            "modules": {
            "control": {
            "executable": "control/points",
            "params": {"points" : 2**32}
            }}})

        r = self.run_module("control/points", "test.conf 1 ../test1.data fakemodel")
        assert r.returncode == 0, "control should stop with 254 returncode"
       

        
