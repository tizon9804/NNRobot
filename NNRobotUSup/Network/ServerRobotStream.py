import socket
import pickle
import numpy as np
import time
import struct
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
            data = self.getData().decode()
            if data == 'raspChappie':
                print data
                self.setData('HiRasp')
                self.getData().decode()
                waiting = False
                self.isRobotActive = True
                print '####################Started Robot...########################'

    def getData(self):
        try:
            dataLen = self.recvall(4)
            if not dataLen:
                return None
            msglen = struct.unpack('>I',dataLen)[0]
            print msglen
            data = self.recvall(msglen)
            return data
        except Exception as ex:
            print "Network: finalizo streaming: " + str(ex)
            self.isRobotActive = False
            self.bparm.logicLife = False
            self.bparm.exploreLife =False
            self.bparm.senseLife = False
            self.connection.close()
            self.server_socket.close()
            return None
        
    def recvall(n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = self.connection.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
    
    def setData(self,data):
        try:
            msg = struct.pack('>I',len(data) + data)
            self.connection.sendall(msg)
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
            data = self.getData()           
            lmoves = pickle.loads(b"".join(data))
            return lmoves
        except Exception,ex:
            return []


    def isHeadingDone(self):
        time.sleep(1)
        data = 'isHeadingDone'
        self.setData(data)
        return bool(self.getData().decode())


    def rotate(self,angle):
        time.sleep(1)
        data = 'rotate:' + str(angle)
        self.setData(data)
        self.getData().decode()

    def rotateSecure(self,angle):
        time.sleep(1)
        data = 'rotateSecure:' + str(angle)
        self.setData(data)
        self.getData().decode()

    def restartHeading(self):
        time.sleep(1)
        data = 'restartHeading'
        self.setData(data)
        self.getData().decode()

    def getTh(self):
        time.sleep(1)
        data = 'getTh'
        self.setData(data)
        return float(self.getData().decode())

    def getClosesFrontDistance(self):
        try:
            time.sleep(1)
            data = 'getClosestFrontDistance'
            self.setData(data)
            closest= float(self.getData().decode())
            return closest
        except Exception, ex:
            print "Falla: intentando enviar getClosestFrontDistance",str(ex)

    def move(self,dist):
        time.sleep(1)
        data = 'move:' + str(dist)
        self.setData(data)
        self.getData().decode()

    def getLaserBuffer(self):                    
        data = 'getLaserBuffer'
        print data
        self.setData(data)
        data = self.getData()
        data_arr,posData = pickle.loads(b"".join(data))
        return np.array(data_arr),posData
       

    def getMaxReadings(self):
        data = 'getMaxReadings'
        self.setData(data)
        return int(self.getData().decode())

    def getMaxDistance(self):
        data = 'getMaxDistance'
        self.setData(data)
        return int(self.getData().decode())

