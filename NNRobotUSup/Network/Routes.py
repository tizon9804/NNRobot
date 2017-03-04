import requests as req
import threading as t
class Network:

    def __init__(self):
        print "request created"

    def sendData(self,data,posData,logic,image,explore,cpu,memory):
        print logic,"#",len(posData),"#",image,"#",explore,"#",cpu,"#",memory
        #tPost = t.Thread(target=self.asycnSend(data,posData,logic,image,explore,cpu,memory))
        #tPost.start();

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
        print "Send Laser: "+r.text