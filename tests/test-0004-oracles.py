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


class AmartTests(CommandLineT):
    def test_basic_amart(self):
        """ Test amart with ask """
        self.conf({
            "output_directory": "outdir",

            "factors": [
            {"name": "k",
             "type": "integer",
             "range": {"min": 1, "max": 8}},
            {"name": "n",
             "type": "integer",
             "range": {"min": 5, "max": 4999}}],

            "modules": {
            "sampler": {
            "executable": "sampler/amart",
            "params": {"n": 50, "seeds": 3, "trees": 10}},

            "control": {
            "executable": "control/points",
            "params": {"n": 150}},

            "bootstrap": {
            "executable": "bootstrap/random-file",
            "params": {"data_file": self.tfile("test1.data"), "n": 50}},

            "source": {
            "executable": "source/file",
            "params": {"data_file": self.tfile("test1.data")}}}})

        r = self.run("ask test.conf")
        assert "outdir/labelled.data" in r.files_created,\
               "labelled.data is created"
        lines = r.files_created["outdir/labelled.data"].bytes.split("\n")
        card = len([l for l in lines if l])
        assert card == 150, "150 samples should have been obtained"


class HierarchicalTests(CommandLineT):
    def test_basic_hierarchical(self):
        """ Test hierarchical with ask """
        self.conf({
            "output_directory": "outdir",
            "factors": [
            {"name": "k",
             "type": "integer",
             "range": {"min": 1, "max": 8}},
            {"name": "n",
             "type": "integer",
             "range": {"min": 5, "max": 4999}}],

            "modules": {
            "sampler": {
            "executable": "sampler/hierarchical",
            "params": {"n": 50, "cp": 0.01}},

            "control": {
            "executable": "control/points",
            "params": {"n": 150}},

            "bootstrap": {
            "executable": "bootstrap/random-file",
            "params": {"data_file": self.tfile("test1.data"), "n": 50}},

            "source": {
            "executable": "source/file",
            "params": {"data_file": self.tfile("test1.data")}}}})

        r = self.run("ask test.conf")
        assert "outdir/labelled.data" in r.files_created,\
                 "labelled.data is created"
        lines = r.files_created["outdir/labelled.data"].bytes.split("\n")
        card = len([l for l in lines if l])
        assert card == 150, "150 samples should have beed obtained"
