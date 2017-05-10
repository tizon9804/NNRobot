__author__ = 'Tizon'
import cPickle
import os
import numpy as np

class targetManager:
    def __init__(self):
        self.NNLoaded={}
        self.DataLoaded=False
        self.DataSensorLoaded=False
        self.state={}
        self.path = '../../data/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def saveNN(self,name,costgrads):
        with open(self.path +str(name)+'.pkl', 'wb') as f:
             cPickle.dump(costgrads, f)
        print "NN ",name," saved..."

    def saveDataSet(self,data):
        with open(self.path +'dataSet.pkl', 'wb') as f:
             cPickle.dump(data, f)
        print "inputs X y saved..."

    def loadNN(self,name):
        try:
            print "trying to load the NN ",name
            self.state[name] = cPickle.load(open(self.path +str(name)+'.pkl','r'))
            self.NNLoaded[name]=True
            print "NN ",name," Loaded..."
            return True
        except Exception,e:
            print "error ",str(e)
            print "New NN ", name,"..."
            self.NNLoaded[name]=False
            return False

    def loadDataSet(self):
        try:
            self.dataset = cPickle.load(open(self.path +'dataSet.pkl','r'))
            self.DataLoaded = True
        except Exception,e:
            print str(e),"no data"
        return self.DataLoaded

    def loadElements(self):
       try:
           self.elements = cPickle.load(open(self.path + 'elements.pkl','r'))
           elements = self.elements
       except:
           elements = [np.array([]),np.array([])]
       return elements

    def saveElements(self,elements):
        with open(self.path + 'elements.pkl', 'wb') as f:
             cPickle.dump(elements, f)
        print "elements saved..."


