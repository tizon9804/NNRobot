import socket


class RobotServerStream:
    def __init__(self):
        # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
        # all interfaces)
        self.isRobotActive = False

    def acceptRobot(self):
        print "open sockets port 8000"
        self.isRobotActive = False
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8080))
        print "listening"
        self.server_socket.listen(0)
        print  "Accept a single connection and make a file-like object out of it"
        self.connection,self.addressR = self.server_socket.accept()
        data = self.getData()
        waiting=True
        while(waiting):
            if data == 'raspChappie':
                self.setData('HiRasp')
                waiting = False
                self.isRobotActive = True
                print 'started...'

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
            return ''

    def setData(self,data):
        self.connection.send(b''+str(data))

    def getClosestDistance(self,x,xend):
        data = 'getClosestDistance:'+str(x)+':'+ str(xend)
        self.setData(data)
        return self.getData()

    def isHeadingDone(self):
        data = 'isHeadingDone'
        self.setData(data)
        return self.getData()


    def rotate(self,angle):
        data = 'rotate:' + str(angle)
        self.setData(data)


    def rotateSecure(self,angle):
        data = 'rotateSecure:' + str(angle)
        self.setData(data)


    def restartHeading(self):
        data = 'restartHeading'
        self.setData(data)


    def getTh(self):
        data = 'getTh'
        self.setData(data)
        return self.getData()

    def getClosesFrontDistance(self):
        data = 'getClosestFrontDistance'
        self.setData(data)
        return self.getData()

    def move(self,dist):
        data = 'move:' + str(dist)
        self.setData(data)

    def getLaserBuffer(self):
        data = 'getLaserBuffer'
        self.setData(data)
        return self.getData()

    def getMaxReadings(self):
        data = 'getMaxReadings'
        self.setData(data)
        return self.getData()

    def getMaxDistance(self):
        data = 'getMaxDistance'
        self.setData(data)
        return self.getData()

