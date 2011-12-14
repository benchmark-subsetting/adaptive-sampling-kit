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
