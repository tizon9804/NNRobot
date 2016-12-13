__author__ = 'Tizon'
import cPickle
import numpy as np
class targetManager:

    def __init__(self):
        try:
            self.NNLoaded={}
            self.DataLoaded=False
            self.DataSensorLoaded=False
            self.state={}
        except :
            print "New Training..."
            self.trainingLoad = False

    def saveNN(self,name,costgrads):
        with open('data/'+str(name)+'.pkl', 'w') as f:
             cPickle.dump(costgrads, f)
        print "NN ",name," saved..."

    def saveElements(self,elements):
        with open('data/'+'elements.pkl', 'w') as f:
             cPickle.dump(elements, f)
        print "elements saved..."
    def saveActions(self,elements):
        with open('data/'+'actions.pkl', 'w') as f:
             cPickle.dump(elements, f)
        print "elements saved..."

    def saveDataSet(self,data):
        with open('data/'+'dataSet.pkl', 'w') as f:
             cPickle.dump(data, f)
        print "inputs X y saved..."
    def saveDataSensor(self,data):
        with open('data/'+'dataSensor.pkl', 'w') as f:
             cPickle.dump(data, f)
        print "inputs X y saved..."

    def loadNN(self,name):
        try:
            print "trying to load the NN ",name
            self.state[name] = cPickle.load(open('data/'+str(name)+'.pkl'))
            self.NNLoaded[name]=True
            print "NN ",name," Loaded..."
            return True
        except Exception,e:
            print "error ",str(e)
            print "New NN ", name,"..."
            self.NNLoaded[name]=False
            return False

    def loadElements(self):
       try:
           self.elements = cPickle.load(open('data/elements.pkl'))
           elements = self.elements
       except:
            elements = {'New': "Create Element"}
            for i in range(100):
                elements[i] = "default"+str(i)
       return elements

    def loadActions(self):
        actions = {}
        actions[0] = "left"
        actions[1] = "center"
        actions[2] = "right"
        return actions

    def loadDataSet(self):
        try:
            self.dataset = cPickle.load(open('data/'+'dataSet.pkl'))
            self.DataLoaded = True
        except Exception,e:
            print str(e),"no data"
        return self.DataLoaded

    def joinDataSet(self):
        try:
            self.dataset = cPickle.load(open('data/'+'dataSet.pkl'))
            print "data2"
            self.dataset2 = cPickle.load(open('data/'+'dataSet2.pkl'))
            x,y=self.dataset
            x1,y1=self.dataset2
            print "joinx",x.shape
            print "joiny",y.shape
            print "joinx1",x1.shape
            print "joiny1",y1.shape
            x=np.vstack([x,x1])
            y=np.append(y,(y1))
            print "joinnewx",x.shape
            print "joinnewy",y.shape
            self.dataset=[x,y]
            self.DataLoaded = True
        except Exception,e:
            print str(e),"no data"
        return self.DataLoaded

    def loadDataSensor(self):
        try:
            self.DataSensorLoaded = False
            self.datasensor = cPickle.load(open('data/'+'dataSensor.pkl'))
            self.DataSensorLoaded = True
        except Exception,e:
            print str(e),"no data"
            return self.DataSensorLoaded
        return self.DataSensorLoaded
    def filterDataSensor(self):
        #try:
            self.datasensor = cPickle.load(open('data/'+'dataSensor.pkl'))
            x,y = self.datasensor
            print x.shape
            lenreading= x.shape[1]
            muestra=x.shape[0]
            if lenreading > 228:
                dif=int((lenreading-228)/2)
            xbuffer=np.zeros((muestra,229))
            for j in range(muestra):
                fbuffer=np.zeros(228)
                objeto=x[j,lenreading-1]
                for i in range(len(fbuffer)):
                    fbuffer[i]=x[j,i+dif]
                print j,'#',i,"Laser readings: ",(lenreading) ," Laser Filtered: ",len(fbuffer)
                xbuffer[j]=np.append(fbuffer,[objeto])
            x=xbuffer
            print x.shape
            print y.shape
            self.datasensor=[x,y]
            self.DataSensorLoaded = True
            with open('data/'+'dataSensorfilteredt.pkl', 'w') as f:
                cPickle.dump(self.datasensor, f)
        #except Exception,e:
            #print str(e),"no data"
            return self.DataSensorLoaded
