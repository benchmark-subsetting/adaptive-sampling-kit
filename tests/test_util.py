# Copyright (c) 2011-2012, Universite de Versailles St-Quentin-en-Yvelines
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
        os.environ["PATH"] = self.ask_path + ":" + os.environ["PATH"]

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
        """ Run an ask modules by itself """
        m = os.path.join(self.ask_path, module)
        print m
        return self.run(m + " " + args, **kwargs)

    def tfile(self, name):
        """ Shortcut to refer to test files """
        return os.path.join(self.test_path, name)

    def conf(self, data, file_name="test.conf"):
        """ Shortcut to write custom test configurations """
        self.writefile(file_name,
                       json.dumps(data)+"\n")
