__author__ = 'Tizon'
import theano
import theano.tensor as T
import numpy as np
from sigmoid import sigmoid
class costGrads:
    def __init__(self,thetain,hiddenTheta,thetaout):
        #define theano function
        print "creating symbolic variables"
        self.x=T.fvector("x")
        self.y=T.ivector("y")
        self.win=theano.shared(thetain.T)
        self.wout=theano.shared(thetaout.T)
        self.thetas=[self.win]
        self.wt=[]
        for theta in hiddenTheta:
            wt=theano.shared(hiddenTheta[theta].T)
            self.wt+=[wt]
            self.thetas+=[wt]
        self.thetas+=[self.wout]
    def setState(self,win,wt,wout):
        self.win.set_value(win)
        self.thetas=[self.win]
        for i in range(len(self.wt)):
            self.wt[i].set_value(wt[i])
            self.thetas+=[self.wt[i]]
        self.wout.set_value(wout)
        self.thetas+=[self.wout]
    def getState(self):
        win=self.win.get_value()
        wt=[]
        for i in range(len(self.wt)):
            wt+=[self.wt[i].get_value()]
        wout=self.wout.get_value()
        return [win,wt,wout]
    def createFunction(self):
        print "nncostfunction..."
        print "sigmoid of X in thetain"
        zin=sigmoid(self.x,self.win).sig
        zhid=zin
        for wt in self.wt:
            zhid=T.concatenate([T.ones((1),zhid.dtype),zhid],axis=0)
            zhid=sigmoid(zhid,wt).sig
        print "sigmoid of zhid in thetaout"
        zhid=T.concatenate([T.ones((1),zhid.dtype),zhid],axis=0)
        zout=sigmoid(zhid,self.wout).sig
        print "creating function"
        logistic=(-self.y*T.log(zout))-((1-self.y)*T.log(1-zout))
        logistic=T.mean(logistic)
        #regular=T.sum(self.win**2)
        #for wt in self.wt:
         #  regular+=T.sum(wt**2)
        #regular+=T.sum(self.wout**2)
        #regular=regular*0.01
        #logistic=logistic+regular
        gs=T.grad(logistic,self.thetas)
        self.cost,self.grads=logistic,gs
        self.max=T.argmax(zout)
        self.maxp=T.max(zout)
        self.maxFunction=theano.function([self.x],T.argmax(zout))
        self.zoutt=zout
        self.maxOptFunction = theano.function(
                                    inputs=[self.x],
                                    outputs=[T.argmax(zout),T.max(zout)],
                                    mode='FAST_RUN')
        self.zout=theano.function([self.x],zout)
        self.maxpFunction=theano.function([self.x],T.max(zout))
        self.testcost=theano.function([self.x,self.y],self.cost)
        self.testgrad=theano.function([self.x,self.y],self.grads)
        print "finished model cost and gradient."