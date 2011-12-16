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




