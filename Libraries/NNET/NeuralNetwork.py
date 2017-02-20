__author__ = 'Tizon'
import numpy as np
from RandInitializeWeights import rndInitW


class CNNET(object):
    """Pool Layer of a convolutional network """

    def __init__(self, type, input_layer_size, num_hidden_layer, hidden_layer_size, num_output_Layer):
        # -----------------------------------------------------------
        num_hidden_layer -= 1
        print "checking existing brain"
        print "----------------------------initializing baby brain ", type
        brain1 = rndInitW(input_layer_size, hidden_layer_size).W
        brainHidden = rndInitW((hidden_layer_size * num_hidden_layer) + (num_hidden_layer - 1), hidden_layer_size).W
        brainOut = rndInitW(hidden_layer_size, num_output_Layer).W
        print "brain input", brain1.shape
        print "brain hidden", brainHidden.shape
        print "brain out", brainOut.shape
        brain1 = brain1.flatten()
        brainHidden = brainHidden.flatten()
        brainOut = brainOut.flatten()
        brain = np.append(brain1, brainHidden)
        brain = np.append(brain, brainOut)
        print "baby brain", brain.shape
        self.brain = brain
