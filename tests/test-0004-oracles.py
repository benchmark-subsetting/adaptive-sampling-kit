from nose.tools import * 
from test_util import CommandLineT

class AmartTests(CommandLineT):
    def test_basic_amart(self):
        """ Test amart through the driver """
        self.conf({
            "output_directory" : "outdir", 
            "factors": [
            {"name": "k",
             "type": "integer",
             "range" : {"min": 1, "max": 8}
             },
            {"name": "n",
             "type": "integer",
             "range": {"min": 5, "max": 4999}
             }
            ],
            "modules": {
            "oracle": {
            "executable":"oracle/amart",
            "params": {"n": 50, "seeds":3, "trees":10}
            },
            "control": {
            "executable": "control/points",
            "params": {"points" : 150}
            },
            "bootstrap": {
            "executable": "bootstrap/random",
            "params": {"data_file" : "../test1.data", "n":50}
            },
            "source" : {
            "executable": "source/file",
            "params": {"data_file" : "../test1.data"}    
            }}})

        r = self.run("driver test.conf")
        assert "outdir/labelled.data" in r.files_created, "labelled.data is created"
        card = len([l for l in r.files_created["outdir/labelled.data"].bytes.split("\n") if l])
        assert card == 150, "150 samples should have beed obtained"

class HierarchicalTests(CommandLineT):
    def test_basic_hierarchical(self):
        """ Test hierarchical through the driver """
        self.conf({
            "output_directory" : "outdir", 
            "factors": [
            {"name": "k",
             "type": "integer",
             "range" : {"min": 1, "max": 8}
             },
            {"name": "n",
             "type": "integer",
             "range": {"min": 5, "max": 4999}
             }
            ],
            "modules": {
            "oracle": {
            "executable":"oracle/hierarchical",
            "params": {"n": 50, "cp":0.01}
            },
            "control": {
            "executable": "control/points",
            "params": {"points" : 150}
            },
            "bootstrap": {
            "executable": "bootstrap/random",
            "params": {"data_file" : "../test1.data", "n":50}
            },
            "source" : {
            "executable": "source/file",
            "params": {"data_file" : "../test1.data"}    
            }}})

        r = self.run("driver test.conf")
        assert "outdir/labelled.data" in r.files_created, "labelled.data is created"
        card = len([l for l in r.files_created["outdir/labelled.data"].bytes.split("\n") if l])
        assert card == 150, "150 samples should have beed obtained"


        

        
