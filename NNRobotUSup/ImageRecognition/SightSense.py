import Camera as c
class SightSense:
    def __init__(self,isVideoStream):
       self.cam = c.Camera(isVideoStream)

    def getRoute(self):
        image = self.cam.getImage()
        self.cam.contours(image)
        #self.cam.show(image)
