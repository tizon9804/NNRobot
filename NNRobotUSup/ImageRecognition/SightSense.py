import Camera as c
import ImageProcessing as IM
class SightSense:
    def __init__(self,isVideoStream,Smemory,Lmemory,ftpSender,bparm):
       self.cam = c.Camera(isVideoStream,bparm)
       self.IMprocess = IM.IMprocess(Smemory,Lmemory,ftpSender)


    def see(self):
        image = self.cam.getImage()
        self.IMprocess.contours(image)
