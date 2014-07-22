from pylearn2.config import yaml_parse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename",type=str,
    help="The filename of the yaml model.")
parser.add_argument("data_dir",type=str,
    help="The relative directory where datasets are stored.")
parser.add_argument("dataset_prefix",type=str,
    help="The prefix of the dataset.")
parser.add_argument("saved_model_prefix",type=str,
    help="The prefix for the saved model.")
args = parser.parse_args()

with open(args.filename,'r') as f:
    nn_yaml = f.read()

hyper_params = {"data_dir": args.data_dir,
                "dataset_prefix": args.dataset_prefix,
                "saved_model_prefix": args.saved_model_prefix}

train = yaml_parse.load(nn_yaml % hyper_params)
train.main_loop()
