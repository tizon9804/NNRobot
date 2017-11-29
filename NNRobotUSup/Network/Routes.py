import requests as req
import threading as t

class Network:
    def __init__(self, debug,bparm):
        self.debug = False
        self.bparm = bparm
        self.url = 'http://35.188.100.1:8080'
        #print "request created"

    def sendData(self, data, posData, logic, image, explore, cpu, memory,actualpredNav,actualprobNav):
        logmessage = str(logic) + "#" + str(len(posData)) + "#" + str(image) + "#" + str(
            explore) + "#" + str(cpu) + "#" + str(memory)
        self.logRoutes(str(logmessage))
        #tPost = t.Thread(target=self.asycnSend,args=(self.url+'/data', data, posData, logic, image, explore,cpu, memory,actualpredNav,actualprobNav))
        tPost = t.Thread(target=self.asycnSend(self.url + '/data', data, posData, logic, image, explore, cpu, memory, actualpredNav, actualprobNav))

        #tPost.start();

    def sendDataSight(self, cluster):
        self.logRoutes("Camera Data")
        #print len(cluster)
        #tPost = t.Thread(target=self.asycnSendSight,args=(self.url+'/dataSight', cluster))
        tPost = t.Thread(target=self.asycnSendSight(self.url + '/dataSight', cluster))
        #Post.start();

    def sendDataNnet(self,reportNN):
        self.logRoutes("NNET Data")
        # print len(cluster)
        tPost = t.Thread(target=self.asycnSendNnet,args=(self.url+'/dataNnet', reportNN))
        tPost = t.Thread(target=self.asycnSendNnet(self.url + '/dataNnet', reportNN))
        #tPost.start();

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
            if not r.status_code==200:
                print("error routes nnet: " + r.text)
                self.bparm.logicLife = False
                self.bparm.exploreLife = False
                self.bparm.senseLife = False
        except Exception as ex:
            print("error routes nnet: " + str(ex))
            self.bparm.logicLife = False
            self.bparm.exploreLife = False
            self.bparm.senseLife = False
            #print "Cannot send message to Node : ",str(ex)


    def asycnSendSight(self, url, cluster):
        try:
            r = req.post(url, data={
                'cluster': [cluster]
            })
            self.logRoutes("Send sight: " + r.text)
            if not r.status_code == 200:
                print("error routes nnet: " + r.text)
                self.bparm.logicLife = False
                self.bparm.exploreLife = False
                self.bparm.senseLife = False
        except Exception as ex:
            print("error routes nnet: " + r.text)
            self.bparm.logicLife = False
            self.bparm.exploreLife = False
            self.bparm.senseLife = False
            #print "Cannot send message to Node : ",str(ex)

    def asycnSendNnet(self, url, reportNN):
        try:
            r = req.post(url, data=reportNN)
            self.logRoutes("Send nnet: " + r.text)
            if not r.status_code == 200:
                print("error routes nnet: " +r.text)
                self.bparm.logicLife = False
                self.bparm.exploreLife = False
                self.bparm.senseLife = False
        except Exception as ex:
            print("error routes nnet: " + str(ex))
            self.bparm.logicLife = False
            self.bparm.exploreLife = False
            self.bparm.senseLife = False
            #print "Cannot send message to Node : ", str(ex)

    def logRoutes(self,message):
        if self.debug:
            print message





