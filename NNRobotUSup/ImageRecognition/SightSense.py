import Camera as c
class SightSense:
    def __init__(self,isVideoStream,Smemory):
       self.cam = c.Camera(isVideoStream,Smemory)
       self.Smemory = Smemory

    def getRoute(self):
        image = self.cam.getImage()
        self.cam.contours(image)
        #self.cam.show(image)
