# Support #

## Issues and Features ##

Google code provides a bug tracker on project pages. Users and developers can write new issues or features, called tickets, at [ASK bug tracker](http://code.google.com/p/adaptive-sampling-kit/issues/list). To open tickets please follow the rules below.

### Program Bugs ###

The following steps should be used to open a bug ticket:

  1. Template: Choose Defect request from user or developer, accordingly.
  1. Subject: Choose an explicit title, summarizing the issue.
  1. Description: Add a brief abstract of the bug. Describe the exact steps that triggered the bug, and if possible attach the files needed to reproduce it.

### Feature Requests ###

The following steps should be used to open a feature ticket:

  1. Tracker: Choose “Review request.”
  1. Subject: Choose an explicit title, summarizing the issue.
  1. Description: Add a description of the feature.

## Contributing ##

The project is particularly interested in:

  * Patches fixing bugs or adding new features
  * Documentation fixes
  * Bug reports

For documentation fixes and bug reports, please use the [issue tracker](http://code.google.com/p/adaptive-sampling-kit/issues/list). For code contributions, contact us at **ask-team@exascale-computing.eu**.

### Running the Test Suite ###

ASK comes with an extensive suite of tests. Before submitting a patch, please make sure that all the tests pass, with the following command:

```bash

cd tests/
nosetests -v
```

If you submit a patch, including unit tests for your code is more than welcome and will make the patch review faster.