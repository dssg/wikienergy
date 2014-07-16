from sklearn import hmm
import utils
from copy import deepcopy
import numpy as np
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
        pi_prior is a 1-D numpy array of size n
        a_prior is a 2-D numpy array of size n x n
        mean_prior is an numpy array of size n
        cov_prior is a 3-D numpy array that has been tiled into two rows,
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
    model_list=OrderedDict()
    for i,instance in enumerate(type.instances):
        if(key_for_model_name):
            instance_name=instance.traces[0].metadata[key_for_model_name]
        else:
            instance_name=i
        model_list[instance_name]=init_HMM(pi_prior,a_prior,mean_prior,cov_prior)
        model_list[instance_name]=fit_instance_to_HMM(model_list[instance_name],instance)
    return model_list

def generate_FHMM_from_HMMs(model_list,key_for_model_name=None):
    '''
    Takes a dictionary of models, where the keys are the device type name, and
    generates an FHMM of these models.
    '''
    pass

def get_best_instance_model(model_list,device_type,key_for_model_name):
    dfs_model = {}
    best_model_score = 0
    for model_name in model_list:
        instances_of_model = []
        for instance in device_type.instances:
            test_trace = instance.traces[0]
            instance_name = test_trace.metadata[key_for_model_name]
            test = values_to_array(test_trace.series)
            model_score = models[model_name].score(test)
            instances_of_model.append([model_name,instance_name,model_score])
            if(model_score > best_model_score):
                best_model = models[model_name]
        dfs_model[model_name] = pd.DataFrame(data=instances_of_model,columns=['Model_Instance','Test_Instance','Value'])
    model_averages = []
    for key in dfs_model:
        sum=0
        for row in dfs_model[key].iterrows():
            sum = sum+row[1]['Value']
        model_averages.append([key,sum/len(dfs_model[key].index)])
    print
    avg_model_df = pd.DataFrame(data=model_averages,columns=['Model_Instance','Avg Probability'])
    print avg_model_df.sort('Avg Probability',ascending=False)
    bestModel = avg_model_df.sort('Avg Probability',ascending=False).sort('Avg Probability',ascending=False).head(1)['Model_Instance'].values[0]
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
