from sklearn import hmm
import utils
from copy import deepcopy
import numpy as np
import pandas as pd
from collections import OrderedDict


def init_HMM(pi_prior,a_prior,mean_prior,cov_prior):
    '''
    Initializes a trace object from a series and a metadata dictionary.
    Series must be sampled at a particular sample rate
    pi_prior is the starting probability of the HMM
    a_prior is the transition matrix of the HMM
    mean_prior is the initial mean value of each state
    cov_prior is the initial covariance of each state

    For an n-state HMM:
    *pi_prior is a 1-D numpy array of size n
    *a_prior is a 2-D numpy array of size n x n
    *mean_prior is an numpy array of size n
    *cov_prior is a 3-D numpy array that has been tiled into two rows,
    one column, and n third dimensional states.
    ex) np.tile(1,(2,1,n)) for uniform covariance to start with.
    '''
    model = hmm.GaussianHMM(pi_prior.size,'full',pi_prior,a_prior)
    model.means_ = mean_prior
    model.covars_ = cov_prior
    return model

def fit_trace_to_HMM(model,trace):
    '''
    Fits the given trace to the model. NaNs are turned into zeroes.
    '''
    trace_values = utils.trace_series_to_numpy_array(trace.series)
    model.fit([trace_values])
    startprob, means, covars, transmat = sort_learnt_parameters(model.startprob_,
            model.means_, model.covars_ , model.transmat_)
    model=hmm.GaussianHMM(startprob.size, 'full', startprob, transmat)
    model.means_ = means
    model.covars_ = covars
    return model

def fit_instance_to_HMM(model,instance):
    '''
    Fits the given instance to the model. NaNs are turned into zeroes.
    '''
    for trace in instance.traces:
        model=fit_trace_to_HMM(model,trace)
    return model

def generate_HMMs_from_type(type,pi_prior,a_prior,
        mean_prior,cov_prior,key_for_model_name=None):
    '''
    Generates a dictionary of HMMs using each instance of given type.
    The key to the dictionary is defined by the parameter 'key_for_model_name'
    which looks at each instances metadata and uses the value from that key
    in order to name the model. If no key is given, the model is named based on
    its index.
    '''
    instance_models=OrderedDict()
    for i,instance in enumerate(type.instances):
        if(key_for_model_name):
            instance_name=instance.traces[0].metadata[key_for_model_name]
        else:
            instance_name=i
        instance_models[instance_name]=init_HMM(pi_prior,a_prior,mean_prior,cov_prior)
        instance_models[instance_name]=fit_instance_to_HMM(instance_models[instance_name],
                instance)
    return instance_models

def generate_FHMM_from_HMMs(type_models):
    '''
    Takes a dictionary of models, where the keys are the device type name, and
    generates an FHMM of these models.
    '''
    list_pi=[]
    list_A=[]
    list_means=[]
    for device_type_name in type_models:
        list_pi.append(type_models[device_type_name].startprob_)
        list_A.append(type_models[device_type_name].transmat_)
        list_means.append(type_models[device_type_name].means_.flatten().
            tolist())
    pi_combined=compute_pi_fhmm(list_pi)
    A_combined=compute_A_fhmm(list_A)
    [mean_combined, cov_combined]=compute_means_fhmm(list_means)
    model_fhmm=create_combined_hmm(len(pi_combined),pi_combined,
            A_combined, mean_combined, cov_combined)


def predict_with_FHMM(model_fhmm,test_data,plot=False):
    '''
    Predicts the decoded states and power for the given test data with the
    given FHMM. test_data is a dictionary that should contain a key called
    'aggregated', as well as keys for each device that is in the FHMM.
    '''
    learnt_states=model_fhmm.predict(test_data['total'])
    decode_hmm(len(learnt_states), mean_prior,
            [appliance for appliance in type_models], learnt_states)
    plot_FHMM_and_predictions(test_data,decoded_power)

def plot_FHMM_and_predictions(test_data,decoded_power):
    '''
    This plots the actual and predicted power based on the FHMM.
    '''
    for i,device_type in enumerate(test_data):
        if(device_type is not 'use'):
            plt.figure()
            plt.plot(test_data[device_type],'g')
            plt.title('Ground Truth Power for %s' %device_type)
            plt.plot(decoded_power[device_type],'b')
            plt.title('Predicted Power for %s' %device_type)
            plt.ylabel('Power (W)')
            plt.xlabel('Time')
            plt.ylim((np.min(test_data[device_type])-10, np.max(test_data[device_type])+10))
            plt.tight_layout()

