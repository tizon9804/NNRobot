import requests as req
import threading as t
class Network:

    def __init__(self,debug):
        self.debug = debug
        print "request created"

    def sendData(self,data,posData,logic,image,explore,cpu,memory):
        logmessage = str(logic) + "#" + str(len(posData)) + "#" + str(image) + "#" + str(explore) + "#" + str(cpu) + "#" + str(memory)
        self.logRoutes(str(logmessage))
        tPost = t.Thread(target=self.asycnSend('http://localhost:3000/data',data,posData,logic,image,explore,cpu,memory))
        tPost.start();

    def sendDataSight(self,posData):
        self.logRoutes("Camera Data")
        tPost = t.Thread(target=self.asycnSend('http://localhost:3000/data',[], posData, [], [], [], [], []))
        tPost.start();

    def asycnSend(self,url,data,posData,logic,image,explore,cpu,memory):
        r= req.post(url,data = {
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