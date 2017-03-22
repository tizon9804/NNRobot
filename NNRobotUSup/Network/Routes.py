import requests as req
import threading as t
class Network:

    def __init__(self,debug):
        self.debug = debug
        print "request created"

    def sendData(self,data,posData,logic,image,explore,cpu,memory):
        logmessage = str(logic) + "#" + str(len(posData)) + "#" + str(image) + "#" + str(explore) + "#" + str(cpu) + "#" + str(memory)
        self.logRoutes(str(logmessage))
        tPost = t.Thread(target=self.asycnSend('http://190.158.131.76:3000/data',data,posData,logic,image,explore,cpu,memory))
        tPost.start();

    def sendDataSight(self,moments,cluster1,cluster2,center):
        self.logRoutes("Camera Data")
        tPost = t.Thread(target=self.asycnSend('http://190.158.131.76:3000/dataSigth',moments, cluster1,cluster2,center))
        tPost.start();

    def asycnSend(self,url,moments,cluster1,cluster2,center):
        r= req.post(url,data = {
            'moments':moments,
            'cluster1': cluster1,
            'cluster2':cluster2,
            'center':center
        })
        self.logRoutes("Send Laser: "+r.text)



    def logRoutes(self,message):
        if self.debug:
            print message