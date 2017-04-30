import NNRobotUSup.Entities.Conscience as Con
import numpy as np
from Libraries.NNET import NNCostFunction as nncost, NeuralNetwork as NN, Think, Train as train
import cv2
import Libraries.Persistence.TargetManager as T
import threading

class LongTerm:
    def __init__(self,persistence):
        self.consciences = []
        self.id = 0
        self.bestWayO = np.array([])
        self.bestWay = np.array([])
        self.persistence = persistence # type: T.targetManager
        self.isTraining = False
        self.accuracyExpected = .98
        self.maxIter = 1000
        self.maxNoCostIter = 700
        self.lambdaNN = 0
        self.numEleToTrain = 10
        self.path = r'../../VaNN/public/stream'


    def createConscience(self, name, inputSize, numHidLayer, hidLayerSize, outputSize):
        input_layer_size = inputSize
        num_hidden_layer = numHidLayer
        hidden_layer_size = hidLayerSize
        num_output_Layers = outputSize
        NNGen = NN.CNNET(name,
                         input_layer_size,
                         num_hidden_layer,
                         hidden_layer_size,
                         num_output_Layers)
        mind = Think.assemble([], NNGen.brain,
                              input_layer_size, num_hidden_layer,
                              hidden_layer_size, num_output_Layers)
        self.persistence.loadNN(name)
        newCons = Con.Conscience(self.id, name, mind,self.persistence)
        self.id += 1
        self.consciences.append(newCons)

    def trainConscience(self,nameCons,data):
        for c in self.consciences:
            if c.name == nameCons:
                self.conscience = c  # type: Con.Conscience
                self.addDataToTrain(data,0)
                numbad = np.nonzero(self.conscience.y)[0].shape[0]
                total = self.conscience.y.shape[0]
                numbest = total - numbad
                print numbest, "best Y"
                if numbest % self.numEleToTrain == 0 and not self.isTraining:
                    self.lambdaNN = float(1.0/(self.conscience.elements.shape[0]*5))
                    self.isTraining = True
                    tTrain = threading.Thread(target=self.trainNN,args=(self.lambdaNN,self.maxIter,self.accuracyExpected,self.maxNoCostIter,self.persistence,self.conscience),name="NNET")
                    tTrain.start()
                    print "continue..."



    def trainNN(self,lambdaNN,maxIter,accuracy,maxNoCost,persistence,conscience):
        print threading.currentThread().getName(), ' training launched'
        self.trainMind = train.config(lambdaNN, maxIter, persistence,conscience.name, accuracy, maxNoCost)
        self.trainMind.train(conscience.mind, conscience.elements, conscience.y)
        threading._sleep(5)
        self.isTraining = False


    def addDataToTrain(self,data,position):
         print "all",self.conscience.elements.shape
         print "new",data.shape
         self.conscience.y = np.append(self.conscience.y, int(position))
         if self.conscience.elements.shape[0]==0:
             self.conscience.elements = data
         else:
             self.conscience.elements = np.vstack([self.conscience.elements,data.flatten()])


    def updateConscience(self):
        todo = True

    def lookForConscience(self,conscienceNameExp):
        for c in self.consciences:
            if c.name == conscienceNameExp:
                self.conscience = c
                return [True,c]
        return [False,0]
    def think(self,nameCons,data):
        for c in self.consciences:
            if c.name == nameCons:
                conscience = c  # type: Con.Conscience
                conscience.initNN()
                if conscience.isInitNN:
                    mind = conscience.mind  # type: Think.assemble
                    conscience.prediction,conscience.probability,zin = mind.think(data,conscience.costgrads)
                    #print zin.shape
                    #img = conscience.win.T[0][1:]
                    img = zin[0][1:]
                    img = np.reshape(img,self.bestWayO.shape)
                    mini = np.min(img)
                    maxi = np.max(img)
                    img =((img - mini) / (maxi - mini)) * (255);
                    cv2.imwrite(self.path + '/image_stream_nnet.jpg', img)

    def newImage(self,img):
        im = np.asarray(img, dtype='float32') / 256 # is important divide 256 to correct train nnet
        gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        self.bestWayO = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.bestWay = np.reshape(gray_image, (1, gray_image.shape[0] * gray_image.shape[1]))


