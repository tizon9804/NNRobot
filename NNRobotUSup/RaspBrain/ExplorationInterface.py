import Libraries.RobotSystem.Robot as R

class ExploreInterface:
    def __init__(self, thread,debugExplore,debugRobot):
        try:
            self.debug = debugExplore
            self.logExplore(thread + "init Explore")
            self.robotSystem = R.RobotDriver(debugRobot)
            self.MAXDISTANCE = self.robotSystem.getMaxDistance()
            self.MAXREADINGS = self.robotSystem.getMaxReadings()
            self.RobotStarted = True
            self.thread = thread
        except Exception as ex:
            self.logExplore(thread + "Cannot connect to Robot:" + str(ex))
            self.RobotStarted = False

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
        return self.robotSystem.getLaserBuffer();










