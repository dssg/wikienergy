Disaggregator Documentation
===========================

Basic usage
-----------
Basic usage of the disaggregator module during development is as follows:

    import sys
    sys.path.append('../../') # or non-Unix equivalent (add wikienergy/ to path)

    import disaggregator

Disaggregator Module
--------------------
The disaggregator module is structured around appliances. We use the
following terms through the documentation:

### Terms
- ***[appliance trace](#the-appliancetrace-class)***: a sequence of consecutive average
power measurements (usually in 15 minute itervals) for a specific appliance
instance for an arbitrary length of time. Ex) Readings from Refrigerator 003
for the day of 01/01/2014
- ***[appliance instance](#the-applianceinstance-class)***: a specific device or example
of an appliance model which may have any number of traces associated with it.
Could additionally be a particular set of parameters for a generative model
such as a HMM. Furthermore, an appliance instance might be an aggregated (i.e.
not yet disaggregated) set of appliances. This is distinct from *appliance set*
below because its measured traces will not temporally overlap.
Ex) Refrigerator 006; &lambda;=(&pi;,A,&mu;,&sigma;).
- ***[appliance type](#the-appliancetype-class)***: a category of appliances which share
a set of meaningful features which may be used to distinguish it from other
appliance types.
- ***[appliance set](#the-applianceset-class)***: a set of appliance instances which
form a metered unit. Appliance sets might also be fabricated to form
ground-truth training, validation or testing sets for algorithmic
disaggregation tasks.

Given that datasets might be loaded from many external sources and combined or
manipulated in a variety of ways, we organize a general hierarchical structure
around these terms which is described briefly below. In general, the categories
below could be formed from sampled, generated, or disaggregated data.

### The ApplianceTrace class

#### Attributes
- `series`: a pandas Series with a single `DatetimeIndex`ed columns which are
timeseries of disaggregated or aggregated appliance traces
- `source`: a string ("pecan","oakpark","hmm",...) describing its origin
- `dataid`: (pecan only) a string representing the dataid of the origin home
- `schema`: (pecan only) a string representing the schema of origin
- `hmm_params`: (hmm only) a list of parameters associated with the origin hmms
- `instance_id`: (tracebase only) a string representing the id of the instance

#### Methods
- `get_sampling_rate()`: Returns a string representing the rate at which the series was sampled.
- `get_series()`: Returns the pandas series object representing this trace.
- `get_source()`: Returns the user-supplied trace source string.
- `set_series(series)`: Updates the series (such as after a resampling).
- `set_source(source)`: Updates the user-supplied source string.

#### Other properties
Blank values are zero, values should be consecutive. Total use is considered
a trace. Best practice: for 15min traces, keep time stamps at clean intervals.
If trace represents a electricity generation such as that from a solar panel,
(this usage of "generation" is meant to be distinct from the notion of data
"generated" by or sampled from a hidden markov model), traces should have
negative values.

### The ApplianceInstance class

#### Attributes
- `traces`: a temporally ordered list of traces with **enforced lack of time
overlap.**

#### Methods
- None

#### Other properties
Traces must have aligned (but not overlapping) time intervals sampled at the
same rate with the same offset.

### The ApplianceType class

#### Attributes
- `appliances`: a list of appliance instances of this type. An appliance could
belong to more than one type, which may arise for situations in which we have
varying levels of functional generality for appliance types. Ex) Refrigerator
vs. energy-star refrigerator).

#### Methods
- None

#### Other properties
Note: This will constitute a sort of way to standardize appliance names.

### The ApplianceSet class

#### Attributes
- `appliances`: a list of appliance instances with **enforced temporal
alignment** (i.e. Misaligned data must be dealt with upon initialization to
have a valid appliance set).
- [`df`]: a pandas dataframe with all appliance instances?

#### Methods
- `top_k`: Get top k energy-consuming appliances

#### Other properties
Possibly combine traces into a single dataframe? Export particular datasets?
Note that an appliance set may have multiple instances of a particular type.


Additional Documentation
------------------------
Additional documentation and example usage can be found [here](#). A live
example can be found [here](#).
