__author__ = 'Tizon'
import numpy as np
from NeuralManager.nnet import NNCostFunction
class assemble(object):
    """Pool Layer of a convolutional network """

    def __init__(self,input,brain,input_layer_size,num_hidden_layer,hidden_layer_size,num_output_Layer):
        #m=input.shape[0]
        num_hidden_layer-=1
        self.thetain=np.reshape(brain[0:hidden_layer_size*(input_layer_size+1)],\
                          (hidden_layer_size,(input_layer_size+1)))
        self.hiddenTheta={}
        thetainsize= self.thetain.flatten().shape[0]
        print "##theta1",self.thetain.shape
        for i in range(0,num_hidden_layer):
           self.hiddenTheta[i]=np.reshape(brain[i+thetainsize+\
                             hidden_layer_size*i*(hidden_layer_size+1):\
                             (i+thetainsize)+hidden_layer_size*(i+1)*(hidden_layer_size+1)],\
                             (hidden_layer_size,hidden_layer_size+1))
           print "##hidden theta ",i,":",self.hiddenTheta[i].shape

        self.thetaout=np.reshape(brain[thetainsize+\
                             hidden_layer_size*num_hidden_layer*(hidden_layer_size+1):],\
                             (num_output_Layer,(hidden_layer_size+1)))
        print "##thetaOut",self.thetaout.shape

    def think(self,X,costgrads,elements):
        Xb=np.ones((X.shape[0],X.shape[1]+1))
        Xb[:,1:]=X.astype(np.float32)
        Xb=Xb.astype(np.float32)
        self.pred,self.proba=costgrads.maxOptFunction(Xb[0])
        self.hn=Xb
        if self.proba > 0.8:
            print "prediction!!!-->",int(self.pred)," object",elements[int(self.pred)]," prediction probability!!!-->", (self.proba*100),"%"



            #print "object",elements[int(self.pred)]
            #print "prediction probability!!!-->", self.proba
            #print "cost",costgrads.testcost(Xb[0],[0,1])
            #print "zout",costgrads.zout(Xb[0])
            #print "------------------------------------------------------"
    def accuracy(self,X,y,costgrads):
        Xb=np.ones((X.shape[0],X.shape[1]+1))
        Xb[:,1:]=X
        self.pred=np.array(())
        self.accuracyProbability=np.array(())
        for inp in range(Xb.shape[0]):
            self.pred=np.append(self.pred,costgrads.maxFunction(Xb[inp]))
            self.accuracyProbability=np.append(self.accuracyProbability,costgrads.maxpFunction(Xb[inp]))
        self.accuracy=np.mean(self.pred==np.asarray(y))*100
        self.accuracyProbability=np.mean(self.accuracyProbability)*100
        print "element predicted", self.pred
        print "element expected", y
        print "accuracy is: ",self.accuracy,"%"
        print "probabilities of the accuracy ",self.accuracyProbability,"%"