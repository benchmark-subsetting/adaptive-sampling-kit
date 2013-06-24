#!/usr/bin/env python3
# Copyright (c) 2011-2013, Universite de Versailles St-Quentin-en-Yvelines
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

# Fix links for google wiki format

import re
import sys


data = open(sys.argv[1]).readlines()

i = 0
while i<len(data):
    l = data[i]
    if "http://#" in l:
        l = l.replace("http://#","#")

    if "http://Application_Characterization:_ASK:_" in l:
        l = l.replace("http://Application_Characterization:_ASK:_","")
        while 1:
            m = re.search("Chapter_[0-9]+:_\S+", l)
            if not m: break
            ori = m.group(0)
            new = ori.replace(":","")
            # replace _ only before the #
            par = new.partition('#')
            new = par[0].replace("_","") + "".join(par[1:])
            l = l.replace(ori, new)
    data[i] = l
    i+=1

with open(sys.argv[2],'w') as f:
    for l in data:
        f.write(l)
