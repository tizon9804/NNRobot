__author__ = 'Tizon'
import numpy as np
import cv2
class Online:
    def __init__(self,persistence,type,typeN,mind1,mind2,NNCostFunction,cap,init,elements,robot,actions):
         self.cap=cap
         self.init=init
         self.elements=elements
         self.robot=robot
         self.actions=actions
         self.mind1=mind1
         self.mind2=mind2
         win,wt,wout=persistence.state[type]
         self.costgrads=NNCostFunction.costGrads(self.mind1.thetain,self.mind1.hiddenTheta,self.mind1.thetaout)
         self.costgrads.setState(win,wt,wout)
         self.costgrads.createFunction()
         win,wt,wout=persistence.state[typeN]
         self.costgradsN=NNCostFunction.costGrads(self.mind2.thetain,self.mind2.hiddenTheta,self.mind2.thetaout)
         self.costgradsN.setState(win,wt,wout)
         self.costgradsN.createFunction()

    def startOnline(self):
            print "----------------------------------"
            print "STARTING ONLINE"
            print "----------------------------------"
            while(True):
              if self.cap.isOpened():
                  self.init.convImage()
                  #print "layer1 convolution",init.convImg.shape
                  self.init.takeframe()
                  if cv2.waitKey(1) & 0xFF == ord('q'):
                          break
                  X=self.init.convImg
                  #print "put all filtered images in a array"
                  #X = X.reshape(1,X.shape[1]*X.shape[2]*X.shape[3])
                  #X = X.reshape(1,X.shape[0]*X.shape[1])
                  print "----------------------------------------------"
                  #self.mind1.think(X,self.costgrads,self.elements)
                  #todo create report
                  print "----------------------------------------------"
              buffersensor = 0
              buffer = self.robot.getLaserBuffer()
              #bufferC = np.append(buffer,[self.mind1.pred])
              bufferC = np.append(buffer,[0])
              bufferC = np.reshape(bufferC,(1,bufferC.shape[0]))
              self.mind2.think(bufferC,self.costgradsN,self.actions)
              self.robot.setRobotAction(int(self.mind2.pred),self.mind2.proba)
            cv2.destroyAllWindows()
            self.robot.robot.disableMotors()

