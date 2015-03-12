# General Information #

## Introduction ##

ASK stands for Adaptive Sampling Kit. Its main goal is accelerating long experiments. Two kinds of variables define an experiment: a response and a set of factors. The response is characterized on the factors’ Cartesian product.

When the space is small, the response can be measured for every point in the space. When the space is large, doing an exhaustive measurement is either not possible in terms of execution time or simply not practical. ASK tries to find good approximations of the response by sampling only a small fraction of the space.

## How Does It Work? ##

ASK tries to efficiently sample the space by using _active learning_, also called _adaptive sampling_, approaches. These approaches can usually be broken into three steps:

  * First, they sample a few points in the space and evaluate the response on the space by building a model.
  * Second, they identify the regions of the space where the model is _imprecise_. The exact definition of _imprecise_ depends on each particular approach.
  * Third, they sample new points by prioritizing the exploration of the _imprecise_ regions. In other terms, they concentrate on the regions where interesting things happen.

## ASK Organization ##

ASK is organized as a toolkit, composed of different modules with well-defined roles:

  * Bootstrap modules: select an initial batch of points to measure
  * Sampler modules: use adaptive sampling techniques that find interesting points to sample
  * Model modules: model the full space response based on a set of sampled points
  * Source modules: gather data by running experiments or by reading data from a database
  * Report modules: report statistics and plots to the user

A driver, called `ask`, orchestrates the communication and set-up of all these modules.