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

from test_util import CommandLineT


class ControlTests(CommandLineT):
    def test_points_control_stop(self):
        """ If enough points reached control should stop """
        self.conf({
            "output_directory": "outdir",
            "modules": {
            "control": {
            "executable": "control/points",
            "params": {"n": 150}}}})

        data = self.tfile("test1.data")
        r = self.run_module("control/points",
                            "test.conf 1 {0} fakemodel".format(data),
                            expect_error=True)
        assert r.returncode == 254, "control should stop with 254 return code"

    def test_points_control_continue(self):
        """ If not enough points reached control should continue """
        self.conf({
            "output_directory": "outdir",
            "modules": {
            "control": {
            "executable": "control/points",
            "params": {"n": 2 ** 16}}}})

        data = self.tfile("test1.data")
        r = self.run_module("control/points",
                            "test.conf 1 {0} fakemodel".format(data),
                            expect_error=True)
        assert r.returncode == 0, "control should continue with 0 return code"
