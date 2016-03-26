import sys
sys.path.append('../') # or non-Unix equivalent (add wikienergy/ to path)
import numpy as np
import pickle
import matplotlib.pyplot as plt
from disaggregator import PecanStreetDatasetAdapter as psda
from disaggregator import utils
from disaggregator import fhmm
from disaggregator import evaluation_metrics as metric
from hmmlearn import hmm
from copy import deepcopy
import pymc
import pylab

def get_model_error_from_trace0(test_instances,model,plot=False):
    error=[]
    for obs_house in test_instances:
        obs_power=utils.trace_series_to_numpy_array(obs_house.traces[0].series)
        est_states=model.predict(obs_power)
        est_power=[]
        for val in est_states:
		est_power.append(float(np.random.normal(model._means_[val],model._covars_[val],1)[0]))
        if(plot):
            plt.figure()
            plt.plot(obs_power,'k')
            plt.plot(est_power,'b',alpha=.5)
        error.append(metric.sum_error(obs_power,np.array(est_power)))
    return np.mean(error)

def get_test_data(num_houses):
	devices_types_unsampled={}
	ids_for_devices={}
	db_url='postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres'
	psda.set_url(db_url)
	schema = 'shared'
	tables= psda.get_table_names(schema)
	print tables
	table=tables[3]
	ids_device_name='air1'
	ids_for_devices[ids_device_name]=psda.get_dataids_with_real_values(schema,table,ids_device_name)

	device_name='air1'
	devices_types_unsampled[device_name]=psda.generate_type_for_appliance_by_dataids(schema,table,device_name,ids_for_devices[ids_device_name][:num_houses])
	device_name='use'
	devices_types_unsampled[device_name]=psda.generate_type_for_appliance_by_dataids(schema,table,device_name,ids_for_devices[ids_device_name][:num_houses])
	

	#Resamples the data
	devices_types={}
	devices_types_unsplit={}
	sample_rate='1T'
	length='D'
	for key in devices_types_unsampled:
	    devices_types_unsplit[key]=devices_types_unsampled[key].resample(sample_rate)
	    #devices_types[key]=devices_types_unsplit[key].split_by(length)
	    devices_types[key]=devices_types_unsplit[key]
	    print "Resampled " + str(key)
	
	return devices_types

def make_model_metric_pickle(state1_min_mean,state1_max_mean,state1_min_cov,state1_max_cov,num_iter,num_test_houses):
	devices_types=get_test_data(num_test_houses)
	errors_mean_cov=[]
	error_dict={}
	device_type_name='air1'
	state1_means = np.linspace(state1_min_mean,state1_max_mean,num_iter)
	state1_covs = np.linspace(state1_min_cov,state1_max_cov,num_iter)
	best_error=100000000
	for state1_mean in state1_means:
	    errors_cov=[]
	    for state1_cov in state1_covs:
		print str(state1_mean)+", "+str(state1_cov)
		pi_prior=np.array([0.9,0.1])
		a_prior=np.array([[0.95,0.05],[0.05,0.95]])
		mean_prior=np.array([[0],[state1_mean]])
		cov_prior=np.array([[[0.0001]],[[state1_cov]]])
		model = hmm.GaussianHMM(pi_prior.size,'full',pi_prior,a_prior)
		model.means_ = mean_prior
		model.covars_ = cov_prior
		error=get_model_error_from_trace0(devices_types[device_type_name].instances,model)
		if(error<best_error):
		    best_mean=state1_mean
		    best_cov=state1_cov
		    best_error=error
		errors_cov.append(error)  
	    errors_mean_cov.append(errors_cov)
	error_dict['error_vals']=errors_mean_cov
	error_dict['cov_vals']=state1_covs
	error_dict['mean_vals']=state1_means
	error_dict['best_mean']=best_mean
	error_dict['best_cov']=best_cov
	error_dict['best_error']=best_error
	with open('error_m_'+str(state1_min_mean)+'_'+
		  str(state1_max_mean)+'_c_'+str(state1_min_cov)+'_'+str(state1_max_cov)+'.pkl','w') as f:
	    pickle.dump(error_dict,f)


state1_min_mean=1.5
state1_max_mean=3.25
state1_min_cov=0.0001
state1_max_cov=0.1
num_iter=50
num_houses=25
make_model_metric_pickle(state1_min_mean,state1_max_mean,state1_min_cov,state1_max_cov,num_iter,num_houses)
