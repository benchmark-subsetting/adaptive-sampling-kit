#!/usr/bin/env Rscript
# Wrapper around the ci.cv.R: code from the MBESS 3.3.3 package
# at http://cran.r-project.org/web/packages/MBESS/
# Authored and Maintained by Ken Kelley and Keke Lai<LaiKeke at ASU.edu>
#
# Copyright (c) 2012 Ken Kelley and Keke Lai
#
# This file is part of MBESS.  MBESS is free software: you can redistribute
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

ci.cv <- function (cv = NULL, mean = NULL, sd = NULL, n = NULL, data = NULL,
          conf.level = 0.95, alpha.lower = NULL, alpha.upper = NULL,
          ...)
{
  if (is.null(conf.level)) {
    if (alpha.lower >= 1 | alpha.lower < 0)
      stop("'alpha.lower' is not correctly specified.")
    if (alpha.upper >= 1 | alpha.upper < 0)
      stop("'alpha.upper' is not correctly specified.")
  }
  if (!is.null(conf.level)) {
    if (!is.null(alpha.lower) | !is.null(alpha.upper))
      stop("Since 'conf.level' is specified, 'alpha.lower' and 'alpha.upper' should be 'NULL'.")
    alpha.lower <- (1 - conf.level)/2
    alpha.upper <- (1 - conf.level)/2
  }
  if (is.null(data) & is.null(cv)) {
    if (is.null(mean))
      stop("Either input the whole data set using 'data' or specify the sample mean.")
    if (mean <= 0)
      stop("The sample mean must be some non-zero positive value (Does taking the absolute value of the mean make sense?).")
    if (is.null(sd))
      stop("Either input the whole data set using 'data' or specify the sample standard deviation (using 'n'-1 in the denominator).")
    if (is.null(n))
      stop("Either input the whole data set using 'data' or specify the sample size")
    k <- sd/mean
    ncp.estimate <- sqrt(n)/k
    CI.NCP <- conf.limits.nct(ncp = ncp.estimate, df = n -
      1, alpha.lower = alpha.upper, alpha.upper = alpha.lower,
                              conf.level = NULL)
    Low.lim <- CI.NCP$Upper.Limit
    Up.lim <- CI.NCP$Lower.Limit
    Low.Lim <- sqrt(n)/Low.lim
    Up.Lim <- sqrt(n)/Up.lim
    if (Up.lim <= 0)
      Up.Lim <- Inf
    Result <- list(Lower.Limit.CofV = Low.Lim, Prob.Less.Lower = alpha.lower,
                   Upper.Limit.CofV = Up.Lim, Prob.Greater.Upper = alpha.upper,
                   C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (alpha.lower == 0)
      Result <- list(Lower.Limit.CofV = -Inf, Prob.Less.Lower = 0,
                     Upper.Limit.CofV = Up.Lim, Prob.Greater.Upper = alpha.upper,
                     C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (alpha.upper == 0)
      Result <- list(Lower.Limit.CofV = Low.Lim, Prob.Less.Lower = alpha.lower,
                     Upper.Limit.CofV = Inf, Prob.Greater.Upper = 0,
                     C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (Up.Lim == Inf)
      Result[4] <- 0
    if (round((Result$Prob.Less.Lower + Result$Prob.Greater.Upper),
ci.cv <- function (cv = NULL, mean = NULL, sd = NULL, n = NULL, data = NULL,
          conf.level = 0.95, alpha.lower = NULL, alpha.upper = NULL,
          ...)
{
  if (is.null(conf.level)) {
    if (alpha.lower >= 1 | alpha.lower < 0)
      stop("'alpha.lower' is not correctly specified.")
    if (alpha.upper >= 1 | alpha.upper < 0)
      stop("'alpha.upper' is not correctly specified.")
  }
  if (!is.null(conf.level)) {
    if (!is.null(alpha.lower) | !is.null(alpha.upper))
      stop("Since 'conf.level' is specified, 'alpha.lower' and 'alpha.upper' should be 'NULL'.")
    alpha.lower <- (1 - conf.level)/2
    alpha.upper <- (1 - conf.level)/2
  }
  if (is.null(data) & is.null(cv)) {
    if (is.null(mean))
      stop("Either input the whole data set using 'data' or specify the sample mean.")
    if (mean <= 0)
      stop("The sample mean must be some non-zero positive value (Does taking the absolute value of the mean make sense?).")
    if (is.null(sd))
      stop("Either input the whole data set using 'data' or specify the sample standard deviation (using 'n'-1 in the denominator).")
    if (is.null(n))
      stop("Either input the whole data set using 'data' or specify the sample size")
    k <- sd/mean
    ncp.estimate <- sqrt(n)/k
    CI.NCP <- conf.limits.nct(ncp = ncp.estimate, df = n -
      1, alpha.lower = alpha.upper, alpha.upper = alpha.lower,
                              conf.level = NULL)
    Low.lim <- CI.NCP$Upper.Limit
    Up.lim <- CI.NCP$Lower.Limit
    Low.Lim <- sqrt(n)/Low.lim
    Up.Lim <- sqrt(n)/Up.lim
    if (Up.lim <= 0)
      Up.Lim <- Inf
    Result <- list(Lower.Limit.CofV = Low.Lim, Prob.Less.Lower = alpha.lower,
                   Upper.Limit.CofV = Up.Lim, Prob.Greater.Upper = alpha.upper,
                   C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (alpha.lower == 0)
      Result <- list(Lower.Limit.CofV = -Inf, Prob.Less.Lower = 0,
                     Upper.Limit.CofV = Up.Lim, Prob.Greater.Upper = alpha.upper,
                     C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (alpha.upper == 0)
      Result <- list(Lower.Limit.CofV = Low.Lim, Prob.Less.Lower = alpha.lower,
                     Upper.Limit.CofV = Inf, Prob.Greater.Upper = 0,
                     C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (Up.Lim == Inf)
      Result[4] <- 0
    if (round((Result$Prob.Less.Lower + Result$Prob.Greater.Upper),
              3) != round((alpha.lower + alpha.upper), 3))
      warning("The computed confidence interval does not have the same coverage as the specified confidence interval.",
              call. = FALSE)
    return(Result)
  }
  if (!is.null(data) & is.null(cv)) {
    if (!is.null(mean))
      stop("Since 'data' is specified, do not specify the 'mean'.")
    if (!is.null(sd))
      stop("Since 'data' is specified, do not specify the 'sd'.")
    if (!is.null(n))
      stop("Since 'data' is specified, do not specify the 'n'.")
    n <- length(data)
    sd.data <- (var(data))^0.5
    mean.data <- mean(data)
    k <- sd.data/mean.data
    ncp.estimate <- sqrt(n)/k
    CI.NCP <- conf.limits.nct(ncp = ncp.estimate, df = n -
      1, alpha.lower = alpha.upper, alpha.upper = alpha.lower,
                              conf.level = NULL)
    Low.lim <- CI.NCP$Upper.Limit
    Up.lim <- CI.NCP$Lower.Limit
    Low.Lim <- sqrt(n)/Low.lim
    Up.Lim <- sqrt(n)/Up.lim
    if (Up.lim <= 0)
      Up.Lim <- Inf
    Result <- list(Lower.Limit.CofV = Low.Lim, Prob.Less.Lower = alpha.lower,
                   Upper.Limit.CofV = Up.Lim, Prob.Greater.Upper = alpha.upper,
                   C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (alpha.lower == 0)
      Result <- list(Lower.Limit.CofV = -Inf, Prob.Less.Lower = 0,
                     Upper.Limit.CofV = Up.Lim, Prob.Greater.Upper = alpha.upper,
                     C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (alpha.upper == 0)
      Result <- list(Lower.Limit.CofV = Low.Lim, Prob.Less.Lower = alpha.lower,
                     Upper.Limit.CofV = Inf, Prob.Greater.Upper = 0,
                     C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (Up.Lim == Inf)
      Result[4] <- 0
    if (round((Result$Prob.Less.Lower + Result$Prob.Greater.Upper),
              3) != round((alpha.lower + alpha.upper), 3))
      warning("The computed confidence interval does not have the same coverage as the specified confidence interval.",
              call. = FALSE)
    return(Result)
  }
  if (!is.null(cv)) {
    k <- cv
    if (is.null(n))
      stop("Since you specified the coefficient of variation directly ('cv'), you must specify the sample size.")
    if (!is.null(data))
      stop("Since you specified the coefficient of variation ('cv') directly, do not include the raw data.")
    if (!is.null(mean))
      stop("Since you specified the coefficient of variation ('cv') directly, do not specify the mean ('mean').")
    if (!is.null(sd))
      stop("Since you specified the coefficient of variation ('cv') directly, do not specify the standard deviation ('sd').")
    ncp.estimate <- sqrt(n)/k
    CI.NCP <- conf.limits.nct(ncp = ncp.estimate, df = n -
      1, alpha.lower = alpha.upper, alpha.upper = alpha.lower,
                              conf.level = NULL)
    Low.lim <- CI.NCP$Upper.Limit
    Up.lim <- CI.NCP$Lower.Limit
    Low.Lim <- sqrt(n)/Low.lim
    Up.Lim <- sqrt(n)/Up.lim
    if (Up.lim <= 0)
      Up.Lim <- Inf
    Result <- list(Lower.Limit.CofV = Low.Lim, Prob.Less.Lower = alpha.lower,
                   Upper.Limit.CofV = Up.Lim, Prob.Greater.Upper = alpha.upper,
                   C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (alpha.lower == 0)
      Result <- list(Lower.Limit.CofV = -Inf, Prob.Less.Lower = 0,
                     Upper.Limit.CofV = Up.Lim, Prob.Greater.Upper = alpha.upper,
                     C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (alpha.upper == 0)
      Result <- list(Lower.Limit.CofV = Low.Lim, Prob.Less.Lower = alpha.lower,
                     Upper.Limit.CofV = Inf, Prob.Greater.Upper = 0,
                     C.of.V = k, C.of.V.Unbiased=k*(1+1/(4*n)))
    if (Up.Lim == Inf)
      Result[4] <- 0
    if (round((Result$Prob.Less.Lower + Result$Prob.Greater.Upper),
              3) != round((alpha.lower + alpha.upper), 3))
      warning("The computed confidence interval does not have the same coverage as the specified confidence interval.",
              call. = FALSE)
    return(Result)
  }
}

# This module computes the coefficient of variation upper bound
# Parse the arguments
args <- commandArgs(trailingOnly = T)
if (length(args) != 4) {
    stop("Usage: coef-variation mean sd sample-size alpha")
}

i_mean=as.real(args[1])
i_sd=as.real(args[2])
i_n=as.integer(args[3])
i_alpha=as.real(args[4])

print(ci.cv(mean=i_mean,sd=i_sd,n=i_n,conf.level=i_alpha)$Upper.Limit.CofV)


