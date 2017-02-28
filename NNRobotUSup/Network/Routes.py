import requests as req

class Network:

    def __init__(self):
        print "request created"

    def sendLaserData(self,data):
        r= req.post('http://localhost:1337/laser',data = {'buffer':data})
        print "Send Laser: "+r.text