from pylearn2.config import yaml_parse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename",type=str,
    help="The filename of the yaml model.")
args = parser.parse_args()

with open(args.filename,'r') as f:
    simple_nn = f.read()

print simple_nn

train_softmax = yaml_parse.load(simple_nn)
train_softmax.main_loop()
