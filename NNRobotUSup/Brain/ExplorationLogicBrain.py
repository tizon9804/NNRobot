import Libraries.RobotSystem.Robot as R
import NNRobotUSup.Network.ServerRobotStream as server


class Explore:
    def __init__(self, thread,debugExplore,debugRobot,isServer):
        try:
            self.debug = debugExplore
            self.logExplore(thread + "init Explore")
            if not isServer:
                self.robotSystem = R.RobotDriver(debugRobot)
            else:
                self.robotSystem = server.RobotServerStream()
                self.robotSystem.acceptRobot()

            self.MAXDISTANCE = self.robotSystem.getMaxDistance()
            self.MAXREADINGS = self.robotSystem.getMaxReadings()
            self.RobotStarted = True
            self.angle = 0
            self.cumulateAngle = 0
            self.rotationRate = 90
            self.actualFront = 0
            self.contAngle = 1
            self.estimation = 0
            self.angleAnt = 0.0
            self.action = False
            self.distance = 0
            self.needOther = True
            self.tempMoves = []
            self.tempMovesBad = []
            self.trackroute = []
            self.thread = thread
        except Exception as ex:
            self.logExplore(thread + "Cannot connect to Robot:" + str(ex))
            self.RobotStarted = False

    def searchDirection(self):
        try:
            start = self.MAXREADINGS/2
            end  = start * -1
            rangeL = 1
            #iterate all reading of the sensor in steps of rangeL grades
            lmoves = self.robotSystem.getClosestDistance(start,(end+rangeL)-1)
            while  self.needOther and len(lmoves) > 0:
                if self.action:
                    angle,distance,estimation = self.getAngleMaxDistanceTempRemove(lmoves)
                    if self.robotSystem.isHeadingDone():
                        self.robotSystem.rotate(angle)
                        self.cumulateAngle += 1
                    self.estimation = estimation
                    angleb, distanceb, estimationb = self.getAngleMinDistanceTemp(lmoves)
                    self.tempMovesBad.append([angleb, distanceb, estimationb])
                    self.tempMoves.append([angle, distance, estimation])
                    self.action = False



            self.logExplore(self.thread + "temp:: "+str(len(self.tempMoves))+"&&"+ str(self.tempMoves[len(self.tempMoves) - 1]))
        except Exception,ex:
            self.logExplore(self.thread + str(ex))

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
        try:
            return self.robotSystem.getTh()
        except Exception,ex:
            self.logExplore(self.thread + str(ex))
            return 0

    def move(self, distance):
        self.contAngle = 1
        self.cumulateAngle = 0
        self.tempMoves = []
        self.tempMovesBad =[]
        actDistance = self.robotSystem.getClosesFrontDistance()
        if actDistance < distance:
            self.logExplore(self.thread + ":: ATTENTION!! DISTANCE TO MOVE NOW IS DIFFERENT::act "+ str(actDistance)+ "expected:: "+str(distance))
            self.robotSystem.move(actDistance * 0.8)
        else:
            self.robotSystem.move(distance)

    def getAngleMaxDistanceTemp(self,list):
        maxdistance = 0
        tupleList = []
        for tuple in reversed(list):
            dist = tuple[2]
            if dist >= maxdistance:
                if dist == maxdistance:
                   tupleList.append(tuple)
                else:
                    tupleList = []
                    tupleList.append(tuple)
                maxdistance = dist
        position =   len(tupleList)/2
        numtup = len(tupleList)
        if numtup > 0:
            tupleMax = tupleList[position]
            return tupleMax
        print "ERROR max getAngleMaxDistanceTemp######################################################"
        return [0, 0, 0]

    def getAngleMaxDistanceTempRemove(self,list):
        maxdistance = 0
        tupleList = []
        i=len(list)-1
        for tuple in reversed(list):
            dist = tuple[2]
            if dist >= maxdistance:
                if dist == maxdistance:
                   tupleList.append([tuple,i])
                else:
                    tupleList = []
                    tupleList.append([tuple,i])
                maxdistance = dist
            i=i-1
        position =   len(tupleList)/2
        numtup = len(tupleList)
        if numtup > 0:
            tupleMax = tupleList[position][0]
            del list[tupleList[position][1]]
            return tupleMax
        print "ERROR max lmoves getAngleMaxDistanceTemp######################################################"
        return [0, 0, 0]

    def getAngleMinDistanceTemp(self,list):
        mindistance = 6000
        tupleList = []
        for tuple in reversed(list):
            dist = tuple[2]
            if dist <= mindistance:
                if dist == mindistance:
                    tupleList.append(tuple)
                else:
                    tupleList = []
                    tupleList.append(tuple)
                    mindistance = dist
        position = len(tupleList) / 2
        numtup = len(tupleList)
        if numtup > 0:
            tupleMin = tupleList[position]
            return tupleMin
        print "ERROR min getAngleMinDistanceTemp######################################################"
        return [0,0,0]

    def trackRoute(self, angle, distance):
        self.trackroute.append([angle, self.actualFront, distance])

    def logExplore(self,message):
        if self.debug:
            print "ExploreLogic: ",message
