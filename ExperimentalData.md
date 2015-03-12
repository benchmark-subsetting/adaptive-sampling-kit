# Experimental Data #

The experimental data used in the paper _ASK: Adaptive Sampling Kit for Performance Characterization_ by Pablo de Oliveira Castro, Eric Petit, Jean Christophe Beyler, and William Jalby is available [here](http://adaptive-sampling-kit.googlecode.com/files/ask-experiments.tar.bz2).

## Unpacking the Archive ##

The archive can be unpacked by typing:

```
$ tar xjvf ask-experiments.tar.bz2
```

## Content of the Archive ##

The experimental data archive contents the following directories

  * `aiaik/`, this directory contains the experimental data for the ai`_`aik experiment
    * `aggregated-timeseries`: error time series files. The median among the nine ASK runs was taken.
    * `configurations`: ASK configuration files used to run the experiments
    * `runs`: nine ASK runs with amart, hvs, hvsrelative, latinsquare, random, and tgp strategies
    * `stride.data`: exhaustive measures of the ai`_`aik kernel
  * `stencil-codes/`, this directory contains the experimental data for the stencil codes experiment
    * `aggregated-timeseries`: error time series files for the 32-core experiment. The median among the nine ASK runs was taken.
    * `bench`: source code of the stencil benchmark
    * `configurations`: ASK configuration files used to run the experiments
    * `runs`: nine ASK runs with amart, hvs, hvsrelative, latinsquare, random, and tgp strategies on the 32-core benchmark
    * `test-set-32.data`: 25600 samples test set used to measure the error on the 32-core benchmark

## Reproducing the Experiments ##

### Ai`_`Aik ###

Because the ai`_`aik’s design space was exhaustively measured, it is easy to reproduce the experiment. First, change the path to the `aiaik/` directory:

```
$ cd aiaik/
```

Create a new directory for your experiments:

```
$ mkdir myexperiments/; cd myexperiments/
```

To run the sampling strategies configurations in `aiaik/configurations/`, run:

```
$ for conf in ../configurations/*.conf; do ask $conf; done
```

Alternatively, it is possible to replay the exact experiments used in the paper. Replaying means that ASK will reuse the samples from a previous run but will regenerate the error and plot reports. To replay the paper experiments: Copy the exhaustive data inside aiaik/runs/ directory :

```
$ cd aiaik/runs/
$ cp ../stride.data .
```

Select the run to replay, for instance `run-1`, and move into its directory:

```
$ cd run-1/
```

Select the configuration to replay, for instance `hvs.conf`, then run:

```
$ ask --replay_only ../../configurations/hvs.conf
```

### Stencil Codes ###

The stencil codes’ design space was too large to be exhaustively sampled; therefore, to reproduce the experiment the samples must be measured using the stencil benchmark available in `stencil-codes/bench`. The benchmark is a simple C program that can be compiled using the included `Makefile`:

```
$ cd stencil-codes/bench
$ make
```

Then, create a new directory for your experiments inside `stencil-codes/`:

```
$ mkdir myexperiment; cd myexperiment
```

To run the sampling strategies configurations in `stencil-codes/configurations/`, run:

```
$ for conf in ../configurations/*.conf; do ask $conf; done
```

This simple setup runs ASK and the stencil bench on the same computer and is not recommended. It is better to run the stencil bench on a remote computer in a isolated environment to get accurate measures. The paper’s data was measured on a controlled and isolated environment. Details to reproduce our setup are available on request: ask-team@exascale-computing.eu.

Alternatively, it is possible to replay the exact experiments used in the paper. Replaying means that ASK will reuse the samples from a previous run but will regenerate the error and plot reports. To replay the paper experiments, copy the test set data inside aiaik/runs/ directory :

```
$ cd stencil-codes/runs/
$ cp ../test-set-32.data .
```

Select the run to replay, for instance run-1, and move into its directory:

```
$ cd run-1/
```

Select the configuration to replay, for instance hvs.conf, then run:

```
$ ask --replay_only ../../configurations/hvs.conf
```