def get_best_instance_model(instance_models,device_type,key_for_model_name):
    dfs_model = {}
    best_model_score = 0
    for model_name in instance_models:
        instances_of_model = []
        for instance in device_type.instances:
            test_trace = instance.traces[0]
            instance_name = test_trace.metadata[key_for_model_name]
            test = utils.trace_series_to_numpy_array(test_trace.series)
            model_score = instance_models[model_name].score(test)
            instances_of_model.append([model_name,instance_name,model_score])
            if(model_score > best_model_score):
                best_model = instance_models[model_name]
        dfs_model[model_name] = pd.DataFrame(data=instances_of_model,
                columns=['Model_Instance','Test_Instance','Value'])
    model_averages = []
    for key in dfs_model:
        sum=0
        for row in dfs_model[key].iterrows():
            sum = sum+row[1]['Value']
        model_averages.append([key,sum/len(dfs_model[key].index)])
    print
    avg_model_df = pd.DataFrame(data=model_averages,
            columns=['Model_Instance','Avg Probability'])
    print avg_model_df.sort('Avg Probability',ascending=False)
    bestModel = avg_model_df.sort('Avg Probability',
            ascending=False).sort('Avg Probability',
                    ascending=False).head(1)['Model_Instance'].values[0]
    print str(bestModel) + ' is best.'
    return bestModel

def sort_startprob(mapping, startprob):
    '''
    Sort the startprob of the HMM according to power means; as returned by mapping
    '''

    num_elements = len(startprob)
    new_startprob = np.zeros(num_elements)
    for i in xrange(len(startprob)):
        new_startprob[i] = startprob[mapping[i]]
    return new_startprob

def sort_covars(mapping, covars):
    num_elements = len(covars)
    new_covars = np.zeros_like(covars)
    for i in xrange(len(covars)):
        new_covars[i] = covars[mapping[i]]
    return new_covars

def sort_transition_matrix(mapping, A):
    '''
    Sorts the transition matrix of the HMM according to power means; as returned by mapping
    '''
    num_elements = len(A)
    A_new = np.zeros((num_elements, num_elements))
    for i in range(num_elements):
        for j in range(num_elements):
            A_new[i,j] = A[mapping[i], mapping[j]]
    return A_new

def return_sorting_mapping(means):
    means_copy = deepcopy(means)
    # Sorting
    means_copy = np.sort(means_copy, axis = 0)
    # Finding mapping
    mapping = {}
    mapping_set=set()
    x=0
    for i, val in enumerate(means_copy):
        x= np.where(val==means)[0]
        for val in x:
            if val not in mapping_set:
                mapping_set.add(val)
                mapping[i]=val
                break
    return mapping

def sort_learnt_parameters(startprob, means, covars, transmat):
    '''
    Sorts the learnt parameters for the HMM
    '''
    mapping = return_sorting_mapping(means)
    means_new = np.sort(means, axis = 0)

    startprob_new = sort_startprob(mapping, startprob)
    covars_new = sort_covars(mapping, covars)
    transmat_new = sort_transition_matrix(mapping, transmat)
    assert np.shape(means_new) == np.shape(means)
    assert np.shape(startprob_new) == np.shape(startprob)
    assert np.shape(transmat_new) == np.shape(transmat)
    return [startprob_new, means_new, covars_new, transmat_new]

def compute_pi_fhmm(list_pi):
    '''
    Input: list_pi: List of PI's of individual learnt HMMs
    Output: Combined Pi for the FHMM
    '''
    result=list_pi[0]
    for i in range(len(list_pi)-1):
        result=np.kron(result,list_pi[i+1])
    return result

def compute_A_fhmm(list_A):
    '''
    Input: list_pi: List of PI's of individual learnt HMMs
    Output: Combined Pi for the FHMM
    '''
    result=list_A[0]
    for i in range(len(list_A)-1):
        result=np.kron(result,list_A[i+1])
    return result

def compute_means_fhmm(list_means):  
    '''
    Returns [mu, sigma]
    '''
    
    #list_of_appliances_centroids=[ [appliance[i][0] for i in range(len(appliance))] for appliance in list_B]
    states_combination=list(itertools.product(*list_means))
    print states_combination
    num_combinations=len(states_combination)
    print num_combinations
    means_stacked=np.array([sum(x) for x in states_combination])
    means=np.reshape(means_stacked,(num_combinations,1)) 
    cov=np.tile(5*np.identity(1), (num_combinations, 1, 1))
    return [means, cov] 

def create_combined_hmm(n, pi, A, mean, cov):
    combined_model=hmm.GaussianHMM(n_components=n,covariance_type='full', startprob=pi, transmat=A)
    combined_model.covars_=cov
    combined_model.means_=mean
    return combined_model

def decode_hmm(length_sequence, centroids, appliance_list, states):
    '''
    Decodes the HMM state sequence
    '''
    power_states_dict={}    
    hmm_states={}
    hmm_power={}
    total_num_combinations=1
    for appliance in appliance_list:
        total_num_combinations*=len(centroids[appliance])  

    for appliance in appliance_list:
        hmm_states[appliance]=np.zeros(length_sequence,dtype=np.int)
        hmm_power[appliance]=np.zeros(length_sequence)
        
    for i in range(length_sequence):
        factor=total_num_combinations
        for appliance in appliance_list:
            #assuming integer division (will cause errors in Python 3x)
            factor=factor//len(centroids[appliance])
            
            temp=int(states[i])/factor
            hmm_states[appliance][i]=temp%len(centroids[appliance])
            hmm_power[appliance][i]=centroids[appliance][hmm_states[appliance][i]]
            
    return [hmm_states,hmm_power]
