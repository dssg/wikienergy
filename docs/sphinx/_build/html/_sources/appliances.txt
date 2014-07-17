Appliances
==========

The ``appliance`` module contains a few classes to standardize intraction with
appliances. They fit together in the following way:

*[Flow diagram]*

Appliance Traces
----------------

An ``ApplianceTrace`` object represents a consecutive series of power
measurements. It is formed from a ``pandas.Series`` object indexed by a
``DatetimeIndex``, and a ``dict`` of metadata about the trace, such as its
source.

ApplianceTrace class
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: disaggregator.appliance.ApplianceTrace
   :members:

Appliance Instances
-------------------

An ``ApplianceInstance`` object represents an ordered set of traces from a
particular device.

ApplianceInstance class
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: disaggregator.appliance.ApplianceInstance
   :members:

Appliance Sets
--------------

An ``ApplianceSet`` represents an set of instances with aligned instances and
traces. All traces must be temporally aligned and sampled at the same rate -
this is enforced at instantiation. It is meant to represent a single metered
unit, such as a home, an apartment, or a building.

ApplianceSet class
~~~~~~~~~~~~~~~~~~

.. autoclass:: disaggregator.appliance.ApplianceSet
   :members:

Appliance Types
---------------

An ``ApplianceType`` object represents a set of appliance instances which
share particular attributes. For instance, an appliance type to model a
refrigerator may contain traces from many different particular instances of
refrigerators, potentially sampled at different times and rates.

ApplianceType class
~~~~~~~~~~~~~~~~~~~

.. autoclass:: disaggregator.appliance.ApplianceType
   :members:
