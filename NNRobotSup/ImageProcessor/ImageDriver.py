__author__ = 'Tizon'
import cv2
import ConvolutionLayer as c
import theano
from theano import tensor as T
import numpy as np

class ImgDriver(object):
    """Pool Layer of a convolutional network """

    def __init__(self):
        rng = np.random.RandomState(23455)
        self.cap = cv2.VideoCapture(0)
        input = T.tensor4(name='input')
        width=480
        height=640
        reductor=3
        pixeles=3
        num_filter=(4,6)
        poolsize=2
        self.layer0 = c.ConvPoolLayer(
                rng,
                input=input,
                image_shape=(1, pixeles, width, height),
                filter_shape=(num_filter[0],pixeles, reductor, reductor),
                poolsize=(poolsize,poolsize)
            )
        self.layer1 = c.ConvPoolLayer(
                rng,
                input=self.layer0.output,
                image_shape=(1, num_filter[0], (width-reductor+1)/poolsize,(height-reductor+1)/poolsize),
                filter_shape=(num_filter[1], num_filter[0], reductor, reductor),
                poolsize=(2,2)
            )
    def convImage(self):
        try:
           # if self.cap.isOpened():
            ret, frame = self.cap.read()
            #else:
             #            frame =  cv2.imread('test/chair.jpg')
            img = np.asarray(frame, dtype=np.float32)/256
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.img=img.astype(np.float32)
            #print img.shape
            #imgTranspose = img.transpose(2, 0, 1).reshape(1, 3, img.shape[0],img.shape[1])
            #conv0=self.layer0.filter(imgTranspose)
            #print "layer0 convolution",conv0.shape
            #conv1=self.layer1.filter(conv0)
            #self.convImg=np.reshape(conv1,(1,conv1.shape[1]*conv1.shape[2]*conv1.shape[3]))
            self.convImg=np.reshape(gray_image,(1,gray_image.shape[0]*gray_image.shape[1]))
        except Exception,e:
            self.img=np.zeros((640,480))
            self.convImg=np.reshape(self.img,(1,self.img.shape[0]*self.img.shape[1]))
            str(e)


    def takeframe(self):
        ret, frame = self.cap.read()
        # dimensions are (height, width, channel)
        img = np.asarray(frame, dtype='float32')/256
        # put image in 4D tensor of shape (1, 3, height, width)
        """ img_ = img.transpose(2, 0, 1).reshape(1, 3, 480,640)
        filtered_img0= self.layer0.filter(img_)
        image1 = filtered_img0[0, 0, :, :]
        image2 = filtered_img0[0, 1, :, :]
        image3 = filtered_img0[0, 2, :, :]
        image4 = filtered_img0[0, 3, :, :]
        filtered_img1= self.layer1.filter(filtered_img0)
        image11 = filtered_img1[0, 0, :, :]
        image12 = filtered_img1[0, 1, :, :]
        image13 = filtered_img1[0, 2, :, :]
        image14 = filtered_img1[0, 3, :, :]
        image15 = filtered_img1[0, 4, :, :]
        image16 = filtered_img1[0, 5, :, :]
        #print "size0",filtered_img1.shape
        l0= np.hstack((image1, image2, image3,image4))
        l1 = np.hstack((image11, image12, image13,image14,image15,image16))
        cv2.imshow('Layer0',l0)
        cv2.imshow('Layer1',l1)"""
        cv2.imshow('Original',img)
        #self.layer_input=image4

    def drawImage(self,name,image=np.arange(2)):
        cv2.imshow(name,image)
        cv2.waitKey(1)