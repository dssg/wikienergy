

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

print "Here are the homes you can see:\n"

for di in dataids:
    print di

home=raw_input("Which one do you want a trace of?\n")

print "OK hold on"

trace = opdsa.generate_trace_by_dataid(homes,home)

print_permission = raw_input("Would you like to see it? Enter yes or no\n")

if print_permission=='yes':
    print trace

pickle_permission = raw_input("Would you like a pickle with that? Enter yes or no\n")

if pickle_permission=='yes':
    utils.pickle_object(trace,'{}'.format(home))
else:
    print "Okie Doke, thanks for coming, check back in for sets and stuff!"