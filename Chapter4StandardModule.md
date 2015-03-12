# Standard Modules #

## Introduction ##

This chapter presents the options for the standard modules bundled in ASK.

## Bootstrap Modules ##

Bootstrap modules select the first batch of sampled points in the experiment.

### Module latinsquare ###

Module latinsquare selects points using a Latin Hypercube sampling. The method is described in _Large sample properties of simulations using Latin Hypercube Sampling_, M. Stein, Technometrics 1987, 143–151, JSTOR. ASK’s module uses the [R lhs package](http://cran.r-project.org/web/packages/lhs/) implementation.

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| n | yes | integer | Number of samples |
| method |  | string: “random”, “genetic” or “maximin” | Method to generate the latin hypercube, refer to [lhs documentation](http://cran.r-project.org/web/packages/lhs/) for details. “random” method is default. |
| seed |  | integer | Seed to initialize the Random Number Generator (RNG). When missing the default R RNG initialization is used. |

### Module lowdiscrepancy ###

Module lowdiscrepancy selects points using a Low Discrepancy sequence. ASK’s module uses the [R fOptions package](http://cran.r-project.org/web/packages/fOptions/) implementation.

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| n | yes | integer | Number of samples |
| method |  | string: “sobol” or “halton” | Type of low discrepancy sequence, refer to [fOptions documentation](http://cran.r-project.org/web/packages/fOptions/) for details. “sobol” method is default. |
| seed |  | integer | Seed to initialize the RNG. When missing the default R RNG initialization is used. |

### Module random ###

Module random selects points by choosing a value for each factor using a uniform random distribution.

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| n | yes | integer |  |
| seed |  | integer | Seed to initialize the RNG. When missing the default Python RNG initialization is used. |

### Module random-file ###

Module random-file selects points by choosing samples at random from a samples file. The file must be in [ASK’s data exchange format](Chapter3ExperimentSetup#Data_Exchange_Format.md).

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| n | yes | integer | Number of samples |
| data`_`file | yes | path | samples file |
| seed |  | integer | Seed to initialize the RNG. When missing the default Python RNG initialization is used. |

## Source Modules ##

Source modules measure the samples selected by a bootstrap or sampler module. Usually, the user writes a custom source module fitting the target experiment.

### Module File ###

The module file uses a text file as a database for returning measures. When the file module receives a requested set of samples, it tries to find them in the database file and returns the matching ones.

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| data`_`file | yes | path | Path of the database file containing previously measured samples in [ASK’s data exchange format](Chapter3ExperimentSetup#Data_Exchange_Format.md). |

## Sampler Modules ##

The sampler module samples additional points in each iteration of the experimental pipeline.

### Module amart ###

Module amart selects points using the method described in _Accurate and efficient processor performance prediction via regression tree based modeling_, B. Li and L. Peng and B. Ramadass, Journal of Systems Architecture 2009, 457–467.

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| n | yes | integer | Number of samples |
| trees |  | integer | Number of trees used by the underlying GBM model. Default is 3000. |
| seeds |  | integer | Size of the committee. |
| predict`_`on`_`all |  | boolean | If true, the committee votes on all the candidate points. If false, the committee votes on a subsample of 20`*`n points using a Latin Hypercube sampling. Default is true. |

### Module hierarchical ###

Module hierarchical selects points using the Hierarchical Variance Sampling method.

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| n | yes | integer | Number of samples |
| confidence |  | float | Confidence bound adjustment. A value of 0.9 means that the interval computed is valid 90% of the time. Default is 0.9. |
| use`_`cov |  | boolean | If true, the error per region is computed from the square of the coefficient of variance, also called relative variance. By default, it is false and the error is computed from the variance. |
| use`_`weights |  | boolean | If true, a weights file is produced. It can be used by other modules (such as GBM) to compensate HVS uneven sampling during model construction. By default, it is true. |
| ponderate`_`by`_`size |  | boolean | If true, the error per region is defined as the square of the coefficient of variance multiplied by the region size. By default, it is true. |

### Module tgp ###

Module tgp selects points using the [Tree Gaussian Process R package](http://cran.r-project.org/web/packages/tgp/).

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| n | yes | integer | Number of samples |

### Module latinsquare ###

Module latinsquare selects points using augmented Latin Hypercube samplings using the [lhs R package](http://cran.r-project.org/web/packages/lhs/). If latinsquare is used as sampler, then latinsquare must be used as bootstrap.

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| n | yes | integer | Number of samples |

### Module random ###

The random module selects points by choosing a value for each factor using a uniform random distribution. It also avoids selecting already sampled points. When selecting an already sampled point, it discards the point and chooses a new random combination. The module finally gives up if, after 50 tries, it is unable to find a new combination,

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| n | yes | integer | Number of samples |

## Model Modules ##

Model modules predict the response in locations not yet sampled.

### Module cart ###

Module cart uses the model described in _CART: Classification and regression trees_, L. Breiman and J. Friedman and R. Olshen and C. Stone and D. Steinberg and P. Colla, Wadsworth 1983.

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| cp | yes | float | Complexity parameter |

### Module gbm ###

Module gbm uses the model described in <a href='http://cran.r-project.org/web/packages/gbm/'><i>Generalized Boosted Models: A guide to the gbm package</i></a>, G. Ridgeway.

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| ntreees |  | integer | Number of trees, default is 3000. |
| interactiondepth |  | integer | Interaction Depth, default is 8. |
| shrinkage |  | float | Shrinkage, default is 0.01 |
| distribution |  | string: “gaussian”, “laplace”, for the full list check [gbm documentation](http://cran.r-project.org/web/packages/gbm/). | Distribution function used when building the boosted tree model. Gaussian, the default minimizes RMSE error. Laplace minimizes the mean absolute error. |

### Module tgp ###

Module tgp uses the Tree Gaussian Process model implemented in the [tgp R package](http://cran.r-project.org/web/packages/tgp/).

ASK’s interface to the tgp module is not yet configurable.

## Control Modules ##

Control modules choose when to end the experiment.

### Module points ###

Module points, stops the experiment after a fixed number of samples.

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| n | yes | integer | Number of samples. The experiment will be stopped when the number of points sampled reaches n. |

### Module convergence ###

The module converge, stops the experiment if the model does not improve significantly in a given time window. It computes the improvement on a measure of the model error. The accuracy values are read from a time series file. The timeseries file, which is briefly discussed in [Chapter 3](Chapter3ExperimentSetup#Analyzing_the_experiment.md), is composed of space separated values. The first line is a header with the name of the columns. The first column contains the number of samples, the second column contain a measure of error. The file is automatically generated by the [generic reporter](#Module_Generic.md), for example:

```bash

samples mean-error max-error rmse mean-relative max-relative
50 0.0377823384121497 0.447323111968324 0.0781095183475204 Inf Inf
100 0.0294159657374007 0.408494500075275 0.0630672408986823 Inf Inf
150 0.0275319895231202 0.281661273924844 0.0469645301362225 Inf Inf
```

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| timeseries |  | path | A file containing the model’s error timeseries. If left empty, the module tries to retrieve the timeseries file from the report module configuration. |
| window |  | int | The window in number of iterations. The default value is 5. |
| threshold |  | float | Improvement threshold. A threshold of 0.1, means that if the error rate of change in the last `window` iterations is under 1%, the experiment stops. |

## Reporter Modules ##

Reporter modules produce informative statistics for the user during the experiment.

### Module generic ###

Module points, stops the experiment after a fixed number of samples.

|  Parameters |  Mandatory |  Expects |  Description |
|:------------|:-----------|:---------|:-------------|
| test`_`set | yes | path | File containing a set of samples. The model error is measured against this test-set of samples. The file must be in [ASK’s data exchange format](#Data_Exchange_Format.md). |
| script | yes | path: “reporter/generic/1D.R” or “reporter/generic/2D.R” or user provided script | This is the path of the script used for plotting the model’s predictions. This module includes generic scripts for 1D and 2D design spaces, that is to say composed of one or two factors. For higher-dimension spaces, the user must [write a custom reporter](Chapter5WritingModules.md). |
| timeseries |  | path | Path of the time series file. Error measures of the model will be written to this file. |
| max`_`error`_`scale |  | float | If specified, it represents the error’s plot maximal error value. If left empty, the error’s plot range is dynamically adapted. |