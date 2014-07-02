import sys
sys.path.append('../')
#print sys.path

'''
    
   An interface for adapting Pecan Street data.
    
'''


import disaggregator.PecanStreetDatasetAdapter as pecan

import pickle

user_name = 'stomkins'
pw='PASSWORD'
host = "db.wiki-energy.org"
port = "5432"
db = "postgres"
db_url = "postgresql"+"://"+user_name+":"+pw+"@"+host+":"+port+"/"+db

table = {'curated':'\"PecanStreet_CuratedSets\"','raw':'\"PecanStreet_RawData\"','shared':'\"PecanStreet_SharedData\"'}

print 'There are two datasets you can view right now, one is called curated, and one is called shared.\n The shared data set has one minute interval data for Jan-May 2014, for about 200 homes. \n\n The curated data set has 15 mintue interval data for different intervals in 2013 and 2012, the largest interval lasting from 12/12-11/13. \n\n If you want to analyze longer term data, the curated set is recommended, whereas if you want shorter but more frequent data the shared set is recommended. \n\n Would you like to recieve data from the shared or curated set?'

dataset = input('Please enter either shared or curated in string format')

p = pecan(db_url)

schema = table[dataset]

schema_e= schema[1:len(schema)-1]

tables= p.set_table_names(schema_e)

print 'You can now view data for any of these months\n'

for i in tables:
    print i + '\n'

print 'Which month would you like to view data for?\nPlease enter one of the table names exactly as it is printed and as a string'

month = input("Please enter month\n")
print month
print "don't worry next step takes about a minute"

[i,a] = p.get_meta_table(schema,str(tables[0]))

print 'You can now load data for a single home. Here are the homes you can choose from:\n'

for home in i:
    print home

print 'each home has the same kind of appliances, here is a list of those appliances:'
print a

print 'You can now get trace information per house. You can also see the trace of a particular appliance. However this is the point where you are informed that \'seeing\' is actually a step that comes after pickling. So long story short what house, what appliance do you want to check out?'

house = input('Enter a home id\n')
appliance = input('Enter an appliance name (this is not actually necessary at this point)\n')

query = 'select * from {0}.{1} where dataid={2}'.format(schema, month,house)
df = p.get_dataframe(query).fillna(0)
temp = p.clean_dataframe(df,schema,[])
test = p.get_month_traces_per_dataid(schema,month,house)

print 'you now have a bunch of appliance traces, one trace for each appliance in a house'
print 'here is some information about the first trace '

print test[0].source

print 'do you want to pickle?\n coming soon!'



