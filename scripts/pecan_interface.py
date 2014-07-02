import sys
sys.path.append('../')
#print sys.path

'''

   An interface for adapting Pecan Street data.

'''


import disaggregator.PecanStreetDatasetAdapter as pecan
import pickle

# Open db connection
db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
p = pecan(db_url)

table = {'curated':'\"PecanStreet_CuratedSets\"',
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
dataset = input('Please enter either "shared" or "curated"(no quotes):\n')
schema = table[dataset]
schema_e= schema[1:len(schema)-1]
tables= p.set_table_names(schema_e)
print 'You can now view data for any of these months\n'
for i in tables:
    print i + '\n'

print '''Which month would you like to view data for?
Please enter one of the table names exactly as it is printed and as a string:
'''
month = raw_input()
print month
print "This next step takes about a minute..."

[i,a] = p.get_meta_table(schema,str(tables[0]))

print '''You can now load data for a single home.
Here are the homes you can choose from:\n'''

for home in i:
    print home

print '''Each home has the same kind of appliances. Here is a list of those
appliances:'''
print a

print '''You can now get trace information per house. You can also see the
trace of a particular appliance. However this is the point where you are
informed that "seeing" is actually a step that comes after pickling. So long
story short what house, what appliance do you want to check out?'''

house = input('Enter a home id\n')
appliance = input('Enter an appliance name (this is not actually necessary at\
this point):')

query = 'select * from {0}.{1} where dataid={2}'.format(schema, month,house)
df = p.get_dataframe(query).fillna(0)
temp = p.clean_dataframe(df,schema,[])
test = p.get_month_traces_per_dataid(schema,month,house)

print 'you now have a bunch of appliance traces, one trace for each appliance in a house'
print 'here is some information about the first trace '

print test[0].source

print 'do you want to pickle?\n coming soon!'



