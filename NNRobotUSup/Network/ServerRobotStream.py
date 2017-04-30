import socket
import pickle
import numpy as np
class RobotServerStream:
    def __init__(self):
        # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
        # all interfaces)
        self.isRobotActive = False

    def acceptRobot(self):
        print "open sockets port 8080"
        self.isRobotActive = False
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8080))
        print "listening ROBOT"
        self.server_socket.listen(0)
        print  "Accept a single connection ROBOT"
        self.connection,self.addressR = self.server_socket.accept()
        waiting=True
        while(waiting):
            print '#################### Waiting Robot...########################'
            data = self.getData()
            if data == 'raspChappie':
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
            connection.close()
            self.server_socket.close()
            return '#############################################################'

    def setData(self,data):
        try:
            self.connection.send(b''+str(data))
        except Exception,ex:
            print "Robot Error: ",str(ex)
    def getClosestDistance(self,x,xend):
        data = 'getClosestDistance:'+str(x)+':'+ str(xend)
        self.setData(data)
        data = self.connection.recv(4096*16)
        try:
            lmoves = pickle.loads(data)
            return lmoves
        except Exception,ex:
            return []


    def isHeadingDone(self):
        data = 'isHeadingDone'
        self.setData(data)
        return bool(self.getData())


    def rotate(self,angle):
        data = 'rotate:' + str(angle)
        self.setData(data)
        self.getData()

    def rotateSecure(self,angle):
        data = 'rotateSecure:' + str(angle)
        self.setData(data)
        self.getData()

    def restartHeading(self):
        data = 'restartHeading'
        self.setData(data)
        self.getData()

    def getTh(self):
        data = 'getTh'
        self.setData(data)
        return float(self.getData())

    def getClosesFrontDistance(self):
        falla = True
        while falla:
            try:
                data = 'getClosestFrontDistance'
                self.setData(data)
                closest= float(self.getData())
                falla = False
                return closest
            except Exception, ex:
                falla = True
                print "Falla: intentando enviar getClosestFrontDistance",str(ex)

    def move(self,dist):
        data = 'move:' + str(dist)
        self.setData(data)
        self.getData()

    def getLaserBuffer(self):
        data = 'getLaserBuffer'
        self.setData(data)
        data = self.connection.recv(4096*16)
        data_arr = pickle.loads(data)
        return np.array(data_arr)


    def getMaxReadings(self):
        data = 'getMaxReadings'
        self.setData(data)
        return int(self.getData())

    def getMaxDistance(self):
        data = 'getMaxDistance'
        self.setData(data)
        return int(self.getData())

