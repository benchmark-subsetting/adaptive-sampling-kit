from test_util import CommandLineT


class ExamplesTests(CommandLineT):
    def test_simple(self):
        """ Test that examples/simple"""

        # retrieve the configuration and data files
        self.run("cp {0}/examples/simple/gauss2D.data .".format(self.ask_path))
        self.run("cp {0}/examples/simple/simple.conf .".format(self.ask_path))

        r = self.run("ask simple.conf")
        assert "output/labelled.data" in r.files_created,\
               "labelled.data is created"
        assert "output/plot00000.png" in r.files_created,\
               "a plot is created"

    def test_gauss2D(self):
        """ Test that examples/gauss2D"""

        # retrieve the configuration and data files
        self.run("cp {0}/examples/gauss2D/source.R ."
                .format(self.ask_path))

        # consider only 300 points in the test set to make the test faster
        data =[]
        f = file("{0}/examples/gauss2D/test.data".format(self.ask_path))
        for l in range(300):
            data.append(f.readline())
        f.close()
        self.writefile("test.data", "".join(data))

        # change the default iterations values to make the test faster
        import json
        original_conf = json.loads(file("{0}/examples/gauss2D/experiment.conf"
                                   .format(self.ask_path)).read())
        original_conf["modules"]["control"]["params"]["n"] = 150
        self.conf(original_conf)

        r = self.run("ask test.conf")
        assert "output/labelled.data" in r.files_created,\
               "labelled.data is created"
        assert "output/plot00002.png" in r.files_created,\
               "a plot is created"






