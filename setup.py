#!/usr/bin/env python
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

import sys

# Check that all the python dependencies are satisfied

missing = []
ubuntu = []

try:
    import numpy
except ImportError:
    missing.append("numpy")
    ubuntu.append("python-numpy")

try:
    import argparse
except ImportError:
    missing.append("argparse")
    ubuntu.append("python-argparse")

try:
    import scipy
except ImportError:
    missing.append("scipy")
    ubuntu.append("python-scipy")


if missing:
    print ("Please install the following python packages: {0}"
        .format("".join(missing)))
    print ("On ubuntu you can type: sudo apt-get install {0}"
        .format(" ".join(ubuntu)))
    sys.exit(1)
