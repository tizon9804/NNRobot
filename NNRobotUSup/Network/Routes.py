import requests as req
import threading as t

class Network:
    def __init__(self, debug):
        self.debug = debug
        #print "request created"

    def sendData(self, data, posData, logic, image, explore, cpu, memory):
        logmessage = str(logic) + "#" + str(len(posData)) + "#" + str(image) + "#" + str(
            explore) + "#" + str(cpu) + "#" + str(memory)
        self.logRoutes(str(logmessage))
        tPost = t.Thread(target=self.asycnSend,args=('http://localhost:3000/data', data, posData, logic, image, explore,cpu, memory))
        tPost.start();

    def sendDataSight(self, cluster):
        self.logRoutes("Camera Data")
        #print len(cluster)
        tPost = t.Thread(target=self.asycnSendSight,args=('http://localhost:3000/dataSight', cluster))
        tPost.start();

    def sendDataNnet(self,reportNN):
        self.logRoutes("NNET Data")
        # print len(cluster)
        tPost = t.Thread(target=self.asycnSendNnet,
                         args=('http://localhost:3000/dataNnet', reportNN))
        tPost.start();

    def asycnSend(self,url,data,posData,logic,image,explore,cpu,memory):
        try:
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
        except Exception as ex:
            print "Cannot send message to Node : ",str(ex)


    def asycnSendSight(self, url, cluster):
        try:
            r = req.post(url, data={
                'cluster': [cluster]
            })
            self.logRoutes("Send Laser: " + r.text)
        except Exception as ex:
            print "Cannot send message to Node : ",str(ex)

    def asycnSendNnet(self, url, reportNN):
        try:
            r = req.post(url, data=reportNN)
            self.logRoutes("Send Laser: " + r.text)
        except Exception as ex:
            print "Cannot send message to Node : ", str(ex)

    def logRoutes(self,message):
        if self.debug:
            print message





