import NNRobotUSup.ImageRecognition.Camera as c

cam = c.Camera(False)

while(True):
    cam.raspCapture()