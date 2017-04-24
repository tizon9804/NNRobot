import socket
#import ExplorationInterface as Exp

class robotStream:
    def __int__(self):
        print 'conecting...'

    def connection(self):
        #self.robot = Exp.ExploreInterface()
        while(True):
            # Connect a client socket to my_server:8000 (change my_server to the
            # hostname of your server) 190.158.131.76
            try:
                self.client_socket = socket.socket()
                self.client_socket.connect(('157.253.206.25', 8080))
                self.connect = True
                try:
                   while(True):
                       if self.startingConv():
                           self.getClosestDistance()
                           #self.isHeadingDone()
                           #self.rotate()
                           #self.rotateSecure()
                           #self.restartHeading()
                           #self.getTh()
                           #self.getClosesFrontDistance()
                           #self.move()
                           #self.getLaserBuffer()

                       print "sended"
                except Exception as ex:
                    self.connect = False
                    print "connection finished..."
                finally:
                    self.client_socket.close()
            except Exception as ex:
                self.connect = False
                print "trying Connect Robot..."

    def getData(self):
        data = self.client_socket.recv(1024).decode()
        print data
        return data

    def setData(self,data):
        self.client_socket.send(b''+str(data))

    def startingConv(self):
        self.client_socket.send(b'raspChappie')
        data = self.getData()
        if data == "HiRasp":
            return True
        return False

    def getClosestDistance(self):
        data = self.getData()
        data = data.split(":")
        if data[0] == "getClosestDistance":
            data = self.robotSystem.getClosestDistance(data[1], data[2])
            self.setData(data)

    def isHeadingDone(self):
        data = self.getData()
        data = data.split(":")
        if data[0] == "isHeadingDone":
            data = self.robotSystem.robot.isHeadingDone()
            self.setData(data)

    def rotate(self):
        data = self.getData()
        data = data.split(":")
        if data[0] == "rotate":
            self.robotSystem.rotate(data[1])

    def rotateSecure(self):
        data = self.getData()
        data = data.split(":")
        if data[0] == "rotateSecure":
            self.robotSystem.rotateSecure(data[1])

    def restartHeading(self):
        data = self.getData()
        data = data.split(":")
        if data[0] == "restartHeading":
            self.robotSystem.restartHeading()

    def getTh(self):
        data = self.getData()
        data = data.split(":")
        if data[0] == "getTh":
            data = self.robotSystem.robot.getPose().getTh()
            self.setData(data)

    def getClosesFrontDistance(self):
        data = self.getData()
        data = data.split(":")
        if data[0] == "getClosestFrontDistance":
            data = self.robotSystem.getClosestFrontDistance()
            self.setData(data)

    def move(self):
        data = self.getData()
        data = data.split(":")
        if data[0] == "move":
            self.robotSystem.move(data[1])

    def getLaserBuffer(self):
        data = self.getData()
        data = data.split(":")
        if data[0] == "getLaserBuffer":
            data = self.robotSystem.getLaserBuffer()
            self.setData(data)


    def getMaxReadings(self):
        data = self.getData()
        data = data.split(":")
        if data[0] == "getMaxReadings":


    def getMaxDistance(self):
        data = self.getData()
        data = data.split(":")
        if data[0] == "getClosestDistance":
