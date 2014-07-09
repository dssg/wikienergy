Dataset Adapters
================

Dataset Adapters are built for importing specific datasets into the format
used throughout the package which is described below. If you wish to use a
different source of data with the disaggregator library, your main task will be
to build a dataset adapter. A few examples have already been built by us.

Dataset adapters may make use of the methods in the `utils` module, but their
main purpose is to provide an interface for collecting appliance traces from
various traces.

Pecan Street Dataset Adapter
----------------------------

Overview
~~~~~~~~

The Pecan Street dataset includes a large repository of disaggregated traces
from submetered homes sampled at one-minute or fifteen-minute intervals.
Credentials are required for access to the database.

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

    from disaggregator import PecanStreetDatasetAdapter as psda

    # set the db_url before using any of the other functions.
    db_url="postgresql://user_name:password@host.url:port/db"
    psda.set_url(db_url)

    # get a list of table names for a schema
    table_names = psda.get_table_names('curated')

Methods
~~~~~~~

.. automodule:: disaggregator.PecanStreetDatasetAdapter
   :members:

Tracebase Dataset Adapter
-------------------------

Overview
~~~~~~~~

The Tracebase dataset contains many different types of individual appliance
twenty-four hour traces sampled at one-second intervals and grouped by
appliance-type. The traces for an individual appliance instance may or may not
be consecutive or temporally aligned with traces from other appliances. Traces
are grouped by filetype and their filenames indicate the appliance instance
and time period.

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

    import disaggregator as da
    folder_path='/home/steve/DSSG/wikienergy/data/Tracebase/'
    tbda=da.TracebaseDatasetAdapter(folder_path,'D','15T')
    cookingstove_type = tbda.generate_type('Cookingstove')

Methods
~~~~~~~

.. automodule:: disaggregator.TracebaseDatasetAdapter
   :members:

GreenButton Dataset Adapter
---------------------------
*[Future]*

Overview
~~~~~~~~

The Green Button xml format is a standard which is used by commercial energy
suppliers to provide end-users with historical energy usages

Methods
~~~~~~~

*[None]*
