DSSG Energy Disaggregation
==========================

Contents
-------------
This repository contains a set of tools for performing end-to-end
disaggregation of single-point energy signals at a low-resolution timescale of
15 - 30 minutes, including algorithms for supervised and unsupervised
decomposition of signals into component appliance-level signals.

In particular, the repository contains:

- the `disaggregator` module, a package of tools for an assortment of
  disaggregation tasks
- `proto`, a directory of ipython notebooks and scripts organized by topic.
- `tests`, a directory containing unit tests for the `disaggregator` module.
- `docs`, a directory containing documentation including sphinx autogen
  directives and instructions for contributors.

How to use the disaggregator module
-----------------------------------
***Please view documentation at /docs/sphinx/html/index.html***

Additional documentation and iPython notebook tutorials can be found in the
[docs](https://github.com/dssg/wikienergy/tree/master/docs) directory.

Background
----------

Parners
-------
- [Pecan Street/WikiEnergy](http://www.pecanstreet.org/)
- [Village of Oak Park](http://www.oak-park.us/)
- [Illinois Science & Energy Innovation Foundation | ISEIF](http://www.iseif.org/)

Team members
------------
 - Stephen Suffian
 - [Phil Ngo](http://www.philngo.me/)
 - Miguel Perez
 - Sabina Tomkins
 - Matthew Gee
 - Varun Chandola

Alternatives
------------

For a set of tools designed for evaluating and measuring
the effectiveness of new algorithms, please instead use
[nilmtk](https://github.com/nilmtk/nilmtk/) (Non-Intrusive Load
Monitoring Toolkit), which is designed with the needs of researchers in mind.

