from pylearn2.config import yaml_parse

simple_nn = open('simple_nn.yaml','r').read()

print simple_nn

train_softmax = yaml_parse.load(simple_nn)
train_softmax.main_loop()
