import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.pardir,os.pardir)))
import disaggregator as da
import disaggregator.PecanStreetDatasetAdapter as psda
from pylearn2.datasets.vector_spaces_dataset import VectorSpacesDataset
from pylearn2.space import CompositeSpace
from pylearn2.space import Conv2DSpace
from pylearn2.space import VectorSpace
import pickle
import argparse
from copy import deepcopy
import numpy as np
import decimal
from scipy.sparse import csr_matrix

def create_dataset(schema,tables,ids, n_classes, which = None):
    all_instances = psda.generate_instances_for_appliances_by_dataids(schema,tables,
            ['use','air1','furnace1'],ids,sample_rate='15T')

    energy_arrays = []
    temperature_arrays = []
    time_arrays = []
    weekday_arrays = []
    target_arrays = []
    sorted_classes = np.linspace(0,1,n_classes + 1)[:-1]
    for instances,dataid in zip(all_instances,ids):
        # format use correctly
        use = instances[0].traces[0]
        use.series.fillna(0,inplace=True)
        use.series = use.series.astype(float).clip(0.0000001)
        use_windows = use.get_windows(window_length,window_stride)

        # create features sources
        energy_arrays.append(use_windows)
        temperature_arrays.append(np.tile([70],(use_windows.shape[0],1)))
        time_arrays.append(np.tile([12],(use_windows.shape[0],1)))
        weekday_arrays.append(np.tile([1,0,0,0,0,0,0],(use_windows.shape[0],1)))

        # determine targets
        air1 = instances[1].traces[0]
        furnace1 = instances[2].traces[0]
        total_air = da.utils.aggregate_traces([air1,furnace1],{})
        total_air.series.fillna(0,inplace=True)
        total_air.series = total_air.series.astype(float)
        ratio_series = total_air.series/use.series
        ratios = da.appliance.ApplianceTrace(ratio_series,{})
        ratio_windows = ratios.get_windows(window_length,window_stride)
        ratio_windows = ratio_windows[:,prediction_index].clip(0,1)
        classes = np.searchsorted(sorted_classes,ratio_windows,side='right') - 1
        target_arrays.append(classes_to_onehot(classes,n_classes))

    # create data tuple
    energy_arrays = np.concatenate(energy_arrays,axis=0)[:,:,np.newaxis,np.newaxis]
    temperature_arrays = np.concatenate(temperature_arrays,axis=0)
    time_arrays = np.concatenate(time_arrays,axis=0)
    weekday_arrays = csr_matrix(np.concatenate(weekday_arrays,axis=0))
    target_arrays = csr_matrix(np.concatenate(target_arrays,axis=0))
    data = (energy_arrays,temperature_arrays,time_arrays,weekday_arrays,target_arrays)

    # define the data specs
    space = CompositeSpace([
        Conv2DSpace(shape=[10,1],num_channels=1),
        VectorSpace(dim=1),
        VectorSpace(dim=1),
        VectorSpace(dim=7,sparse=True),
        VectorSpace(dim=n_classes,sparse=True)])
    source = ('features0','features1','features2','features3','targets')
    data_specs = (space,source)
    dataset = VectorSpacesDataset(data=data,data_specs=data_specs)
    with open(os.path.join(args.data_dir,args.prefix+'_'+which+'.pkl'),'w') as f:
        pickle.dump(dataset,f)

def classes_to_onehot(classes,n):
    one_hot = np.zeros((classes.shape[0],n))
    for i,n in enumerate(classes):
        one_hot[i,n] = 1
    return one_hot

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create appliance detection datasets for pylearn2.')
    parser.add_argument('data_dir',type=str,
            help='directory in which to store data')
    parser.add_argument('prefix',type=str,
            help='prefix for dataset files')
    args = parser.parse_args()

    schema = 'shared'
    tables = [u'validated_01_2014',
              u'validated_02_2014',
              u'validated_03_2014',
              u'validated_04_2014',
              u'validated_05_2014',]

    db_url = "postgresql:/USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
    psda.set_url(db_url)

    window_length = 10
    window_stride = 1
    prediction_index = 6

    all_ids = []
    for month in range(5):
        air1_ids = psda.get_dataids_with_real_values(schema,tables[month],'air1')
        furnace1_ids = psda.get_dataids_with_real_values(schema,tables[month],'furnace1')
        all_ids.append(air1_ids)
        all_ids.append(furnace1_ids)
    common_ids = da.utils.get_common_ids(all_ids)

    #n = len(common_ids)
    n = 4
    n_train = n/2
    n_valid = n/4
    n_test = n - (n/2 + n/4)
    train_ids = common_ids[:n_train]
    valid_ids = common_ids[n_train:n_train+n_valid]
    test_ids = common_ids[n_train+n_valid:n_train+n_valid+n_test]
    n_classes = 10

    for ids,which in zip([train_ids,valid_ids,test_ids],["train","test","valid"]):
        create_dataset(schema,tables[:1],ids,n_classes,which)
