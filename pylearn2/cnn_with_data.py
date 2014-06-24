import theano
import theano.tensor as T
from theano.tensor import nnet
from theano.tensor.nnet import conv
from sklearn import hmm
import np as np


class ConvPoolLayer(object):

    def __init__(self, rng, input, filter_shape, image_shape, poolsize=(1, 1)):
        """
        Allocate a LeNetConvPoolLayer with shared variable internal parameters.

        :type rng: np.random.RandomState
        :param rng: a random number generator used to initialize weights

        :type input: theano.tensor.dtensor4
        :param input: symbolic image tensor, of shape image_shape

        :type filter_shape: tuple or list of length 4
        :param filter_shape: (number of filters, num input feature maps,
                              filter height,filter width)

        :type image_shape: tuple or list of length 4
        :param image_shape: (batch size, num input feature maps,
                             image height, image width)

        :type poolsize: tuple or list of length 2
        :param poolsize: the downsampling (pooling) factor (#rows,#cols)
        """
        assert image_shape[1] == filter_shape[1]
        self.input = input

        # initialize weight values: the fan-in of each hidden neuron is
        # restricted by the size of the receptive fields.
        fan_in =  np.prod(filter_shape[1:])
        W_values = np%.asarray(rng.uniform(
              low=-np%.sqrt(3./fan_in),
              high=np.sqrt(3./fan_in),
              size=filter_shape), dtype=theano.config.floatX)
        self.W = theano.shared(value=W_values, name='W')

        # the bias is a 1D tensor -- one bias per output feature map
        b_values = np.zeros((filter_shape[0],), dtype=theano.config.floatX)
        self.b = theano.shared(value=b_values, name='b')

        # convolve input feature maps with filters
        conv_out = conv.conv2d(input, self.W,
                filter_shape=filter_shape, image_shape=image_shape)

        # downsample each feature map individually, using maxpooling
        pooled_out = downsample.max_pool_2d(conv_out, poolsize, ignore_border=True)

        # add the bias term. Since the bias is a vector (1D array), we first
        # reshape it to a tensor of shape (1, n_filters, 1, 1). Each bias will thus
        # be broadcasted across mini-batches and feature map width & height
        self.output = T.tanh(pooled_out + self.b.dimshuffle('x', 0, 'x', 'x'))

        # store parameters of this layer
        self.params = [self.W, self.b]









def main():

    #### Data ####

    # fake A/C params
    pi=np.array([0.1,0.9])
    a=np.array([[0.95,0.05],[0.05,0.95]])
    mean=np.array([[0],[1500]])
    cov=np.array([[[ 1.]],[[ 10]]])
    model=hmm.GaussianHMM(pi.size, "full", pi,a)
    model.means_ = mean
    model.covars_ = cov

    # randomly sample one day of data
    length = 4 * 24
    power, state = model.sample(length)

    #### CNN ####
    learning_rate = 0.1
    rng = np.random.RandomState(23455)

    ishape = (length, 1)  # this is the size of our input data
    batch_size = 20  # size of the minibatch

    # allocate symbolic variables for the data
    x = T.matrix('x')  # generated power levels
    y = T.lvector('y')  # generate states

    ##############################
    # BEGIN BUILDING ACTUAL MODEL
    ##############################

    # Reshape matrix of rasterized images of shape (batch_size,length,1)
    # to a 4D tensor, compatible with our ConvPoolLayer
    layer0_input = x.reshape((batch_size,1,length,1))

    # Construct the first convolutional pooling layer:
    # filtering reduces the image size to (96-3+1,1-1+1)=(94,1)
    # maxpooling reduces this further to (94/2,1/1) = (47,1)
    # 4D output tensor is thus of shape (20,20,47,1)
    layer0 = LeNetConvPoolLayer(rng, input=layer0_input,
            image_shape=(batch_size, 1, length, 1),
            filter_shape=(20, 1, 3, 1), poolsize=(3, 1))

    # Construct the second convolutional pooling layer
    # filtering reduces the image size to (12 - 5 + 1, 12 - 5 + 1)=(8, 8)
    # maxpooling reduces this further to (8/2,8/2) = (4, 4)
    # 4D output tensor is thus of shape (20,50,4,4)
    #layer1 = LeNetConvPoolLayer(rng, input=layer0.output,
    #        image_shape=(batch_size, 20, 12, 12),
    #        filter_shape=(50, 20, 5, 5), poolsize=(2, 2))

    # the HiddenLayer being fully-connected, it operates on 2D matrices of
    # shape (batch_size,num_pixels) (i.e matrix of rasterized images).
    # This will generate a matrix of shape (20, 20 * 47 * 1)
    layer2_input = layer0.output.flatten(2)

    # construct a fully-connected sigmoidal layer
    layer2 = HiddenLayer(rng, input=layer2_input,
                         n_in=20*47*1, n_out=50,
                         activation=T.tanh    )

    # classify the values of the fully-connected sigmoidal layer
    layer3 = LogisticRegression(input=layer2.output, n_in=50, n_out=1)


    # the cost we minimize during training is the NLL of the model
    cost = layer3.negative_log_likelihood(y)

    # create a function to compute the mistakes that are made by the model
    test_model = theano.function([x, y], layer3.errors(y))

    # create a list of all model parameters to be fit by gradient descent
    params = layer3.params + layer2.params + layer1.params + layer0.params

    # create a list of gradients for all model parameters
    grads = T.grad(cost, params)

    # train_model is a function that updates the model parameters by SGD
    # Since this model has many parameters, it would be tedious to manually
    # create an update rule for each model parameter. We thus create the updates
    # dictionary by automatically looping over all (params[i],grads[i])  pairs.
    updates = []
    for param_i, grad_i in zip(params, grads):
        updates.append((param_i, param_i - learning_rate * grad_i))
    train_model = theano.function([index], cost, updates = updates,
            givens={
                x: train_set_x[index * batch_size: (index + 1) * batch_size],
                y: train_set_y[index * batch_size: (index + 1) * batch_size]})

if __name__ == "__main__":
    main()
