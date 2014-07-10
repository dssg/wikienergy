from pylearn2.config import yaml_parse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename",type=str,
    help="The filename of the yaml model.")
args = parser.parse_args()

with open(args.filename,'r') as f:
    nn_yaml = f.read()

print nn_yaml

train = yaml_parse.load(nn_yaml)
train.main_loop()
