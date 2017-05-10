import Libraries.RobotSystem.Robot as R

class ExploreInterface:
    def __init__(self, thread,debugExplore,debugRobot,ip):
        try:
            self.debug = debugExplore
            print thread + "init Explore"
            self.debugRobot =debugRobot
            self.ip =ip
            self.robotSystem = R.RobotDriver(debugRobot,ip)
            self.MAXDISTANCE = self.robotSystem.getMaxDistance()
            self.MAXREADINGS = self.robotSystem.getMaxReadings()
            self.robot = self.robotSystem.robot
            self.RobotStarted = True
            self.thread = thread
        except Exception as ex:
            print thread + "Cannot connect to Robot:" + str(ex)
            self.RobotStarted = False
            self.restart()

    def getClosestDistance(self,x,xend):
        return self.robotSystem.getClosestDistance(x,xend)

    def isHeadingDone(self):
        return self.robotSystem.robot.isHeadingDone()

    def rotate(self,angle):
        self.robotSystem.rotate(angle)

    def rotateSecure(self,angle):
        self.robotSystem.rotateSecure(angle)

    def restartHeading(self):
        self.robotSystem.restartHeading()

    def getTh(self):
        return self.robotSystem.robot.getPose().getTh()

    def getClosesFrontDistance(self):
        return self.robotSystem.getClosestFrontDistance()

    def move(self,dist):
        self.robotSystem.move(dist)

    def getLaserBuffer(self):
        buffer =  self.robotSystem.getLaserBuffer();
        if buffer =='NoneType':
            self.restart()
        return buffer

    def restart(self):
        try:
            self.robotSystem.closeRobot();
            self.robotSystem = R.RobotDriver(self.debugRobot, self.ip)
            self.MAXDISTANCE = self.robotSystem.getMaxDistance()
            self.MAXREADINGS = self.robotSystem.getMaxReadings()
            self.robot = self.robotSystem.robot
            self.RobotStarted = True
        except Exception,ex:
            self.RobotStarted = False







