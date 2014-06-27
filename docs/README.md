Disaggregator Documentation
===========================

Basic usage
-----------
Basic usage of the disaggregator module during development is as follows:

    import sys
    sys.path.add('../../') # or non-Unix equivalent

    import disaggregator

Disaggregator Module
--------------------
The disaggregator module is structured around appliances. We use the
following terms through the documentation:

### Terms
- ***[appliance trace](#appliance-trace)***: a sequence of consecutive average
power measurements (usually in 15 minute itervals) for a specific appliance
instance for an arbitrary length of time. Ex) Readings from Refrigerator 003
for the day of 01/01/2014
- ***[appliance instance](#appliance-instance)***: a specific device or example
of an appliance model which may have any number of traces associated with it.
Could additionally be a particular set of parameters for a generative model
such as a HMM. Furthermore, an appliance instance might be an aggregated (i.e.
not yet disaggregated) set of appliances. This is distinct from *appliance set*
below because its measured traces will not temporally overlap.
Ex) Refrigerator 006; \lambda=(\pi,\A,\mu,\sigma)
- ***[appliance type](#appliance-type)***: a category of appliances which share
a set of meaningful features which may be used to distinguish it from other
appliance types.
- ***[appliance set](#appliance-set)***: a set of appliance instances which
form a metered unit. Appliance sets might also be fabricated to form
ground-truth training, validation or testing sets for algorithmic
disaggregation tasks.

Given that datasets might be loaded from many external sources and combined or
manipulated in a variety of ways, we organize a general hierarchical structure
around these terms which is described briefly below. In general, the categories
below could be formed from sampled, generated, or disaggregated data.

### The ApplianceTrace class
#### Attributes
- `trace`: a pandas Series with a single `DatetimeIndex`ed columns which are
timeseries of disaggregated or aggregated appliance traces
- `source`: a string ("pecan","oakpark","hmm",...) describing its origin
- `dataid`: (pecan only) a string representing the dataid of the origin home
- `schema`: (pecan only) a string representing the schema of origin
- `hmm_params`: (hmm only) a list of parameters associated with the origin hmms
#### Methods
- None

### The ApplianceInstance class
#### Attributes
- `traces`: a temporally ordered list of traces with **enforced lack of time
overlap.**
#### Methods
- None

### The ApplianceType class
#### Attributes
- `appliances`: a set of appliance instances of this type. An appliance could
belong to more than one type, which may arise for situations in which we have
varying levels of functional generality for appliance types. Ex) Refrigerator
vs. energy-star refrigerator).
#### Methods
- None

### The ApplianceSet class
#### Attributes
- `appliances`: a list of appliance instances with **enforced temporal
alignment.**
#### Methods
- None


(thought - organization around polymorphic appliances instead?)

Pandas DataFrame, DatetimeIndex-ed
Must include use column
Columns are appliances
Rows indexed by utc time
Blank values are zero.
Dataframe can have any number of rows
Dataframe interval should be 15min.
timestamps should be at clean 15min intervals (like at the hour)
no time column (use index instead)
dataframe is for one metered unit (house, building).
gen values must be negative.
get rid of subpanels. 
Keep track of appliances per column?
remove all-zero columns?
map from numbers to names for columns?
data
Source attribute ("pecan", "tracebase", "hmm"..., "oak_park") - mostly for humans
if pecan, must have dataid, table attribute (None, otherwise
if hmm, must have hmm used to make it
if tracebase, must have instance id. 
could have any number of columns.
dealing with multiples(2 fridges)?
pick standard column names?
Generated data format
same

Algorithmically disaggregated data
same

The following lists describes standards for the dataset class:
- Datasets 
- 


Additional documentation and example usage can be found [here](#). A live example
can be found [here](#).
