Disaggregator Package Overview
==============================

Datasets might be loaded from many external sources and combined or
manipulated in a variety of ways toward the end of energy disaggregation;
therefore, we organize a general hierarchical structure around appliance traces
and other elements described below in order to serve as ground truth training
sets for algorithmic models.

The main tasks facilitated by this package are:
- Importing appliance traces
- Organizing appliance traces into appliance instances, types, and sets
- Algorithms for completing the following three tasks:
  - Determining appliance presence in new traces
  - Given appliance presence, determine on-off states for each time point
  - Given appliance states, reconstruct original signals
- Evaluating algorithmic results

Basic usage
-----------
Basic usage of the disaggregator module during development is as follows:

    import sys
    sys.path.append('../../') # or non-Unix equivalent (add wikienergy/ to path)

    import disaggregator as da

Terms
-----
We use the following terms throughout the documentation to refer to different
aspects of appliance level energy usage. In general, items in the categories
described below could be formed from sampled, generated, or disaggregated data.
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

Structural Elements
-------------------
[Dataset Adapters](#dataset-adapters) |
[Appliance Classes](#appliance-classes) |
[Algorithm Classes](#algorithm-classes) |
## Dataset Adapters

Dataset Adapters are built for importing specific datasets into the format
used throughout the package which is described below. If you wish to use a
different source of data with the disaggregator library, your main task will be
to build a dataset adapter. A few examples have already been built by us.

Dataset adapters may make use of the methods in the `utils` module, but their
main purpose is to provide an interface for collecting appliance traces from
various traces.


### PecanStreetDatasetAdapter
#### Overview
The Pecan Street dataset includes a large repository of disaggregated traces
from submetered homes sampled at one-minute or fifteen-minute intervals.
Credentials are required for access to the database.

#### Methods
- None

### TracebaseDatasetAdapter
#### Overview
The Tracebase dataset contains many different types of individual appliance
twenty-four hour traces sampled at one-second intervals and grouped by
appliance-type. The traces for an individual appliance instance may or may not
be consecutive or temporally aligned with traces from other appliances. Traces
are grouped by filetype and their filenames indicate the appliance instance
and time period.

#### Methods
- None

### GreenButtonDatasetAdapter [Future]
#### Overview
The Green Button xml format is a standard which is used by commercial energy
suppliers to provide end-users with historical energy usages

#### Methods
- None

## Appliance classes

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
- `get_metadata()`: Returns the user-supplied trace metadata dict.
- `get_total_usage()`: Computes and returns the total usage of the trace.
- `set_series(series)`: Updates the series (such as after a resampling).
- `set_metadata(metadata)`: Updates the user-supplied metadata dict.
- `print_trace()`: Prints a summary of the trace

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
- `add_traces(traces)`: Updates the list of traces to include the traces in the
newly supplied list of traces.
- `get_traces()`: Returns a reference to the list of traces owned by the
appliance.
- `set_traces()`: Sets the list of traces owned by the appliance
- `order_traces(traces)`: Given a set of traces, orders them chronologically
and catches overlapping traces.

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
- `add_instances(instances)`: Add instances to the list of instances. (Check
for uniqueness?)
- `get_instances()`: Returns the list of appliance instances which are members
of this type.
- `set_instances(instances)`: Replaces the old list of instances with the new
set of instances. (Check for uniqueness?)

#### Other properties
Note: This will constitute a sort of way to standardize appliance names.

### The ApplianceSet class

#### Attributes
- `appliances`: a list of appliance instances with **enforced temporal
alignment** (i.e. Misaligned data must be dealt with upon initialization to
have a valid appliance set).
- [`df`]: a pandas dataframe with all appliance instances?

#### Methods
- `add_instances(instances)`: Adds the list of appliances to the appliance set.
- `add_to_dataframe(instances)`: Adds a new list of appliances to the
dataframe.
- `get_dataframe()`: Returns the dataframe object representing the dataset.
- `make_dataframe()`: Makes a new dataframe of the appliance instances. Throws
an exception if the appliance instances have traces that don't align.
- `set_instances(instances)`: Replaces the old instances with the new list.
Makes a new dataframe using those instances.
- `top_k`: Get top k energy-consuming appliances


#### Other properties
Possibly combine traces into a single dataframe? Export particular datasets?
Note that an appliance set may have multiple instances of a particular type.

## Algorithm Classes

[TODO]


Additional Documentation
------------------------
Additional documentation and example usage can be found [here](#). A live
example can be found [here](#).
