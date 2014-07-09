Disaggregator Package Overview
==============================


***Please view more up-to-date documentation at /docs/sphinx/html/index.html***

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
    import os.path
    sys.path.append(os.path.join(os.pardir,os.pardir))

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
[Utilities](#utils) |
[Evaluation Metrics](#evaluation-metrics) |
[Algorithm Classes](#algorithm-classes)
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

#### Example Usage

    from disaggregator import PecanStreetDatasetAdapter as psda

    # set the db_url before using any of the other functions.
    db_url="postgresql://user_name:password@host.url:port/db"
    psda.set_url(db_url)

    # get a list of table names for a schema
    table_names = psda.get_table_names('curated')

#### Methods
- `set_url(db_url)`:
  - Initialize an adapter using a database url string.
- `get_table_names(schema)`:
  - Returns a list of tables in the schema.
- `get_table_dataids(schema,table)`:
  - Returns a list of dataids for this schema and table
- `get_table_column_names(schema,table)`:
  - Returns a list of column names for this schema and table
- `get_table_dataids_and_column_names(schema,table)`:
  - Returns a list of dataids for this schema and table, and a list of the
    column names for this schema and table.
- `get_unique_dataids(schema,year,month,group=None)`:
  - Returns a list of dataids for a specifc schema ("curated","shared", or
    "raw"), month (int), year (int), and [group (int) - only if "curated"].
- `clean_dataframe(df,schema,drop_cols)`:
  - Cleans a dataframe queried directly from the database by renaming the db
    time column (ex. 'utc\_15min') to a column name 'time'. It then converts
    the time column to datetime objects and reindexes the dataframe to the time
    column before dropping that column from the dataframe. It also drops any
    columns included in the list `drop_cols`. The columns 'id' and 'dataid' are
    also dropped.
- `get_dataids_with_real_values(schema,table,appliance,ids)`:
  - Returns ids that contain non-'NoneType' values for a given appliance
- `generate_month_traces_from_table_name(schema,table,dataid)`:
  - Returns a list of traces for one house and one month
- `generate_set_by_house_and_month(schema,table,dataid)`:
  - Returns an ApplianceSet for given month and house.
- `get_table_name(schema,year,month,group=None, rate = None)`:
  - Given the year, month, and group return the table name.
- `generate_month_traces_from_attributes(schema,year,month,
group=None,rate=None,dataid=None)`:
  - Returns a list of traces from a given month. It first finds the table
    name associated with that month.
- `generate_traces_for_appliance_by_dataids(schema,table,app,ids)`:
  - Returns traces for a single appliance type across a set of dataids.
- `generate_type_for_appliance_by_dataids(schema,table,appliance,ids)`:
  - Given an appliance and a list of dataids, generate an ApplianceType
- `get_dataframe(query)`:
  - Returns a Pandas dataframe with the query results.

### TracebaseDatasetAdapter

#### Overview
The Tracebase dataset contains many different types of individual appliance
twenty-four hour traces sampled at one-second intervals and grouped by
appliance-type. The traces for an individual appliance instance may or may not
be consecutive or temporally aligned with traces from other appliances. Traces
are grouped by filetype and their filenames indicate the appliance instance
and time period.

#### Example Usage

    import disaggregator as da
    folder_path='/home/steve/DSSG/wikienergy/data/Tracebase/'
    tbda=da.TracebaseDatasetAdapter(folder_path,'D','15T')
    cookingstove_type = tbda.generate_type('Cookingstove')

#### Methods
- `get_trace_dates_from_instance(device,instance)`:
  - This function returns a unique set of dates (corresponding to
    individual files) for a single device instance id
- `generate_traces(device,instance_id,date)`:
  - Returns traces split across NAN values from a single file
- `split_on_NANs(series)`:
  - This function splits a trace into several traces,
    divided by the NAN values. Only outputs traces that have at
    least 6 hours of real values
- `generate_instance(device,instance_id)`:
  - This function imports the CSV files from a single device
    instance in a device folder
- `generate_type(device)`:
  - This function imports the CSV files from ALL device
    instances in a single device folder
- `get_unique_instance_ids(self,device)`:
  - This function returns a unique set of instance ids from tracebase

### GreenButtonDatasetAdapter _[Future]_
#### Overview
The Green Button xml format is a standard which is used by commercial energy
suppliers to provide end-users with historical energy usages

#### Methods
- None

## Appliance classes

### The ApplianceTrace class

#### Attributes
- `series`
  - a pandas Series with a single `DatetimeIndex`ed columns which are
    timeseries of disaggregated or aggregated appliance traces
- `metadata`:
  - a user-defined dictionary describing its origin

#### Methods
- `get_sampling_rate()`
  - Returns a string representing the rate at which the
    series was sampled.
- `get_total_usage()`:
  - Computes and returns the total usage of the trace.
- `print_trace()`:
  - Prints a summary of the trace

#### Other properties
Blank values are zero, values should be consecutive. Total use is considered
a trace. Best practice: for 15min traces, keep time stamps at clean intervals.
If trace represents a electricity generation such as that from a solar panel,
(this usage of "generation" is meant to be distinct from the notion of data
"generated" by or sampled from a hidden markov model), traces should have
negative values.

### The ApplianceInstance class

#### Attributes
- `traces`:
  - a temporally ordered list of traces with **enforced lack of time
overlap.**
- `metadata`:
  - a user-defined dictionary describing its origin

#### Methods
- `concatenate_traces(how="strict")`:
  - Takes its own list of traces and attempts to concatenate them.

#### Other properties
Traces must have aligned (but not overlapping) time intervals sampled at the
same rate with the same offset.

### The ApplianceType class

#### Attributes
- `appliances`: a list of appliance instances of this type. An appliance could
belong to more than one type, which may arise for situations in which we have
varying levels of functional generality for appliance types. Ex) Refrigerator
vs. energy-star refrigerator).
- `metadata`:
  - a user-defined dictionary describing its origin

#### Methods
- None

#### Other properties
Note: This will constitute a sort of way to standardize appliance names.

### The ApplianceSet class

#### Attributes
- `appliances`:
  - a list of appliance instances with **enforced temporal alignment**
    (i.e. Misaligned data must be dealt with upon initialization to
    have a valid appliance set).
- `metadata`:
  - a user-defined dictionary describing its origin
- [`df`]:
  - a pandas dataframe with all appliance instances?

#### Methods
- `make_dataframe()`:
  - Makes a new dataframe of the appliance instances. Throws an exception if
    the appliance instances have traces that don't align.
- `set_instances(instances)`:
  - Replaces the old instances with the new list. Makes a new dataframe using
    those instances.
- `generate_top_k_set(k)`:
  - Returns an ApplianceSet of the top k energy-consuming appliances
- `generate_non_zero_set()`:
  - Returns an ApplianceSet of all non-zero energy-consuming appliances


#### Other properties
Possibly combine traces into a single dataframe? Export particular datasets?
Note that an appliance set may have multiple instances of a particular type.

## Utils
#### Methods
- `aggregate_instances(instances, metadata, how="strict")`:
  - Given a list of temporally aligned instances, aggregate them into a single
    signal.
- `aggregate_traces(traces, metadata, how="strict")`:
  - Given a list of temporally aligned traces, aggregate them into a single
    signal.
- `get_common_ids(id_lists)`:
  - Returns a list of ids common to the supplied lists. (id set intersection)
- `concatenate_traces(traces, metadata=None, how="strict")`:
  - Given a list of appliance traces, returns a single concatenated
    trace. With how="strict" option, must be sampled at the same rate and
    consecutive, without overlapping datapoints.
- `concatenate_traces_lists(traces, metadata=None, how="strict")`:
  - Takes a list of lists of n traces and concatenates them into a single
    list of n traces.
- `order_traces(traces)`:
  - Given a set of traces, orders them chronologically and catches
    overlapping traces.
- `pickle_object(obj,title)`:
  - Given an object and a filename saves the object in pickled format to the
    data directory.

## Evaluation Metrics

#### Methods
- `sum_error(truth,prediction)`:
  - Given a numpy array of truth values and prediction values, returns the
    absolute value of the difference between their sums.
- `rss(truth,prediction)`:
  - Sum of squared residuals
- `guess_truth_from_power(signals,threshold)`:
  - Helper function for ground truth signals without on/off information.
    Given a series of power readings returns a numpy array where x[i]=0
    if signals[i] < threshold and x[i]=1 if signals[i] >= threshold
- `get_positive_negative_stats(true_states, predicted_states)`:
  - Returns a dictionary of numpy arrays containing the true positives a 'tp',
    the false negatives as 'fn', the true negatives as 'tn', and
    the false positives as 'fp'. I would like to make this a truth table
    instead of putting the logic directly in the list comprehension.
- `get_sensitivity(true_positives,false_negatives)`:
  - Given a numpy array of true positives, and false negatives returns a
    sensitivty measure. Then the sensitivity is equal to TP/(TP+FN), where TP
    is a true positive, such that TP=1 when the predicted value was correctly
    classified as positive and 0 otherwise and FN is false negative, such that
    FN = 1 if a value was falsely predicted to be negative and 0 otherwise.
- `get_specificity(true_negatives, false_positives)`:
  - Given a numpy array of true negatives, and false positives returns a
    specificty measure. The specificity measure is equal to TN/(TN+FP), where
    TN is a true negative, such that TN=1 when the predicted value was
    correctly classified as negative and 0 otherwise and FP is a false
    positive, such that FP = 1 if a value was falsely predicted to be positive
    and 0 otherwise.
- `get_precision(true_positives,false_positives)`:
  - Given a numpy array of true positives, and false positives returns a
    precision measure. The precision measure is equal to TP/(TP+FP), where TP
    is a true positive, such that TP=1 when the predicted value was correctly
    classified as positive and 0 otherwise and FP is a false positive, such
    that FP = 1 if a value was falsely predicted to be positive and 0
    otherwise.
- `get_accuracy(stats)`:
  - Takes an array of true positives, false negatives, true negatives,
    and false positives. Returns the Accuracy measure where accuracy is
    tp+tn/(tn+fn+tp+fp)

## Algorithm Classes

[TODO]


Additional Documentation
------------------------
Additional documentation and example usage can be found [here](#). A live
example can be found [here](#).
