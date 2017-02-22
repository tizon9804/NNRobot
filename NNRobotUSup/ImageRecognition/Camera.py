# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from fractions import Fraction
import cv2

class Camera:
    def __init__(self):
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

    def getImage(self):
        # capture frames from the camera
        self.camera.capture(self.rawCapture,"bgr")
        #print 'Captured image: ', self.rawCapture.array.shape
        self.image = self.rawCapture.array
        #cv2.imshow("Frame", self.image)
        #key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        self.rawCapture.truncate(0)

