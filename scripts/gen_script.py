import sys
sys.path.append('../')
from disaggregator import fhmm
from disaggregator import PecanStreetDatasetAdapter as psda
import pickle
import numpy as np


def get_type_from_dataset(device_name,table_num,limit=0):
    '''
    Given the device name
    '''

    devices_types={}
    devices_types_unsampled={}
    db_url='postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres'
    psda.set_url(db_url)
    schema = 'shared'
    table='validated_0'+str(table_num)+'_2014'
    ids_for_device=psda.get_dataids_with_real_values(schema,table,device_name)
    if(limit>len(ids_for_device) or limit==0):
        limit=len(ids_for_device)
    device_type_orig=psda.generate_type_for_appliance_by_dataids(schema,
            table,device_name,ids_for_device[:limit])
    return device_type_orig

def resample_and_split(device_type_orig,length='D',sample_rate='15T',split=True,sample=True):
    if(sample):
        device_type_unsplit=device_type_orig.resample(sample_rate)
    else:
        device_type_unsplit=device_type_orig
    if(split):
        device_type=device_type_unsplit.split_by(length)
    else:
        device_type=device_type_unsplit
    return device_type

def generate_and_pickle_models(device_name,pi_prior,a_prior,mean_prior,cov_prior,
        key_for_model_name,table_num,length='D',sample_rate='15T',limit=0):
    device_type_orig=get_type_from_dataset(device_name,table_num,limit)
    print 'Device Type Generated.'
    device_type=resample_and_split(device_type_orig,length,sample_rate)
    print 'Device Type Resampled.'
    device_models=fhmm.generate_HMMs_from_type(device_type,pi_prior,a_prior,mean_prior,cov_prior,
            key_for_model_name)
    print 'Device Model Completed.'
    with open(str(device_name)+'_'+str(table_num)+'_' + str(sample_rate)+'.pkl','w') as f:
       pickle.dump(device_models,f)
    return device_type,device_models


pi_prior=np.array([0.5,0.5])
a_prior=np.array([[0.98,0.02],[0.02,0.98]])
mean_prior=np.array([[0],[2]])
cov_prior=np.tile(1, (2, 1, 1))
generate_and_pickle_models('air1',pi_prior,a_prior,mean_prior,cov_prior,'dataid',5,'D','1T')
