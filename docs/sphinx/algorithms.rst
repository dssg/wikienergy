Algorithms
==========

The following algorithm modules work modules with the particular data types
defined in the ``appliance`` module to perform particular disaggregation tasks
such as:

1. Appliance detection
2. Appliance modeling and signal generation
3. Appliance disaggregation

Factorial Hidden Markov Models
------------------------------

The ``fhmm`` module contains methods for using Hidden Markov Models (HMM) and
Factorial Hidden Markov Models (FHMM) for appliance type modeling and sample
generation. Given a set of appliances for a house with known parameters, FHMMs
combine a number of HMMs in parallel to model appliance states.

Methods
~~~~~~~

.. automodule:: disaggregator.fhmm
   :members:

Neural Networks
---------------

The ``nn`` module contains methods for using Neural networks for appliance
detection.

Convolutional Neural Networks capture translation invariant features.

Methods
~~~~~~~

*[Future]*

Sparse Coding
-------------

Sparse coding methods model appliances as a linear combinations of basis
functions. It is termed "sparse coding" because appliances are coded using
a sparse selection of the basis functions.

Methods
~~~~~~~

*[Future]*

Ensemble Methods
----------------

Some methods use multiple algorithms to gain better insight into particular
problems.

Methods
~~~~~~~

*[Future]*

