#!/bin/sh
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

# Automatically generate a table of contents for google wiki format

DEST="./adaptive-sampling-kit.wiki/"
IFS="
"

echo "* [main Documentation]"
echo
for i in $DEST/Chapter*.wiki $DEST/fdl.wiki $DEST/ExperimentalData.wiki; do
    chapter_link=$(basename $i .wiki)
    chapter_name=$(egrep -Z '^= (.*) =' $i | sed 's/= //g' | sed 's/ =//g')
    toc=$(egrep -Z '^== (.*) ==' $i)
    echo "* [$chapter_link $chapter_name]"
    echo
    for s in $toc; do
        section_name=$(echo $s | sed 's/== //g' | sed 's/ ==//g')
        section_link=$(echo $section_name | sed 's/ /_/g')
        url="$chapter_name#$section_link"
        echo "  * [$chapter_link#$section_link $section_name]"
        echo
    done
done
