#!/usr/bin/env python
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


if missing:
    print ("Please install the following python packages: {0}"
        .format("".join(missing)))
    print ("On ubuntu you can type: sudo apt-get install {0}"
        .format(" ".join(ubuntu)))
    sys.exit(1)
