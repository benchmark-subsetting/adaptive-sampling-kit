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

from test_util import CommandLineT

class DriverTests(CommandLineT):
    def test_no_arguments(self):
        """ ask should complain if called without arguments """
        r = self.run("ask", expect_error=True)

        assert "usage" in r.stderr, "Usage message should be printed"
        assert r.returncode != 0, "Return code should be != 0"

    def test_no_output_rewrite(self):
        """ The output directory should not be overwriten """
        self.conf({"output_directory": "outdir",
                   "factors" : [],
                   "modules" : {
                      "bootstrap" : {"executable" : "/bin/false"},
                      "sampler" : {"executable" : "/bin/false"},
                      "source" : {"executable" : "/bin/false"},
                      "control" : {"executable" : "/bin/false"},
                   }})

        self.run("mkdir outdir")
        self.run("touch outdir/MARKER")
        r = self.run("ask test.conf", expect_error=True)
        assert r.returncode != 0, "Return code should be != 0"
        assert "outdir/MARKER" in r.files_after, "outdir should not be overwritten"

    def test_output_rewrite(self):
        """ The output directory should be overwriten when
            passing the --force_overwrite flag
        """
        self.conf({"output_directory": "outdir",
                   "factors" : [],
                   "modules" : {
                      "bootstrap" : {"executable" : "/bin/false"},
                      "sampler" : {"executable" : "/bin/false"},
                      "source" : {"executable" : "/bin/false"},
                      "control" : {"executable" : "/bin/false"},
                   }})

        self.run("mkdir outdir")
        self.run("touch outdir/MARKER")
        r = self.run("ask test.conf --force_overwrite", expect_error=True)
        assert r.returncode != 0, "Return code should be != 0"
        assert "outdir/MARKER" not in r.files_after, "outdir should be overwritten"
