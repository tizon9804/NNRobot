import Libraries.RobotSystem.Robot as R
import numpy as np


class Explore:
    def __init__(self, thread,debugExplore,debugRobot):
        try:
            self.debug = debugExplore
            self.logExplore(thread + "init Explore")
            self.robotSystem = R.RobotDriver(debugRobot)
            self.MAXDISTANCE = self.robotSystem.getMaxDistance()
            self.MAXREADINGS = self.robotSystem.getMaxReadings()
            self.RobotStarted = True
            self.angle = 0
            self.cumulateAngle = 0
            self.rotationRate = 90
            self.actualFront = 0
            self.contAngle = 1
            self.estimation = 0
            self.distance = 0
            self.tempMoves = []
            self.trackroute = []
            self.thread = thread
        except Exception as ex:
            self.logExplore(thread + "Cannot connect to Robot:" + str(ex))
            self.RobotStarted = False

    def searchDirection(self):
        start = self.MAXREADINGS/2
        end  = start * -1
        rangeL = 30
        lmoves = []
        #iterate al reading of the sensor in steps of rangeL grades
        for x in range(start,(end+rangeL)-1,-1):
            xend = x-rangeL
            distance,angle = self.robotSystem.getClosestDistance(x,xend)
            self.logExplore(self.thread + " angle::"+ str(self.angle)+ "relative::"+ str(self.getRelativeAngle()))
            estimation = self.calculateProbToMove(distance)
            lmoves.append([angle, distance, estimation])
        self.angle,distance,estimation = self.getAngleMaxDistanceTemp(lmoves)
        self.tempMoves.append([self.angle, distance, estimation])
        self.estimation = estimation
        if self.robotSystem.robot.isHeadingDone():
            self.robotSystem.rotate(self.angle)
            self.cumulateAngle += 1
        self.logExplore(self.thread + "temp:: "+str(len(self.tempMoves))+"&&"+ str(self.tempMoves[len(self.tempMoves) - 1]))


    def calculateProbToMove(self, distance):
        # calculate the final value estimation to move between distance and bestway
        scaledistance = (distance / self.MAXDISTANCE)
        moveestimate = (scaledistance)
        self.logExplore("distance::"+ str(distance)+ "::scaledist::"+ str(scaledistance)+ "::move est:: "+ str(moveestimate))
        return moveestimate

    def transitionMove(self, angle):
        self.logExplore(self.thread + " transition before move::"+ str(angle)+ "relative::"+ str(self.getRelativeAngle()))
        self.robotSystem.rotateSecure(angle)
        self.robotSystem.restartHeading()

    def getRelativeAngle(self):
        return self.robotSystem.robot.getPose().getTh()

    def move(self, distance):
        self.contAngle = 1
        self.cumulateAngle = 0
        self.tempMoves = []
        actDistance = self.robotSystem.getClosestFrontDistance()
        if actDistance < distance:
            self.logExplore(self.thread + ":: ATTENTION!! DISTANCE TO MOVE NOW IS DIFFERENT::act "+ str(actDistance)+ "expected:: "+str(distance))
            self.robotSystem.move(actDistance * 0.8)
        else:
            self.robotSystem.move(distance)

    def getAngleMaxDistanceTemp(self,list):
        maxdistance = 0
        tupleMax = list[len(list) - 1]
        for tuple in reversed(list):
            dist = tuple[2]
            if dist > maxdistance:
                maxdistance = dist
                tupleMax = tuple
        return tupleMax

    def trackRoute(self, angle, distance):
        self.trackroute.append([angle, self.actualFront, distance])

    def logExplore(self,message):
        if self.debug:
            print "ExploreLogic: ",message
