# Copyright 2011,2012 Exascale Computing Research
#
# This file is part of ASK.  ASK is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import json
import math
import os
import os.path
import shutil

from common.util import fatal

 # Modules that need to be defined for the ask to work
expected_modules = ["sampler", "reporter", "control",
                 "model", "bootstrap", "source"]


def check_executable(modulepath):
    # Find exact module path
    # try raw module path
    if not os.path.isfile(modulepath):
        # if not found look relatively to ASKHOME
        modulepath = os.path.join(os.environ["ASKHOME"], modulepath)
        if not os.path.isfile(modulepath):
            fatal("Module {0} could not be found".format(modulepath))

    # Check if the found path is executable
    if not os.access(modulepath, os.X_OK):
        fatal("Module {0} is not executable".format(modulepath))

    return modulepath


class Configuration():
    def __init__(self,
                 user_configuration,
                 reload_live_configuration=True,
                 force_overwrite=False,
                 replay_only=False):

        # If reloading a live configuration, there is
        # no need to check it for errors nor load the
        # default one.
        if reload_live_configuration:
            self._conf = Configuration.load(user_configuration)
        else:
            # First load the default configuration
            default_configuration = os.path.join(os.environ["ASKHOME"],
                                                 "default.conf")
            self._conf = Configuration.load(default_configuration)

            # Now load the user configuration
            user_conf = Configuration.load(user_configuration)

            # Overwrite default configuration with user's one
            Configuration.overwrite(self._conf, user_conf)

            # Check and eventually create the output directory
            self.check_outdir(force_overwrite, replay_only)
            # Change and check modules paths
            self.check_modules()

            # Check the factors
            self.check_factors()

            # Write live configuration to disk
            filename = os.path.join(self._conf["output_directory"],
                                    ".ask.conf")
            self._conf["configuration_file"] = filename
            f = open(filename, "w")
            json.dump(self._conf, f, indent=2)
            f.write("\n")
            f.close()

    def check_outdir(self, force_overwrite, replay_only):
        """ Ensure that the output directory can be used """

        if os.path.exists(self("output_directory")):
            if force_overwrite:
                print("Removing existing output directory {0}"
                      " since --force_overwrite was passed."
                      .format(self("output_directory")))
                shutil.rmtree(self("output_directory"))
                os.makedirs(self("output_directory"))
            elif not replay_only:
                fatal("Output directory \"{0}\" already exists."
                      " Use --force_overwrite option to discard it."
                      .format(self("output_directory")))
        elif replay_only:
                fatal("Output directory \"{0}\" does not exist."
                      " Cannot use --replay_only."
                      .format(self("output_directory")))
        else:
            os.makedirs(self("output_directory"))

    def check_factors(self):
        """ Check the factors configuration section """

        if "factors" not in self._conf:
            fatal("Configuration file is missing the factors section")
        if not isinstance(self._conf["factors"], list):
            fatal("Factors section should contain a list of factors")

        names = set()
        for f in self._conf["factors"]:
            if "name" not in f:
                fatal("Some factors are missing a name")
            if f["name"] in names:
                fatal("Two factors have the same name: {0}"
                      .format(f["name"]))
            else:
                names.add(f["name"])

            if "type" not in f:
                fatal("Factor {0} is missing a type"
                      .format(f["name"]))

            if f["type"] == "integer":
                if "range" not in f or "min" not in f["range"] \
                   or "max" not in f["range"]:
                    fatal("Factor {0} needs a valid range")

                # Check that min and max are integers and
                # that min < max
                mi = f["range"]["min"]
                ma = f["range"]["max"]
                if math.modf(mi)[0] != 0 or math.modf(ma)[0] != 0:
                    fatal("Range bounds for factor {0} should be integers"
                          .format(f["name"]))

                if mi >= ma:
                    fatal("Range of factor {0} is invalid : min >= max"
                          .format(f["name"]))

            elif f["type"] == "float":
                if "range" not in f or "min" not in f["range"] \
                   or "max" not in f["range"]:
                    fatal("Factor {0} needs a valid range")

                # Check that min < max
                if f["range"]["min"] >= f["range"]["max"]:
                    fatal("Range of factor {0} is invalid : min >= max"
                          .format(f["name"]))

            elif f["type"] == "categorical":
                if "values" not in f or not isinstance(f["values"], list):
                    fatal("Values field is missing or invalid for factor {0}"
                          .format(f["name"]))
            else:
                fatal("Unknown type {0} for factor {1})"
                      .format(f["type"], f["name"]))

    def check_modules(self):
        """ Check the modules configuration section
            and replace module relative paths with absolute ones
        """
        for module in expected_modules:
            # Check that the module executable can be found,
            # and update it with its complete path
            modulepath = self("modules.{0}.executable"
                           .format(module))
            self._conf["modules"][module]["executable"] =\
              check_executable(modulepath)

            if module == "model":
                # Model module as an optional executable, predictor
                # which we may need to check
                if "predictor" in self._conf["modules"][module]:
                    predictorpath = self._conf["modules"][module]["predictor"]
                    self._conf["modules"][module]["predictor"] =\
                      check_executable(predictorpath)

    @staticmethod
    def load(filename):
        # Parse configuration
        try:
            f = open(filename, "r")
            conf = json.load(f)
            f.close()
        except ValueError, e:
            fatal("Problem parsing configuration file {0}:\n"
                  "  {1}".format(filename, e))
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

        for key, value in new_conf.iteritems():
            if isinstance(value, dict) and key in old_conf:
                Configuration.overwrite(old_conf[key],
                                        value)
            else:
                old_conf[key] = value

    def __call__(self, key, expected_type=None, default_value=None):
        subkeys = key.split(".")
        # Check that the key exists and handle default_value
        try:
            V = self._conf
            for sk in subkeys:
                V = V[sk]
        except KeyError:
            if default_value == None:
                fatal("Missing configuration parameter {0}"
                      .format(key))
            else:
                V = default_value

        # Check the type
        if expected_type and not isinstance(V, expected_type):
            fatal("Wrong parameter {0} : expected {1} got '{2}'"
                    .format(key, expected_type.__name__, V))
        else:
            return V

    def __getitem__(self, key):
        return self._conf[key]
