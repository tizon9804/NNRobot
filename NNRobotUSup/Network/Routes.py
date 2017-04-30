import requests as req
import threading as t

class Network:
    def __init__(self, debug):
        self.debug = debug
        self.url = 'http://104.198.238.71'
        #print "request created"

    def sendData(self, data, posData, logic, image, explore, cpu, memory,actualpredNav,actualprobNav):
        logmessage = str(logic) + "#" + str(len(posData)) + "#" + str(image) + "#" + str(
            explore) + "#" + str(cpu) + "#" + str(memory)
        self.logRoutes(str(logmessage))
        tPost = t.Thread(target=self.asycnSend,args=(self.url+'/data', data, posData, logic, image, explore,cpu, memory,actualpredNav,actualprobNav))
        tPost.start();

    def sendDataSight(self, cluster):
        self.logRoutes("Camera Data")
        #print len(cluster)
        tPost = t.Thread(target=self.asycnSendSight,args=(self.url+'/dataSight', cluster))
        tPost.start();

    def sendDataNnet(self,reportNN):
        self.logRoutes("NNET Data")
        # print len(cluster)
        tPost = t.Thread(target=self.asycnSendNnet,
                         args=(self.url+'/dataNnet', reportNN))
        tPost.start();

    def asycnSend(self,url,data,posData,logic,image,explore,cpu,memory,prednav,probnav):
        try:
            r= req.post(url,data = {
                'buffer':data,
                'bufferpos': [posData],
                'nlogic':logic,
                'nimage':image,
                'nexplore':explore,
                'cpu':cpu,
                'memory':memory,
                'predNav':prednav,
                'probNav':probnav
            })
            self.logRoutes("Send Laser: "+r.text)
        except Exception as ex:
            d=0
            #print "Cannot send message to Node : ",str(ex)


    def asycnSendSight(self, url, cluster):
        try:
            r = req.post(url, data={
                'cluster': [cluster]
            })
            self.logRoutes("Send Laser: " + r.text)
        except Exception as ex:
            d=0
            #print "Cannot send message to Node : ",str(ex)

    def asycnSendNnet(self, url, reportNN):
        try:
            r = req.post(url, data=reportNN)
            self.logRoutes("Send Laser: " + r.text)
        except Exception as ex:
            d=0
            #print "Cannot send message to Node : ", str(ex)

    def logRoutes(self,message):
        if self.debug:
            print message





