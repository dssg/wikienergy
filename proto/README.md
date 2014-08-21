Prototyping topics overview
===========================

This directory contains folders, organized by topic, which together represent
nearly all of the prototyping work which was done in the summer of 2014 by
the DSSG energy fellows. In its current, unfiltered form, it can be difficult
to navigate.

A curated set of iPython notebooks which cover a small percentage
of the prototyping done here is available in the
[tutorials](https://github.com/dssg/wikienergy/tree/master/docs/tutorials)
directory. These are easier to follow and are much more helpful for becoming
familiar with the various techniques and modules used here.


Topics
------
- General Disaggregation:
  - [`FHMM`](https://github.com/dssg/wikienergy/tree/master/proto/FHMM):
      Factorial HMM implementations and tests.
  - [`sparse_coding`](https://github.com/dssg/wikienergy/tree/master/proto/oakpark_to_aws)
      Sparse Coding implementation and exploration
- Appliance detection:
  - [`pylearn2`](https://github.com/dssg/wikienergy/tree/master/proto/pylearn2):
      Appliance detection (specifically electric vehicle); `pylearn2` dataset
      creation and manipulation, model loading and saving.
- Processing weather data:
  - [`weather`](https://github.com/dssg/wikienergy/tree/master/proto/weather):
      Obtaining data from wunderground API
  - [`setpoint_analysis`](https://github.com/dssg/wikienergy/tree/master/proto/setpoint_analysis):
      Loading data for determining the set point for individual homes
- Set-point analysis:
  - [`setpoint_analysis`](https://github.com/dssg/wikienergy/tree/master/proto/setpoint_analysis):
      Loading data for determining the set point for individual homes
- Data diagnostics: (see also: [deep dives](https://github.com/dssg/wikienergy/tree/master/docs/deepdives))
  - [`diagnostics`](https://github.com/dssg/wikienergy/tree/master/proto/diagnostics):
      Exploratory data analysis and visualization
  - [`explore_oakpark`](https://github.com/dssg/wikienergy/tree/master/proto/explore_oakpark):
      Exploratory data analysis, loading, and visualization
- Data format changes:
  - [`vis_data`](https://github.com/dssg/wikienergy/tree/master/proto/vis_data)
      Simple script demonstrating use of disaggregator module
  - [`createJSON`](https://github.com/dssg/wikienergy/tree/master/proto/createJSON)
      Pre-disaggregator temporary serialized JSON format
  - [`oakpark_to_aws`](https://github.com/dssg/wikienergy/tree/master/proto/oakpark_to_aws)
      Batch reformatting of Oak Park volunteer data
  - [`SQL`](https://github.com/dssg/wikienergy/tree/master/proto/SQL)
      Testing of pyscopg, sqlalchemy, pecan street connection
- Disaggregator:
  - [`dataset_adapter_notebooks`](https://github.com/dssg/wikienergy/tree/master/proto/dataset_adapter_notebooks)
      Notebooks created during testing of dataset adapter classes
  - [`vis_data`](https://github.com/dssg/wikienergy/tree/master/proto/vis_data)
      Simple script demonstrating use of disaggregator module
  - [`disaggregator_old`](https://github.com/dssg/wikienergy/tree/master/proto/disaggregator_old)
      First (discarded) draft of disaggregator module


Algorithms
----------
- Hidden Markov Models:
  - [`HMM`](https://github.com/dssg/wikienergy/tree/master/proto/HMM):
      HMM implementations and testing
  - [`FHMM`](https://github.com/dssg/wikienergy/tree/master/proto/FHMM):
      Factorial HMM implementations and tests
- Neural Networks:
  - [`pylearn2`](https://github.com/dssg/wikienergy/tree/master/proto/pylearn2):
      Appliance detection (specifically electric vehicle); `pylearn2` dataset
      creation and manipulation, model loading and saving.
  - [`NN`](https://github.com/dssg/wikienergy/tree/master/proto/NN):
      Backpropagation algorithm implementation, pybrain testing.
- Sparse Coding:
  - [`sparse_coding`](https://github.com/dssg/wikienergy/tree/master/proto/oakpark_to_aws)
      Sparse Coding implementation and exploration
- Support Vector Machines:
  - [`SVM`](https://github.com/dssg/wikienergy/tree/master/proto/SVM):
      Raw electric vehicle vs air conditioning signal separation, principle
      component analysis.
