# Installation and First Use #

## Introduction ##

The following chapter presents how to download and configure ASK on the user’s workstation.

## Download ##

Download ASK through the Git version control system:

```bash

$ git clone https://code.google.com/p/adaptive-sampling-kit/
```

The previous command retrieves the current stable version of ASK. To switch to the development version type:

```bash

$ cd ask
$ git checkout develop
```

## Configuration ##

Before using ASK, make sure all its dependencies are satisfied:

  * Python: at least version 2.6
  * R
  * Libraries: python-numpy, python-scipy and python-argparse
  * Optionally, nosetests, which is only needed to [run the regression test suite](Chapter6Support#Running_the_Test_Suite.md)

In a Debian or Ubuntu system, use:

```bash

$ sudo apt-get install python2.6 r-base python-numpy python-scipy \
python-argparse python-nose
```

Ensure that R`_`LIBS contains a writable directory. For example, add the following line to your `.bashrc`, or equivalent, file:

```bash

export R_LIBS=$HOME/.R-libs:$R_LIBS
```

and create the directory with:

```bash

$ mkdir $HOME/.R-libs/
```

Once the dependencies are installed and R`_`LIBS configured, enter ASK’s directory and execute the `configure` script.

```bash

$./configure
Checking if R is installed
Checking if python is installed
All the dependencies are satisfied.
Building uniform sampling dynamic library (only needed for amart sampler module)
```

The configure script makes sure all previous dependencies are properly installed. It also retrieves a set of R modules from [rcran](http://cran.r-project.org/). Therefore, before running this script, make sure the computer is connected to the internet.

ASK installation is self-contained: it does not install system-wide files. The `ask` binary can be run directly, or added to the PATH environment variable, eg. in bash:

```bash

cd ask/
export PATH=$PWD:$PATH
```

The ASK directory contains the following subdirectories:

  * `common/`, contains common libraries
  * `examples/`, contains runable examples of ASK’s usage
  * `tests/`, contains the [test regression suite](Chapter6Support#Running_the_Test_Suite.md)
  * `bootstrap/`, contains the standard [Bootstrap modules](Chapter4StandardModules#Bootstrap_Modules.md)
  * `control/`, contains the standard [Control modules](Chapter4StandardModules#Control_Modules.md)
  * `model/`, contains the standard [Model modules](Chapter4StandardModules#Model_Modules.md)
  * `reporter/`, contains the standard [Reporter modules](Chapter4StandardModules#Reporter_Modules.md)
  * `sampler/`, contains the standard [Sampler modules](Chapter4StandardModules#Sampler_Modules.md)
  * `source/`, contains the standard [Source modules](Chapter4StandardModules#Source_Modules.md)
  * `utils/`, contains two scripts handling time series, described in [Chapter 3](Chapter3ExperimentSetup#Analyzing_the_experiment.md)

## First Use ##

Go into ASK’s directory and type `ask -h` to get a brief summary of the command-line options. [Chapter 3](Chapter3ExperimentSetup#ASK_invocation.md) explains in detail ASK’s invocation.

Now, consider the `simple` experiment from the `examples` directory.

```bash

$ cd ask/; export PATH=$PWD:$PATH
$ cd examples/simple
$ ls
gauss2D.data simple.conf
```

Observe there are two files:

  * `Gauss2D.data` contains some measures:

```rconsole

-200 -200 -0.000670925255805024
-199 -200 -0.000694745225748637
-198 -200 -0.000719248849372865
-197 -200 -0.00074444881633483
-196 -200 -0.00077035776068282
-195 -200 -0.0007969882457312
-194 -200 -0.000824352748414127
-193 -200 -0.00085246364311948
-192 -200 -0.000881333185005384
-191 -200 -0.000910973492802606
...
```

The last column represents the response; the first two columns are factors.

The above file contains an exhaustive measure of a design space inspired by an example from the article, _tgp: An R package for Bayesian nonstationary, semiparametric nonlinear regression and design by treed gaussian process models._, R. B. Gramacy, Journal of Statistical Software 2007:

$$f(x`_`1,x`_`2) = frac{x`_`1}{100}.e<sup>{-(frac{x`_`1}{100})</sup>2-(frac{x`_`2}{100})^2} textrm{ on } `[`-200:600`]` times `[`-200:600`]`$$

The design space has two factors, named x1 and x2 in the formula, and the response f(x1,x2).

  * `Simple.conf` contains the configuration of the experiment

The configuration file’s first section, named factors, describes the factors of the experiment:

```js

"factors": [
{"name": "x",
"type": "integer",
"range": {"min": -200, "max": 600}
},
{"name": "y",
"type": "integer",
"range": {"min": -200, "max": 600}
}
]
```

In the experiment, there are two factors called **x** and **y**, both of type **integer** and varying between -200 and 600, bounds included.

The second section, Modules, configures the ask modules involved in this experiment. The bootstrap module samples five hundred points random points, a general boosting machine (gbm) model is built and the 2D reporter plots the result. For a full discussion of module parameters please refer to [Chapter 3](Chapter3GeneralUsage.md).

To run the experiments, type:

```bash

$ ask simple.conf
Logging to default.log
Experiments finished normally
```

The ask driver runs approximately for one minute and reports that the experiment finished without errors. While it is running, the `default.log` file tracks the driver’s progress, the default.log file is created by default in the directory where ASK is invoked. ASK saves all the results into the default output directory `output/`:

```bash

$ ls output/
labelled00000.data  labelled.data  model00000.data  plot00000.png
prediction00000.data
```

Open the `plot00000.png` file in an image viewer, observe it shows two level plots:

  * The top one, shows the absolute error between the response model and the true response: white is better
  * The bottom one, shows the response model built using five hundred samples
  * The samples themselves are marked by the tiny circles

![http://wiki.adaptive-sampling-kit.googlecode.com/git/figures/ASK-first-plot.png](http://wiki.adaptive-sampling-kit.googlecode.com/git/figures/ASK-first-plot.png)