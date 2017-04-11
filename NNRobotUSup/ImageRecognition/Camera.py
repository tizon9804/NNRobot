# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera


import NNRobotUSup.Network.ServerVideoStream as server
import time
import cv2
import numpy as np
import io
import NNRobotUSup.Network.Routes as ro
import NNRobotUSup.Entities.Item as I

class Camera:
    def __init__(self,isVideoStream):
        self.debugNetwork = False
        self.net = ro.Network(self.debugNetwork)
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
            #camera.iso = 800
            #camera.image_effect = 'emboss'
            #camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2017 GSC'
            self.rawCapture = PiRGBArray(camera)
            # allow the camera to warmup
            #camera.start_preview()
            time.sleep(5)
            self.camera = camera

    def getImage(self):
        if self.isVideoStream:
            img = self.netCapture()
        else:
            img = self.raspCapture()
        return img

    def raspCapture(self):
        # capture frames from the camera
        #stream = io.BytesIO()
        self.camera.capture(self.rawCapture, "bgr", use_video_port=True)
        # print 'Captured image: ', self.rawCapture.array.shape
        #stream.seek(0)
        #data = np.fromstring(stream.read(),dtype=np.uint8)
        image = self.rawCapture.array
        #print data
        #image = cv2.imdecode(image, 1)
        #cv2.imshow("Frame", image)
        #key = cv2.waitKey(1) & 0xFF
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



