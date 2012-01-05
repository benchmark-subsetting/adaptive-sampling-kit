from test_util import CommandLineT


class FactorTests(CommandLineT):
    def test_ranges(self):
        """ Ranges should make sense """
        self.conf({"factors": [
          {"name":"f1",
           "type":"integer",
           "range":{"min":100, "max":10}}],
          "output_directory": "outdir",
          "modules": {
            "bootstrap": {"executable": "/bin/false"},
            "sampler": {"executable": "/bin/false"},
            "source": {"executable": "/bin/false"},
            "control": {"executable": "/bin/false"}}})

        r = self.run("ask test.conf", expect_error=True)
        assert r.returncode != 0, "Return code should be != 0"
        assert r.stderr.find("min") != -1,\
                 "error message should mention problem with min"

    def test_invalid_types(self):
        """  Check that unknown factor type is rejected """
        self.conf({"factors": [
          {"name":"f1",
           "type":"notvalidtype"}],
          "output_directory": "outdir",
          "modules": {
            "bootstrap": {"executable": "/bin/false"},
            "sampler": {"executable": "/bin/false"},
            "source": {"executable": "/bin/false"},
            "control": {"executable": "/bin/false"}}})

        r = self.run("ask test.conf", expect_error=True)
        assert r.returncode != 0, "Return code should be != 0"
        assert r.stderr.find("type") != -1,\
                 "error message should mention problem with type"

    def test_bad_categorical(self):
        """ Categorical factor missing values """
        self.conf({"factors": [
          {"name":"f1",
           "type":"categorical",
           "range": {"min": 0, "max": 10}}],
          "output_directory": "outdir",
          "modules": {
            "bootstrap": {"executable": "/bin/false"},
            "sampler": {"executable": "/bin/false"},
            "source": {"executable": "/bin/false"},
            "control": {"executable": "/bin/false"}}})

        r = self.run("ask test.conf", expect_error=True)
        assert r.returncode != 0, "Return code should be != 0"
        assert r.stderr.find("Values") != -1,\
                 "error message should mention problem with values"

    def test_bad_integer(self):
        """ Integer factor missing range """
        self.conf({"factors": [
          {"name":"f1",
           "type": "integer"}],
          "output_directory": "outdir",
          "modules": {
            "bootstrap": {"executable": "/bin/false"},
            "sampler": {"executable": "/bin/false"},
            "source": {"executable": "/bin/false"},
            "control": {"executable": "/bin/false"}}})

        r = self.run("ask test.conf", expect_error=True)
        assert r.returncode != 0, "Return code should be != 0"
        assert r.stderr.find("range") != -1,\
                 "error message should mention problem with range"

    def test_repeated_name(self):
        """ No repeated name in factors """
        self.conf({"factors": [
          {"name":"f1",
           "type":"integer",
           "range": {"min": 0, "max": 10}},
          {"name":"f1",
           "type":"integer",
           "range": {"min": 0, "max": 10}}],
          "output_directory": "outdir",
          "modules": {
            "bootstrap": {"executable": "/bin/false"},
            "sampler": {"executable": "/bin/false"},
            "source": {"executable": "/bin/false"},
            "control": {"executable": "/bin/false"}}})

        r = self.run("ask test.conf", expect_error=True)
        assert r.returncode != 0, "Return code should be != 0"
        assert r.stderr.find("name") != -1,\
                 "error message should mention problem with name"

    def test_types_ok(self):
        """ Check that valid factors are accepted """

        self.writefile("test.data", "0 5.5 0")

        self.conf({"factors": [
          {"name":"f1",
           "type":"integer",
           "range": {"min": 0, "max": 10}},
          {"name":"f2",
           "type":"float",
           "range": {"min": 0.5, "max": 10.33}},
          {"name":"f3",
           "type":"categorical",
           "values": ["a", "b", "foo"]}],
          "output_directory": "outdir",
          "modules": {
            "bootstrap": {"executable": "bootstrap/random-file",
                          "params": {"n": 1, "data_file": "test.data"}},
            "sampler": {"executable": "/bin/false"},
            "source": {"executable": "source/file",
                       "params": {"data_file": "test.data"}},
            "control": {"executable": "control/points",
                        "params": {"n": 0}}}})

        self.run("ask test.conf", expect_error=False)
