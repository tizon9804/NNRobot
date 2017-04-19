__author__ = 'Tizon'
import cv2
import TargetManager as target
import numpy as np
from NeuralManager.nnet import NNCostFunction
from nnet import Think
from Mode import Training,Online
print "------------------------------------------------------"
print("Waking up Chappie!!")
print "------------------------------------------------------"
print ""
print "------------------------------------------------------"
print "------------------------------------------------------"
print "                     ---------"
print "                     ---------"
print "                     ---------"
print "                     ---------"
print "                     ---------"
print "                     ---------"
print "                     ---------"
print "                     ---------"
print "                     ---------"
print "                     ---------"
print "                     ---------"
print "                     ---------"
print "------------------------------------------------------"
print "------------------------------------------------------"
#-------------------------------------------------------------------------
#initialize targetManager
#-------------------------------------------------------------------------
print("initializing target manager..")
persistence=target.targetManager()
#-------------------------------------------------------------------------
#initialize elements
#-------------------------------------------------------------------------
print("initializing elements..")
elements=persistence.loadElements()
actions=persistence.loadActions()
#-------------------------------------------------------------------------
#initialize imagedriver
#-------------------------------------------------------------------------
print("initializing imagedriver..")
from ImageProcessor import ImageDriver as imd
init=imd.ImgDriver()
cap=init.cap
#-------------------------------------------------------------------------
#initialize robotDriver
#-------------------------------------------------------------------------
print("initializing robotdriver..")
#from RobotSystem import Robot
#robot=Robot.RobotDriver()

#-------------------------------------------------------------------------
#initialize neuralnetwork
#-------------------------------------------------------------------------
print("initializing neuralnetwork..")
from nnet import NeuralNetwork as NN
type='SightConscience'
init.convImage()
print init.convImg.shape
input_layer_size = init.convImg.shape[1]
num_hidden_layer = 3
hidden_layer_size = 100
num_output_Layers = 5
NNSight=NN.CNNET(type,
                      input_layer_size,
                      num_hidden_layer,
                      hidden_layer_size,
                      num_output_Layers)
mind1 = Think.assemble([],NNSight.brain,
            input_layer_size,num_hidden_layer,
            hidden_layer_size,num_output_Layers)

persistence.loadNN(type)

typeN='NavigatonConscience'
input_layer_size = 229
num_hidden_layer = 3
hidden_layer_size = 25
num_output_Layer = 3
NNNavigation=NN.CNNET(typeN,
                      input_layer_size,
                      num_hidden_layer,
                      hidden_layer_size,
                      num_output_Layer)
mind2 = Think.assemble([],NNNavigation.brain,
            input_layer_size,num_hidden_layer,
            hidden_layer_size,num_output_Layer)

persistence.loadNN(typeN)

#-------------------------------------------------------------------------
#Mode
#-------------------------------------------------------------------------
while True:
    mode=raw_input("please select a mode(0:online,1:training):")
    if mode=='1':
        #-------------------------------------------------------------------------
        #initialize training
        #-------------------------------------------------------------------------
        lamb = 0.001
        iterations = 3000

        ty=raw_input("please select a type(0:sight,1:navigation):")
        if ty =='0':
            print("initializing training sight..")
            training = Training.config(elements,lamb,iterations,persistence,type)
            training.elements = persistence.loadElements()
            elements = training.elements
            training.collectDataImg(cap,init)
            training.train(init.layer0.params, init.layer1.params, mind1,num_output_Layers)
            elements=training.elements
        elif ty =='1':
            training = Training.config(actions,lamb,iterations,persistence,typeN)
            training.elements = elements
            training.collectDataSensor(robot,elements)
            training.train(init.layer0.params, init.layer1.params, mind2,num_output_Layer)

    elif mode == '0':
        #-------------------------------------------------------------------------
        #initialize online
        #-------------------------------------------------------------------------
       print("initializing online..")
       if persistence.NNLoaded[type] and  persistence.NNLoaded[typeN]:
           on=Online.Online(persistence,type,typeN,mind1,mind2,NNCostFunction,cap,init,elements,robot,actions)
           on.startOnline()
       else:
            print "first you have to train me!!"
    else:
        print("Chappie is sleeping..")
        break
#-------------------------------------------------------------------------#-------------------------------------------------------------------------#-------------------------------------------------------------------------
#-------------------------------------------------------------------------#-------------------------------------------------------------------------#-------------------------------------------------------------------------
#-------------------------------------------------------------------------#-------------------------------------------------------------------------#-------------------------------------------------------------------------
#-------------------------------------------------------------------------#-------------------------------------------------------------------------#-------------------------------------------------------------------------
#robot.closeRobot()
cap.release()
cv2.destroyAllWindows()
print("Chappie down!!")






