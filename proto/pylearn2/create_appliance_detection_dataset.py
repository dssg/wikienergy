import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.pardir,os.pardir)))
import disaggregator as da
import disaggregator.PecanStreetDatasetAdapter as psda
import pylearn2.datasets as ds
import pickle
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create appliance detection datasets for pylearn2.')
    parser.add_argument('appliance',type=str,
            help='appliance to make the datasets around')
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

    db_url = "postgresql://USERNAME:PASSWORD@db.wiki-energy.org:5432/postgres"
    psda.set_url(db_url)

    window_length=24*4*7
    window_stride=24*4
    train,valid,test = psda.get_appliance_detection_arrays(
        schema,tables,args.appliance,window_length,window_stride,10)
    train_dataset = ds.DenseDesignMatrix(X=train[0],y=train[1])
    valid_dataset = ds.DenseDesignMatrix(X=valid[0],y=valid[1])
    test_dataset = ds.DenseDesignMatrix(X=test[0],y=test[1])

    with open('{data_dir}/{prefix}_train.pkl'
            .format(data_dir=args.data_dir,prefix=args.prefix), 'w') as f:
        pickle.dump(train_dataset,f)

    with open('{data_dir}/{prefix}_valid.pkl'
            .format(data_dir=args.data_dir,prefix=args.prefix), 'w') as f:
        pickle.dump(valid_dataset,f)

    with open('{data_dir}/{prefix}_test.pkl'
            .format(data_dir=args.data_dir,prefix=args.prefix), 'w') as f:
        pickle.dump(test_dataset,f)
    import pdb; pdb.set_trace()
