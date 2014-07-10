import sys
sys.path.append('../')
#print sys.path

'''

   An interface for adapting Pecan Street data.

'''


import disaggregator.PecanStreetDatasetAdapter as pecan
import pickle
import disaggregator.utils as utils

# Open db connection
db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
pecan.set_url(db_url)

schema_names = {'curated':'\"PecanStreet_CuratedSets\"',
        'raw':'\"PecanStreet_RawData\"',
        'shared':'\"PecanStreet_SharedData\"'}

print '''There are two datasets you can view right now, one is called curated,
and one is called shared. The shared data set has one minute interval data
for Jan-May 2014, for about 200 homes.

The curated data set has 15 minute interval data for 2013 and 2012 (the largest
interval lasts from 12/12-11/13.

If you want to analyze longer term data, the curated set is recommended,
whereas if you want shorter but more frequent data the shared set
is recommended.

Would you like to recieve data from the shared or curated set?'''

# get tables from schema
dataset = raw_input('Please enter either "shared" or "curated"(no quotes):\n')
##this is wrong it depends which version is running
schema = dataset
#schema_e = schema[1:-1]
tables = pecan.get_table_names(schema)
print 'You can now view data for any of these months\n'
for i in tables:
    print i + '\n'

print '''Which month would you like to view data for?
Please enter one of the table names exactly as it is printed and as a string:
'''
month = raw_input()
print month
print "This next step takes about a minute..."

i,a = pecan.get_table_dataids_and_column_names(schema,str(month))

print '''You can now load data for a single home.
Here are the homes you can choose from:\n'''

for home in i:
    print home

print '''Each home has the same kind of appliances. Here is a list of those
appliances:'''
print a

print '''You can now get trace information per house. You can also see the
trace of a particular appliance. However this is the point where you are
informed that "seeing" is actually a step that comes after pickling. Do you want to pickle a house? If not you will be asked shortly to pickle a type? Enter yes or no'''
boo = raw_input()
if str(boo)=='yes':
    
    #house = raw_input('Enter a home id\n')
    #appliance = raw_input('Enter an appliance name (this is not actually necessary at\this point):')

    #query = 'select * from {0}.{1} where dataid={2}'.format(schema_names[schema], month,house)
    #df = p.get_dataframe(query).fillna(0)
    #   temp = p.clean_dataframe(df,schema,[])
    #   test = p.get_month_traces_per_dataid(schema,month,house)

    print 'you now have a bunch of appliance traces, one trace for each appliance in a house'
    print 'here is some information about the first trace '


elif str(boo)=='no':
    print 'ok what appliance do you want?'
    app = str(raw_input())
    print 'this step takes quite a while'
    pecan.set_url(db_url)
    dataids = pecan.get_dataids_with_real_values(schema,month,app)
    
    type = pecan.generate_traces_for_appliance_by_dataids(schema, month,app,dataids)
    utils.pickle_object(type, '{}_{}'.format(app,month))

else:
    print 'what was that?'





