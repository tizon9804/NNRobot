import socket
import pickle
import numpy as np
import time
class RobotServerStream:
    def __init__(self,bparm):
        # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
        # all interfaces)
        self.bparm = bparm
        self.isRobotActive = False

    def acceptRobot(self):
        print "open sockets port 8001"
        self.isRobotActive = False
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8001))
        print "listening ROBOT"
        self.server_socket.listen(0)
        print  "Accept a single connection ROBOT"
        self.connection,self.addressR = self.server_socket.accept()
        waiting=True
        while(waiting):
            print '#################### Waiting Robot...########################'
            data = self.getData()
            if data == 'raspChappie':
                print data
                self.setData('HiRasp')
                self.getData()
                waiting = False
                self.isRobotActive = True
                print '####################Started Robot...########################'

    def getData(self):
        try:
            connection = self.connection
            data = connection.recv(1024).decode()
            return data
        except Exception as ex:
            print "Network: finalizo streaming: " + str(ex)
            self.isRobotActive = False
            self.bparm.logicLife = False
            self.bparm.exploreLife =False
            self.bparm.senseLife = False
            self.connection.close()
            self.server_socket.close()
            return '#############################################################'

    def setData(self,data):
        try:
            self.connection.send(b''+str(data))
        except Exception,ex:
            print "Robot Error: ",str(ex)
            self.isRobotActive = False
            self.bparm.logicLife = False
            self.bparm.exploreLife =False
            self.bparm.senseLife=False
            self.connection.close()
            self.server_socket.close()

    def getClosestDistance(self,x,xend):
        try:
            time.sleep(2)
            data = 'getClosestDistance:'+str(x)+':'+ str(xend)
            self.setData(data)
            data = []
            while True:
                packet = self.connection.recv()
                print "packet"
                print len(packet)                
                if not packet: break
                data.append(packet)
                print "pre daata"
                print len(data)
            print "data#####################"
            print len(data)           
            lmoves = pickle.loads(b"".join(data))
            return lmoves
        except Exception,ex:
            return []


    def isHeadingDone(self):
        time.sleep(1)
        data = 'isHeadingDone'
        self.setData(data)
        return bool(self.getData())


    def rotate(self,angle):
        time.sleep(1)
        data = 'rotate:' + str(angle)
        self.setData(data)
        self.getData()

    def rotateSecure(self,angle):
        time.sleep(1)
        data = 'rotateSecure:' + str(angle)
        self.setData(data)
        self.getData()

    def restartHeading(self):
        time.sleep(1)
        data = 'restartHeading'
        self.setData(data)
        self.getData()

    def getTh(self):
        time.sleep(1)
        data = 'getTh'
        self.setData(data)
        return float(self.getData())

    def getClosesFrontDistance(self):
        try:
            time.sleep(1)
            data = 'getClosestFrontDistance'
            self.setData(data)
            closest= float(self.getData())
            return closest
        except Exception, ex:
            print "Falla: intentando enviar getClosestFrontDistance",str(ex)

    def move(self,dist):
        time.sleep(1)
        data = 'move:' + str(dist)
        self.setData(data)
        self.getData()

    def getLaserBuffer(self):                    
        data = 'getLaserBuffer'
        print data
        self.setData(data)
        data = []
        print "enter while true"
        while True:
            print "looping"
            packet = self.connection.recv()
            print "packet"
            print len(packet)                
            if not packet: break
            data.append(packet)
            print "pre daata"
            print len(data)
        print "data#####################"
        print len(data)
        data_arr,posData = pickle.loads(b"".join(data))
        return np.array(data_arr),posData
       

    def getMaxReadings(self):
        data = 'getMaxReadings'
        self.setData(data)
        return int(self.getData())

    def getMaxDistance(self):
        data = 'getMaxDistance'
        self.setData(data)
        return int(self.getData())

