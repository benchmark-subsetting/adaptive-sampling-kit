# Copyright (c) 2011-2012, Université de Versailles St-Quentin-en-Yvelines
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


class BootstrapFileSource(CommandLineT):
    def test_missing_params(self):
        """ File source should print a message if parameters are missing """
        self.conf({"modules": {"source": {"params": {}}}})

        r = self.run_module("source/file",
                            "test.conf request sample",
                            expect_error=True)
        assert r.stderr.find("data_file") != -1,\
                 "error message should mention data_file"

    def test_request(self):
        """ Source request should be fullfilled """
        card = 3
        self.conf(
            {"modules": {"source":
                         {"params": {"data_file": self.tfile("test1.data")}}}})

        self.writefile("request", "\n".join(["5 3000", "3 2777", "8 2777"]))
        r = self.run_module("source/file",
                            "test.conf request sample",
                            expect_stderr=True)

        assert "sample" in r.files_created, "sample is created"
        sample = r.files_created["sample"]
        lines = [l for l in sample.bytes.split("\n") if l]
        sample_card = len(lines)
        assert sample_card == card, "we should get exactly 3 samples"
        for l in lines:
            print l
            assert len(l.split()) == 3, "each line should have 3 elements)"

    def test_missing(self):
        """ Missing points should not be returned """
        card = 2
        self.conf(
            {"modules": {"source":
                         {"params": {"data_file": self.tfile("test1.data")}}}})

        self.writefile("request",
                       "\n".join(["5 3000", "3 2777", "100000000 2777"]))
        r = self.run_module("source/file",
                            "test.conf request sample",
                            expect_stderr=True)
        sample = r.files_created["sample"]
        lines = [l for l in sample.bytes.split("\n") if l]
        sample_card = len(lines)
        assert sample_card == card, "we should get exactly 2 samples"
