__author__ = 'Tizon'
import numpy as np

class rndInitW(object):
    def __init__(self,L_in,L_out):
        epsilon_init = np.sqrt(6)/np.sqrt(L_in+L_out)
        self.W = np.random.random((L_out,1+L_in))*2*epsilon_init-epsilon_init
        self.W=self.W.astype(np.float32)
