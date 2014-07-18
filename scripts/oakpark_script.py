

'''
    
    An interface for adapting Oak Park data.
    
'''
import sys
sys.path.append('../')

import disaggregator.OakParkDatasetAdapter as opdsa
import disaggregator.utils as utils

print "Hello! Ready to get your hands on some Oak Park data? I'm sure you said yes, just hold tight..."

db = opdsa.get_db_connection()

homes = opdsa.get_homes(db)

dataids = homes.keys()

pickle_thing = None
pickle_name = None

print "You've got two choices: you can generate a trace for a house,"\
 "or you can generate a set of all traces for all homes for a given"\
 " year and month. So would you like to generate a set, or a trace?"

reply = raw_input("Please enter set or trace\n")

if reply=="trace":

    print "Here are the homes you can see:\n"

    for di in dataids:
        print di

    home=raw_input("Which one do you want a trace of?\n")

    print "OK hold on"

    trace = opdsa.generate_trace_by_dataid(homes,home)

    print_permission = raw_input("Would you like to see it? Enter yes or no\n")

    if print_permission=='yes':
        print trace
    pickle_thing=trace
    pickle_name = str(home)

elif reply=="set":
    print "You can see any month in 2013, and any month up to July in 2014."
    year = raw_input("Please enter 2014 or 2013\n")
    month = raw_input("Please enter a number one through twelve\n")
    print "Ok hold on"
    app_set = opdsa.generate_set_by_year_month(homes,int(year),int(month))
    pickle_thing=app_set
    pickle_name = '{}_{}'.format(str(year),str(month))
else:
    print "HEY! I said trace or set dum dum"

pickle_permission = raw_input("Would you like a pickle with that? Enter yes or no\n")

if pickle_permission=='yes':
    utils.pickle_object(pickle_thing,pickle_name)
else:
    print "Okie Doke, thanks for coming!"

#print trace.resample('MS').series

