__author__ = 'Tizon'
import theano
import theano.tensor as T

class sigmoid(object):
    def __init__(self,X,W):
        s = 1/(1+T.exp(-T.dot(X,W)))
        self.sig = s
