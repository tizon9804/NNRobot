__author__ = 'Tizon'
import numpy as np
import theano
import time
from Libraries.NNET import NNCostFunction, Think


class config:
    def __init__(self, lamb, iterations, persistence, nameCons,secure,maxIterNoMinimize):
        self.persistence = persistence
        self.lamb = lamb
        self.iterations = iterations
        self.type = nameCons
        self.secure = secure
        self.maxIter = maxIterNoMinimize
        self.X = np.array([])
        self.y = np.array([])
        self.reportCost = np.array([])
        self.reportSecure = np.array([])
        self.i=0
        self.j=0

    def train(self, mind1,x,y):
        self.X=x
        self.y=y
        mind1 = mind1 # type: Think.assemble
        num_output_Layer = mind1.thetaout.shape[0]
        print "inputs", self.X.shape
        print "outputs", self.y.shape
        print "output layer", num_output_Layer
        # convert y in a vector of dimensions 1xnum_outputs with values 1 and 0
        # print "element to train ",self.elements[int(self.position)]
        Xb = np.ones((self.X.shape[0], self.X.shape[1] + 1), dtype=np.float32)
        Xb[:, 1:] = self.X.astype(np.float32)
        costgrads = NNCostFunction.costGrads(mind1.thetain, mind1.hiddenTheta, mind1.thetaout)
        if self.persistence.NNLoaded[self.type]:
            print "use NN saved", self.type
            win, wt, wout = self.persistence.state[self.type]
            costgrads.setState(win, wt, wout)
        else:
            print "use New NN"
        costgrads.createFunction()
        ##determine the inicial accuracy
        self.accuracyF(Xb, costgrads)
        ##----------------------------
        vecy = np.array(())
        print self.y
        for ye in self.y:
            vy = np.arange(0, num_output_Layer)
            vy = (vy == int(ye))
            vy = vy.astype(np.int32)
            if vecy.shape[0] == 0:
                vecy = np.vstack([vy])
            else:
                vecy = np.vstack([vecy, vy])
        updates = [
            (param_i, param_i - self.lamb * grad_i)
            for param_i, grad_i in zip(costgrads.thetas, costgrads.grads)]
        train = theano.function(inputs=[costgrads.x, costgrads.y],
                                outputs=[costgrads.cost, costgrads.max, costgrads.maxp],
                                updates=updates,
                                mode='FAST_RUN')
        t0 = time.time()
        try:
            secureAct = 0
            cont = 0
            self.reportCost = np.array(())
            self.reportSecure = np.array(())
            self.i = 0
            self.j = 0
            for i in range(self.iterations):
                secure = 0
                promcost = 0
                for j in range(vecy.shape[0]):
                    cost, pred, prob = train(Xb[j], vecy[j])
                    secure += prob
                    promcost += cost
                secure = secure / vecy.shape[0]
                promcost = promcost / vecy.shape[0]
                self.reportCost = np.append(self.reportCost, [promcost])
                self.reportSecure = np.append(self.reportSecure, [secure])
                self.i = i
                self.j = j
                print "#", i + 1, "/", self.iterations, "secure", secure * 100, "final cost->", cost, "vector to train", \
                    vecy[j],"lamda",str(self.lamb)," element predicted->", int(pred), ":probability-> ", (
                    prob * 100), "%"  # ,"\r",
                # the way to stop learning
                if (secure) > self.secure:
                    print "#", i + 1, "/", self.iterations, "#", j, "Secure in a ", secure * 100, "%"
                    break
                elif round(secure, 3) == round(secureAct, 3):
                    print "warning!! ", round(secure, 3), " ## ", round(secureAct, 3)
                    cont += 1
                else:
                    cont = 0
                secureAct = secure
                if cont >= self.maxIter:
                    print "stop because do not minimize any more"
                    break

        except Exception, e:
            print str(e)
        t1 = time.time()
        print("Looping %d times took %f seconds" % (i, t1 - t0))
        gpu = False
        for x in train.maker.fgraph.toposort():
            if str(type(x.op).__name__).startswith("Gpu"):
                gpu = True
                print "used GPU"
                break
        if not gpu:
            print "used cpu"

        self.persistence.saveNN(self.type, costgrads.getState())
        if not self.persistence.loadNN(self.type):
            print "unstable consciousness"
        ##determine the Final accuracy
        self.accuracyF(Xb, costgrads)

    def accuracyF(self, Xb, costgrads):
        self.pred = np.array(())
        self.accuracyProbability = np.array(())
        for inp in range(Xb.shape[0]):
            self.pred = np.append(self.pred, costgrads.maxFunction(Xb[inp]))
            self.accuracyProbability = np.append(self.accuracyProbability, costgrads.maxpFunction(Xb[inp]))
        self.accuracy = np.mean(self.pred == np.asarray(self.y)) * 100
        self.accuracyProbability = np.mean(self.accuracyProbability) * 0.5
        print "element predicted", self.pred
        print "element expected", self.y
        print "accuracy is: ", self.accuracy, "%"
        print "probabilities of the accuracy ", self.accuracyProbability, "%"

