# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

class Camera:
    def __init__(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 30
        self.camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2017 GSC'
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        # allow the camera to warmup
        time.sleep(0.1)
    def getImage(self):
        # capture frames from the camera
        self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        print('Captured %dx%d image' % (
        self.rawCapture.array.shape[1], self.rawCapture.array.shape[0]))
        # clear the stream in preparation for the next frame
        self.rawCapture.truncate(0)
