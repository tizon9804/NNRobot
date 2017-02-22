import Camera as c
class SightSense:
    def __init__(self):
       self.cam = c.Camera()

    def getRoute(self):
        self.cam.getImage()