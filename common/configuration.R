require(rjson, quietly=T)
configuration = fromJSON(paste(readLines(args[1]), collapse=""))

conf <- function(key) {
  dollarkey = gsub("\\.","$", key)
  v = eval(parse(text=paste("configuration$",dollarkey,sep="")))
  if (is.null(v)) {
    stop(paste("Missing parameter ", key))
  } else {
    return(v)
  }
}
