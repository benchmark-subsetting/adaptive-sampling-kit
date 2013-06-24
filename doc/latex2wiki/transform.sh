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

# Translate the latex documentation into google wiki format

DEST="./adaptive-sampling-kit.wiki/"
BUILD="./build/"

mkdir -p $DEST
mkdir -p $BUILD

for i in *.tex; do
    echo "Processing ${i}"
    bn=$(basename $i .tex)
    cp $i $BUILD/$bn.tmp
    sed -i -e 's/{| p{0.18\\textwidth} | p{0.18\\textwidth} | p{0.14\\textwidth} | p{0.50\\textwidth}  |}/{|c|c|c|l|}/g' $BUILD/$bn.tmp
    sed -i -e 's/\\hrefinternal{http:\/\/\/wiki\/\(.*\)}/\\href{http:\/\/\1}/g' $BUILD/$bn.tmp
    pandoc --from=latex -s $BUILD/$bn.tmp -o $BUILD/$bn.md
    sed -i -e 's/~~~~ {.\(.*\)}/<pre><code language="\1">/g' $BUILD/$bn.md
    sed -i -e 's/~~~~/<\/code><\/pre>/g' $BUILD/$bn.md
    ./latex2wiki/ttab.py $BUILD/$bn.md $BUILD/$bn.gtabs.md
    markowik --mx tables --image-baseurl "http://wiki.adaptive-sampling-kit.googlecode.com/git/" $BUILD/$bn.gtabs.md $BUILD/$bn.wiki.tmp
    sed -i -e 's/<pre><code/<code/g' $BUILD/$bn.wiki.tmp
    sed -i -e 's/<\/code><\/pre>/<\/code>/g' $BUILD/$bn.wiki.tmp
    ./latex2wiki/tlin.py $BUILD/$bn.wiki.tmp $DEST/$bn.wiki
done

./latex2wiki/autotoc.sh > $DEST/Sidebar.wiki
