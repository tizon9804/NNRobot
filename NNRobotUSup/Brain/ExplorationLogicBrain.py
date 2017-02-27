import Libraries.RobotSystem.Robot as R
import numpy as np

class Explore:
    def __init__(self,thread):
        try:
            print thread + "init Explore"
            self.robotSystem = R.RobotDriver()
            self.MAXDISTANCE = self.robotSystem.getMaxDistance()
            self.RobotStarted = True
            self.angle = 0
            self.actualFront = 0
            self.contAngle=1
            self.estimation = 0
            self.distance = 0
            self.tempMoves = []
            self.thread = thread
        except Exception as ex:
            print thread + "Cannot connect to Robot:" + str(ex)
            self.RobotStarted = False
    def searchDirection(self,bestWay):
        relAngle=self.getRelativeAngle(self.angle)
        self.robotSystem.rotateSecure(relAngle)
        distance = self.robotSystem.getClosestFrontDistance()
        print self.thread + " angle::", self.angle,"relative::",relAngle
        self.estimation = self.calculateProbToMove(distance,bestWay)
        self.tempMoves.append([self.angle,distance,self.estimation])
        print self.thread + "temp::",self.tempMoves[len(self.tempMoves)-1]
        self.angle += np.power(-1.4,self.contAngle)
        self.contAngle += 1

    def calculateProbToMove(self,distance,bestWay):
        # calculate the final value estimation to move between distance and bestway
        scaledistance = (distance / self.MAXDISTANCE)*2
        moveestimate = bestWay - (1 - scaledistance)
        print "distance::", distance, "::besway::", bestWay, "::scaledist::", scaledistance, "::move est:: ", moveestimate
        return moveestimate

    def transitionMove(self,angle):
        relAngle = self.getRelativeAngle(angle)
        print self.thread + " transition before move::", angle,"relative::",relAngle
        self.robotSystem.rotateSecure(relAngle)
        self.robotSystem.restartHeading()

    def getRelativeAngle(self,angle):
        return self.actualFront + angle

    def move(self,distance):
        self.actualFront = self.robotSystem.robot.getPose().getTh()
        self.angle = 0
        self.contAngle = 1
        self.tempMoves = []
        actDistance = self.robotSystem.getClosestFrontDistance()
        if actDistance < distance:
            print self.thread + ":: ATTENTION!! DISTANCE TO MOVE NOW IS DIFFERENT::act",actDistance,"expected::", distance
            self.robotSystem.move(actDistance * 0.8)
        else:
            self.robotSystem.move(distance)

    def getAngleMaxDistanceTemp(self):
        maxdistance=0
        tupleMax = self.tempMoves[len(self.tempMoves)-1]
        for tuple in self.tempMoves:
            dist=tuple[2]
            if dist > maxdistance:
                maxdistance=dist
                tupleMax = tuple
        return tupleMax
