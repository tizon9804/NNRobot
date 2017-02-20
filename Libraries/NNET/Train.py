__author__ = 'Tizon'
import numpy as np
import theano
import threading
import time
import cv2
import matplotlib.pyplot as plt
from Libraries.NNET import NNCostFunction


class config:

    def __init__(self, elements, lamb, iterations, persistence, type):
        self.persistence = persistence
        self.lamb = lamb
        self.iterations = iterations
        self.X = np.array(())
        self.y = np.array(())
        self.elements = elements
        self.type = type
        element = ""

    def collectDataImg(self, cap, init):
        if self.persistence.loadDataSet():
            self.X, self.y = self.persistence.dataset
            print "data loaded"
            save = True
            while (cap.isOpened()):
                init.convImage()
                X = init.convImg
                # X = X.reshape(1,X.shape[1]*X.shape[2]*X.shape[3])
                # X = X.reshape(1,X.shape[0]*X.shape[1])
                thread = threading.Thread(target=init.drawImage("todo", init.img))
                thread.start()
                if cv2.waitKey(1) & 0xFF == ord('z'):
                    break
                self.addDataToTrain(X, y, position)
            cv2.destroyAllWindows()
            print "saving..."
        if save:
            self.persistence.saveElements(self.elements)
            self.persistence.saveDataSet([self.X, self.y])

    def addDataToTrain(self, x, y, position):
        self.position = int(position)
        print "all", self.X.shape
        print "new", x.shape
        if self.X.shape[0] == 0:
           self.X = x
        else:
          print "adding new data in the bucket"
          self.X = np.vstack([self.X, x.flatten()])
          self.y = np.append(self.y, int(position))

    def train(self, layer0params, layer1params, mind1, num_output_Layer):
        print "inputs", self.X.shape
        print "outputs", self.y.shape
        print "output layer", num_output_Layer
        m = self.X.shape[0]
        # convert y in a vector of dimensions 1xnum_outputs with values 1 and 0
        # print "element to train ",self.elements[int(self.position)]
        Xb = np.ones((self.X.shape[0], self.X.shape[1] + 1), dtype=np.float32)
        Xb[:, 1:] = self.X.astype(np.float32)
        print Xb.shape
        costgrads = NNCostFunction.costGrads(mind1.thetain, mind1.hiddenTheta, mind1.thetaout)
        if self.persistence.NNLoaded[self.type]:
            print "use NN saved", self.type
            win, wt, wout = self.persistence.state[self.type]
            costgrads.setState(win, wt, wout)
        else:
            print "use New NN"
        costgrads.createFunction()
        ##determine the inicial accuracy
        self.accuracy(Xb, costgrads)
        ##----------------------------
        vecy = np.array(())
        print self.y
        for ye in self.y:
            vy = np.arange(0, num_output_Layer)
            vy = (vy == int(ye))
            vy = vy.astype(np.int32)
            if vecy.shape[0] == 0:
                vecy = vy
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
            crec = 0
            reportcost = np.array(())
            reportsecure = np.array(())
            for i in range(self.iterations):
                secure = 0
                promcost = 0
                for j in range(vecy.shape[0]):
                    cost, pred, prob = train(Xb[j], vecy[j])
                    # print "#",i+1,"/",self.iterations,"#",j,"final cost->",cost,"vector to train",vecy[j]," element predicted->",int(pred),":",self.elements[int(pred)]," probability-> ",(prob*100),"%"#,"\r",
                    secure += prob
                    promcost += cost
                secure = secure / vecy.shape[0]
                promcost = promcost / vecy.shape[0]
                reportcost = np.append(reportcost, [promcost])
                reportsecure = np.append(reportsecure, [secure])

                print "#", i + 1, "/", self.iterations, "secure", secure * 100, "final cost->", cost, "vector to train", \
                    vecy[j], " element predicted->", int(pred), ":", self.elements[int(pred)], " probability-> ", (
                    prob * 100), "%"  # ,"\r",
                # the way to stop learning
                if (secure) > .97:
                    print "#", i + 1, "/", self.iterations, "#", j, "Secure in a ", secure * 100, "%"
                    break
                elif round(secure, 3) == round(secureAct, 3):
                    print "warning!! ", round(secure, 3), " ## ", round(secureAct, 3)
                    cont += 1
                else:
                    cont = 0
                secureAct = secure
                if cont >= 1000:
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
        self.pred = np.array(())
        self.accuracyProbability = np.array(())
        for inp in range(Xb.shape[0]):
            self.pred = np.append(self.pred, costgrads.maxFunction(Xb[inp]))
            self.accuracyProbability = np.append(self.accuracyProbability, costgrads.maxpFunction(Xb[inp]))
        self.accuracy = np.mean(self.pred == np.asarray(self.y)) * 100
        self.accuracyProbability = np.mean(self.accuracyProbability) * 100
        print "element predicted", self.pred
        print "element expected", self.y
        print "accuracy is: ", self.accuracy, "%"
        print "probabilities of the accuracy ", self.accuracyProbability, "%"
        plt.figure(1)
        plt.subplot(211)
        plt.plot(reportsecure)
        plt.subplot(212)
        plt.plot(reportcost)
        plt.show()

    def accuracy(self, Xb, costgrads):
        self.pred = np.array(())
        self.accuracyProbability = np.array(())
        for inp in range(Xb.shape[0]):
            self.pred = np.append(self.pred, costgrads.maxFunction(Xb[inp]))
            self.accuracyProbability = np.append(self.accuracyProbability, costgrads.maxpFunction(Xb[inp]))
        self.accuracy = np.mean(self.pred == np.asarray(self.y)) * 100
        self.accuracyProbability = np.mean(self.accuracyProbability) * 100
        print "element predicted", self.pred
        print "element expected", self.y
        print "accuracy is: ", self.accuracy, "%"
        print "probabilities of the accuracy ", self.accuracyProbability, "%"
