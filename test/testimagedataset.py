
import cPickle
import numpy as np
import cv2
import threading

class imageExctract:

    def __init__(self):
        dataset = cPickle.load(open('../data/'+'dataSet.pkl'))
        print "data2"
        x,y=dataset
        print "joinx",x.shape
        print "joiny",y.shape
        i=0
        while(i<x.shape[0]):
            img = np.reshape(x[i],(480,640))
            thread = threading.Thread(target=self.drawImage("w",img))
            thread.start()
            if cv2.waitKey(1) & 0xFF == ord('z'):
                break
            y = raw_input()
            i+=1

    def drawImage(self,name,image=np.arange(2)):
            cv2.imshow(name,image)
            cv2.waitKey(1)