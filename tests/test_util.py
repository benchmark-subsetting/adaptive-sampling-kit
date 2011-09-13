import os
import unittest
from scripttest import TestFileEnvironment
import json


class CommandLineT(unittest.TestCase):
    def setUp(self):
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.ask_path = os.path.realpath(os.path.join(self.test_path, ".."))
        os.environ["ASKHOME"] = self.ask_path
        if "PYTHONPATH" in os.environ:
            os.environ["PYTHONPATH"] += ":" + self.ask_path
        else:
            os.environ["PYTHONPATH"] = self.ask_path
        os.environ["PATH"] += ":" + self.ask_path

        # ensure test sandbox exists
        try:
            os.makedirs("sandbox")
        except OSError as exc:
            if exc.errno == os.errno.EEXIST:
                pass
            else:
                raise

        self.E = TestFileEnvironment(os.path.join("sandbox", str(self.id())))
        self.run = self.E.run
        self.writefile = self.E.writefile
        self.clear = self.E.clear

    def run_module(self, module, args, **kwargs):
        m = os.path.join(self.ask_path, module)
        print m
        return self.run(m + " " + args, **kwargs)

    def tfile(self, name):
        return os.path.join(self.test_path, name)

    def conf(self, data, file_name="test.conf"):
        self.writefile(file_name,
                       json.dumps(data)+"\n")
