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

# Fix tables in google wiki format

import re
import sys


data = open(sys.argv[1]).readlines()

def reformat_table(data, start, end, cols):
    for i in range(start,end):
        d = list(data[i])
        for p in cols:
            d[p] = '|'
        d = "".join(d)
        data[i] = d[2:]

i = 0
while i<len(data):
    l = data[i]
    if re.match("(--+\ +)+", l.strip()):
        leading_blank = len(l)-len(l.lstrip())
        cols = [match.start() for match in re.finditer(" ", l)]
        cols = list(filter(lambda x: x > leading_blank, cols))
        start_table = i-1

        #find end of table
        while i<len(data) and data[i].strip() != "":
            i+=1

        end_table = i

        reformat_table(data, start_table, end_table, cols)

    i+=1

with open(sys.argv[2],'w') as f:
    for l in data:
        f.write(l)
