import requests as req
import threading as t
class Network:

    def __init__(self,debug):
        self.debug = debug
        print "request created"

    def sendData(self,data,posData,logic,image,explore,cpu,memory):
        logmessage = str(logic) + "#" + str(len(posData)) + "#" + str(image) + "#" + str(explore) + "#" + str(cpu) + "#" + str(memory)
        self.logRoutes(str(logmessage))
        tPost = t.Thread(target=self.asycnSend(data,posData,logic,image,explore,cpu,memory))
        tPost.start();

    def asycnSend(self,data,posData,logic,image,explore,cpu,memory):
        r= req.post('http://localhost:3000/data',data = {
            'buffer':data,
            'bufferpos': [posData],
            'nlogic':logic,
            'nimage':image,
            'nexplore':explore,
            'cpu':cpu,
            'memory':memory
        })
        self.logRoutes("Send Laser: "+r.text)

    def logRoutes(self,message):
        if self.debug:
            print message