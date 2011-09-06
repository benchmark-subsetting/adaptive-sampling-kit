import json
from util import fatal

class Configuration():
    def __init__(self,
                 user_configuration,
                 default_configuration = "default.conf"):

        # First load the default configuration
        self._conf = Configuration.load(default_configuration)

        # Now load the user configuration
        user_conf = Configuration.load(user_configuration)

        # Overwrite default configuration with user's one
        Configuration.overwrite(self._conf, user_conf)

        # Write live configuration to disk
        filename = "live_configuration.conf"
        self._conf["configuration_file"] = filename
        f = open(filename, "w")
        json.dump(self._conf, f, indent=2)
        f.write("\n")
        f.close()

    @staticmethod
    def load(filename):
        # Parse configuration
        try:
            f = open(filename, "r")
            conf = json.load(f)
            f.close()
        except ValueError, e:
            fatal("Problem parsing configuration file {0}:\n"
                  "  {1}".format(filename,e))
        except IOError:
            fatal("Could not open configuration file {0}"
                  .format(filename))
        return conf

    @staticmethod
    def overwrite(old_conf, new_conf):
        """
        Overwrite a previous configuration with a new one.  Existing
        configuration values not redefined by new_conf are preserved
        (which allows to merge different configurations together).

        The merged configuration is written to old_conf.
        """
        for key,value in new_conf.iteritems():
            if isinstance(value, dict) and key in old_conf:
                Configuration.overwrite(old_conf[key],
                                        value)
            else:
                old_conf[key] = value

    def __getitem__(self, key):
        subkeys = key.split(".")
        try:
            V = self._conf
            for sk in subkeys:
                V = V[sk]
            return V
        except KeyError:       
            fatal("Missing configuration parameter {0}"
                  .format(key))
