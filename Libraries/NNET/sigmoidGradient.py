__author__ = 'Tizon'
import theano
import theano.tensor as T


class sigmoidGradient(object):
    def __init__(self):
        x = T.dmatrix('x')
        ds = (1 + T.tanh(x / 2)) / 2
        s = ds*(1-ds)
        sigG = theano.function([x], s)
        self.sigG = sigG