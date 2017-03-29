import Camera as c
import ImageProcessing as IM
class SightSense:
    def __init__(self,isVideoStream,Smemory,Lmemory):
       self.cam = c.Camera(isVideoStream)
       self.IMprocess = IM.IMprocess(Smemory,Lmemory)


    def see(self):
        image = self.cam.getImage()
        self.IMprocess.contours(image)
