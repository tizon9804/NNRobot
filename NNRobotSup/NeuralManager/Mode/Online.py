__author__ = 'Tizon'
import numpy as np
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import time
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
            # initialize the camera and grab a reference to the raw camera capture
            camera = PiCamera()
            camera.resolution = (640, 480)
            camera.framerate = 30
            #dark
            #camera.framerate = Fraction(1, 6)
            #camera.shutter_speed = 6#000000
            #camera.exposure_mode = 'off'
            camera.iso = 800
            #camera.image_effect = 'emboss'
            #
            camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2017 GSC'
            self.rawCapture = PiRGBArray(camera)
            # allow the camera to warmup
            time.sleep(0.1)
            self.camera = camera
            
            
            while(True):
              if True:
                  # capture frames from the camera
                  self.camera.capture(self.rawCapture,"bgr")
                  #print 'Captured image: ', self.rawCapture.array.shape
                  self.image = self.rawCapture.array
                  cv2.imshow("Frame", self.image)
                  #key = cv2.waitKey(1) & 0xFF
                  # clear the stream in preparation for the next frame
                  img = np.asarray(self.image, dtype=np.float32)/256
                  self.img=img.astype(np.float32)
                  gray_image = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
                  self.img=img.astype(np.float32)
                  self.convImg=np.reshape(gray_image,(1,gray_image.shape[0]*gray_image.shape[1]))
               
                  #print "layer1 convolution",init.convImg.shape
                  
                  if cv2.waitKey(1) & 0xFF == ord('q'):
                          break
                  X=self.convImg
                  self.rawCapture.truncate(0)
                  print X.shape
                  print "put all filtered images in a array"
                  #X = X.reshape(1,X.shape[1]*X.shape[2]*X.shape[3])
                  #X = X.reshape(1,X.shape[0]*X.shape[1])
                  print "----------------------------------------------"
                  self.mind1.think(X,self.costgrads,self.elements)
                  #todo create report
                  print "----------------------------------------------"
              buffersensor = 0
              buffer = self.robot.getLaserBuffer()
              bufferC = np.append(buffer,[self.mind1.pred])
              bufferC = np.append(buffer,[0])
              bufferC = np.reshape(bufferC,(1,bufferC.shape[0]))
              self.mind2.think(bufferC,self.costgradsN,self.actions)
              self.robot.setRobotAction(int(self.mind2.pred),self.mind2.proba)
            cv2.destroyAllWindows()
            #self.robot.robot.disableMotors()

