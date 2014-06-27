Disaggregator Documentation
===========================

Basic usage
-----------
Basic usage of the disaggregator module during development is as follows:

    import sys
    sys.path.add('../../')

    import disaggregator

Disaggregator Module
--------------------
The disaggregator module is structured around appliances. We've use the
following terms through the documentation:

### Terms
- ***appliance trace***:
- ***appliance instance***:
- ***appliance type***:
- ***appliance set***:

Given that datasets might be loaded from many external sources and combined or
manipulated in a variety of ways, we organize a general hierarchical structure
described briefly below.

### The Dataset class

The main data structure of the disaggregation library is called the Dataset.
Datasets are formed from sampled, generated, or disaggregated data. Datasets are
meant to model metered units such as a building or home, and contain
descriptions of the power traces of the appliances (either directly measured or
generated) which they contain. They are meant to be versatile data structures
which facilitate use in algorithms.

Datasets have the following attributes:
- `df`, a pandas dataframe with a `DatetimeIndex` containing columns which are
timeseries of disaggregated or aggregated appliance traces
- `source` a list of length `n_columns` containing a string ("pecan","oakpark",
"hmm",...) describing its origin
- `dataid` (pecan only) a list of length `n_columns` containing integers
representing the dataid of the origin home
- `table` (pecan only) a list of length `n_columns` containing an (per column)
- `column_mapping` a list of length `n_columns`, describing
- `hmm_params` (hmm only) a list of parameters associated with the origin hmms
instance_id

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
