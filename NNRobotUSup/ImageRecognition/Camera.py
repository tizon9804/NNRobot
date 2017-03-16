# import the necessary packages
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import NNRobotUSup.Network.ServerVideoStream as server
import time
import cv2
import numpy as np

class Camera:
    def __init__(self,isVideoStream):
        self.image = []
        self.isVideoStream = isVideoStream
        if isVideoStream:
            self.server= server.VideStream()
        else:
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
            camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2017 GSC'
            self.rawCapture = PiRGBArray(camera)
            # allow the camera to warmup
            time.sleep(0.1)
            self.camera = camera

    def getImage(self):
        if self.isVideoStream:
            img = self.netCapture()
        else:
            img = self.raspCapture()
        return img

    def raspCapture(self):
        # capture frames from the camera
        self.camera.capture(self.rawCapture, "bgr")
        # print 'Captured image: ', self.rawCapture.array.shape
        image =  self.rawCapture.array
        # cv2.imshow("Frame", self.image)
        # key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        self.rawCapture.truncate(0)
        return image

    def netCapture(self):
        if self.server.isVideoActive:
            img =  self.server.getImage()
        else:
            img =  self.server.acceptVideo()
        return img

    def show(self,image):
        try:
            cv2.imshow("EYES",image)
            key = cv2.waitKey(1) & 0xFF
        except Exception as ex:
            print "SENSE: SHOW error ",str(ex)

    def contours(self,img):
        img2=img
        self.img = img
        self.imFilt = img
        self.gaussianBlur(False)
        self.gray(True)
        self.laplacian(True)
        self.gaussianBlur(True)
        self.convolution(True)
        self.medianBlur(False)
        self.bilateralFilter(False)
        self.medianBlur(True)
        self.bilateralFilter(True)
        self.cannyEdges(True)
        self.img = self.imFilt
        im2, contours, hierarchy = cv2.findContours(self.imFilt.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        for contour in contours:
            cnt = contour
            hull = cv2.convexHull(cnt)
            rect = cv2.minAreaRect(cnt)
            w,h=rect[1]
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            max = 320
            min = 50
            if w>=min and h>=min and w<=max and h<=max:
                #obtainPieceOfImage(rect,img2,i)
                cv2.drawContours(img, [box], -1, (114, 224, 150),2)
                cv2.drawContours(img, [hull], -1, (207, 252, 232), 1)
            i += 1
        cv2.imshow("Contours", img)
        cv2.waitKey(1)

    def obtainPieceOfImage(self,rect,img2,i):
        rotMatrix = cv2.getRotationMatrix2D(rect[0],rect[2],1.0)
        rotated = cv2.warpAffine(img2,rotMatrix,(640,480),cv2.INTER_CUBIC)
        w, h = rect[1]
        size = (int(w), int(h))
        newimg = cv2.getRectSubPix(rotated,size,rect[0])
        cv2.imshow("Contours"+str(i), newimg)
        cv2.waitKey(1)

    def gaussianBlur(self,show):
        self.img = self.imFilt
        self.imFilt = cv2.GaussianBlur(self.img, (7, 7), 0)
        if show:
            cv2.imshow("GaussianBlur", self.imFilt)
            cv2.waitKey(1)

    def gray(self,show):
        self.img = self.imFilt
        self.imFilt = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        if show:
            cv2.imshow("COLOR_BGR2GRAY", self.imFilt)
            cv2.waitKey(1)

    def laplacian(self,show):
        self.img = self.imFilt
        dst = cv2.Laplacian(self.img, ddepth=cv2.CV_16S,
                            scale=2, delta=200, ksize=5, borderType=cv2.BORDER_CONSTANT)
        self.imFilt = cv2.convertScaleAbs(dst)
        if show:
            cv2.imshow("Laplacian", self.imFilt)
            cv2.waitKey(1)

    def medianBlur(self,show):
        self.img = self.imFilt
        self.imFilt = cv2.medianBlur(self.img, 5)
        if show:
            cv2.imshow("medianBlur", self.imFilt)
            cv2.waitKey(1)

    def bilateralFilter(self,show):
        self.img = self.imFilt
        self.imFilt = cv2.bilateralFilter(self.img, 10, 17, 17)
        if show:
            cv2.imshow("bilateralFilter", self.imFilt)
            cv2.waitKey(1)

    def convolution(self,show):
        self.img = self.imFilt
        kernel = np.ones((5, 5), np.float32) / 25
        self.imFilt = cv2.filter2D(self.img, -1, kernel)
        if show:
            cv2.imshow("convolution", self.imFilt)
            cv2.waitKey(1)

    def cannyEdges(self,show):
        self.img = self.imFilt
        self.imFilt = cv2.Canny(self.img, 0, 50)
        if show:
            cv2.imshow("edges1", self.imFilt)
            cv2.waitKey(1)

