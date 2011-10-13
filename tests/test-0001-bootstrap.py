from test_util import CommandLineT


class BootstrapRandomFileTests(CommandLineT):
    def test_random_missing_params(self):
        """ Random-File bootstrap should print a message if parameters are missing
        """
        self.conf({
            "factors": [
            {"name":"f1", "type":"integer", "range":{"min":1, "max":8}},
            {"name":"f2", "type":"integer", "range":{"min":5, "max":4999}}],
            "modules": {"bootstrap":
                        {"params": {"data_file": self.tfile("test1.data")}}}})

        r = self.run_module("bootstrap/random-file",
                            "test.conf sample",
                            expect_error=True)
        assert "n" in r.stderr, "error message should mention n"

    def test_wrong_parameter(self):
        """ Random-File bootstrap should fail nicely when n is not integer """
        self.conf({
             "factors": [
            {"name":"f1", "type":"integer", "range":{"min":1, "max":8}},
            {"name":"f2", "type":"integer", "range":{"min":5, "max":4999}}],
             "modules": {"bootstrap":
                         {"params": {"n": "foo", "data_file": "bar"}}}})

        r = self.run_module("bootstrap/random-file",
                            "test.conf sample",
                            expect_error=True)
        assert r.stderr.find("int") != -1,\
                 "error message should mention expected type"
        assert "n" in r.stderr, "error message should mention n"

    def test_sampling(self):
        """ Random-File bootstrap should sample points """
        card = 17
        self.conf({
             "factors": [
            {"name":"f1", "type":"integer", "range":{"min":1, "max":8}},
            {"name":"f2", "type":"integer", "range":{"min":5, "max":4999}}],
             "modules": {"bootstrap":
                         {"params": {"n": card,
                                     "data_file": self.tfile("test1.data")}}}})

        r = self.run_module("bootstrap/random-file", "test.conf sample")
        assert "sample" in r.files_created, "sample is created"
        sample = r.files_created["sample"]
        sample_card = len([l for l in sample.bytes.split("\n") if l])
        assert sample_card == card, "we should get exactly 17 samples"

    def test_too_large_sampling(self):
        """ Asking more points than available in the file should fail """
        data = self.tfile("test1.data")
        card = len(file(data).readlines()) + 1
        self.conf(
            {"modules": {"bootstrap":
                         {"params": {"n": card, "data_file": data}}}})

        r = self.run_module("bootstrap/random-file",
                            "test.conf sample",
                            expect_error=True)
        assert r.stderr.find("Not enough points") != -1,\
                 "error message should mention expected type"


class BootstrapRandomTests(CommandLineT):
    def test_random_with_types(self):
        """ Test Random bootstrap"""

        card = 25
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
            "bootstrap": {"executable": "bootstrap/random",
                          "params": {"n": 25}},
            "sampler": {"executable": "/bin/false"},
            "source": {"executable": "source/file",
                       "params": {"data_file": "test.data"}},
            "control": {"executable": "control/points",
                        "params": {"points": 0}}}})

        r = self.run("ask test.conf", expect_error=False)
        assert "outdir/requested00000.data" in r.files_created, "sample is created"
        sample = r.files_created["outdir/requested00000.data"]
        sample_card = len([l for l in sample.bytes.split("\n") if l])
        assert sample_card == card, "we should get exactly 25 samples"


class BootstrapLatinsquareTests(CommandLineT):
    def test_latinsquare_missing_params(self):
        """ Latinsquare bootstrap should print a message
        if parameters are missing
        """
        self.conf(
            {"factors": [],
            "modules": {"bootstrap":
                        {"params": {}}}})

        r = self.run_module("bootstrap/latinsquare",
                            "test.conf sample",
                            expect_error=True)
        assert "n" in r.stderr, "error message should mention n"

    def test_wrong_parameter(self):
        """ Latinsquare bootstrap should fail nicely when n is not integer """
        self.conf(
            {"factors": [],
             "modules": {"bootstrap":
                         {"params": {"n": "foo"}}}})

        r = self.run_module("bootstrap/latinsquare",
                            "test.conf sample",
                            expect_error=True)
        assert r.stderr.find("int") != -1,\
                 "error message should mention expected type"
        assert "n" in r.stderr, "error message should mention n"

    def test_sampling(self):
        """ Latinsquare bootstrap should sample points """
        card = 17
        self.run("mkdir outdir")
        self.conf(
            {"output_directory" : "outdir",
             "factors": [{"name": "f1", "type": "integer",
                          "range": {"min": -10, "max": 100}},
                         {"name": "f2", "type": "float",
                          "range": {"min": -10, "max": 100}},
                         {"name": "f3", "type": "categorical",
                          "values": ["a", "b", "c"]}],
             "modules": {"bootstrap":
                         {"params": {"n": card}}}})

        r = self.run_module("bootstrap/latinsquare", "test.conf sample")
        assert "sample" in r.files_created, "sample is created"
        sample = r.files_created["sample"]
        sample_card = len([l for l in sample.bytes.split("\n") if l])
        assert sample_card == card, "we should get exactly 17 samples"
