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

# Defines the conf function to help reading ASK configuration files from R
# modules.

require(RJSONIO, quietly=T)
configuration = fromJSON(paste(readLines(args[1]), collapse=""),
                         simplify=F)

conf <- function(key, default=NULL) {
  dollarkey = gsub("\\.","$", key)
  v = eval(parse(text=paste("configuration$",dollarkey,sep="")))
  if (is.null(v)) {
    if (is.null(default)) {
        stop(paste("Missing parameter ", key))
    } else {
        return(default)
    }
  } else {
    return(v)
  }
}
