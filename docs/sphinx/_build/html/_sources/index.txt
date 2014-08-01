.. disaggregator documentation master file, created by
   sphinx-quickstart on Wed Jul  9 10:35:35 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Disaggregator Package
=====================

.. toctree::
   :maxdepth: 2

   dataset_adapters
   appliances
   evaluation_metrics
   utils
   algorithms
   generators
   weather

Overview
--------

Datasets might be loaded from many external sources and combined or
manipulated in a variety of ways toward the end of energy disaggregation;
therefore, we organize a general hierarchical structure around appliance traces
and other elements described below in order to serve as ground truth training
sets for algorithmic models.

The main tasks facilitated by this package are:

* Importing appliance traces
* Organizing appliance traces into appliance instances, types, and sets
* Algorithms for completing the following three tasks:

  * Determining appliance presence in new traces
  * Given appliance presence, determine on-off states for each time point
  * Given appliance states, reconstruct original signals

* Evaluating algorithmic results with a standard set of metrics

Basic usage
-----------
Basic usage of the disaggregator module during development is as follows:

.. code-block:: python

    import sys
    import os.path
    sys.path.append(os.path.join(os.pardir,os.pardir))

    import disaggregator as da

Terms
-----
We use the following terms throughout the documentation to refer to different
aspects of appliance level energy usage. In general, items in the categories
described below could be formed from sampled, generated, or disaggregated data.

appliance trace
   sequence of consecutive average power measurements (usually in 15 minute
   itervals) for a specific appliance instance for an arbitrary length of time.

   Ex) Readings from Refrigerator 003 for the day of 01/01/2014

appliance instance
   a specific device or example of an appliance model which may have any
   number of traces associated with it. Could additionally be a particular set
   of parameters for a generative model such as a HMM. Furthermore, an
   appliance instance might be an aggregated (i.e. not yet disaggregated) set
   of appliances. This is distinct from *appliance set* because its
   measured traces will not temporally overlap.

   Ex) Refrigerator 006; :math:`\lambda = (\pi,A,\mu,\sigma)`.

appliance type
   a category of appliances which share a set of meaningful features which may
   be used to distinguish it from other appliance types.

appliance set
   a set of appliance instances which form a metered unit. Appliance sets
   might also be fabricated to form ground-truth training, validation or
   testing sets for algorithmic disaggregation tasks.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

