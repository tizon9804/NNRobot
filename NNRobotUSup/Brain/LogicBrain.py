from NNRobotUSup.Memory import LongTerm as lt
import ExplorationLogicBrain as ELB
#import NNRobotUSup.ImageRecognition.SightSense as sight
import threading
import numpy as np


class LogicBrain:
    def __init__(self):
        self.PROBTOMOVE = 0.8#is temp 1
        self.logicLife = True
        self.senseLife = True
        self.exploreLife = True
        self.RobotLife = False
        self.moveEstimation = 0
        self.actualEstimation = 0
        self.actualDistance = 0
        self.actualAngle = 0
        self.error = 100
        self.isSearching = True
        self.isMoving = False
        self.isTransition = False
        self.targetList = []
        self.longTerm = lt.LongTerm()
        # init in new thread the part of the brain that take decisions
        tLogic = threading.Thread(target=self.loopLogic)
        tLogic.start()
        # init in new thread the part of the brain that take the sensors
        tSense = threading.Thread(target=self.loopSense)
        #tSense.start()
        # init in new thread the part of the brain that have actuators
        tExplore = threading.Thread(target=self.loopExplore)
        tExplore.start()

    def loopLogic(self):
        self.logic = "Logic"
        self.logLogicThread("thread started...")
        while self.logicLife:
            if self.RobotLife:
                if self.isSearching:
                    self.isSearchingLogic()

    def isSearchingLogic(self):
        if np.absolute(self.exploreLogic.angle) > 180 or self.moveEstimation >= self.PROBTOMOVE:
            self.isSearching = False
            self.logLogicThread("Finishing Search")
            threading._sleep(1)
            self.logLogicThread("###SEARCHED###")
            self.logLogicThread(":::" + str(self.moveEstimation))
            while len(self.exploreLogic.tempMoves)== 0:
                print "waiting.."
            self.actualAngle,self.actualDistance,self.actualEstimation = self.exploreLogic.getAngleMaxDistanceTemp()
            self.error = self.actualDistance * 0.1
            self.startMoving()

    def startMoving(self):
        self.isTransition = True
        self.isMoving = True
    def loopSense(self):
        self.sense = "Sense"
        self.logSenseThread("thread started...")
        self.sight = sight.SightSense()
        while self.senseLife:
            self.sight.getRoute()
            if self.RobotLife:
                self.logSenseThread("sense laser robotlife:" + str(self.RobotLife))

    def loopExplore(self):
        self.explore = "Explore"
        self.logExploreThread("thread started...")
        self.exploreLogic = ELB.Explore(self.explore)
        while self.exploreLife:
            self.RobotLife = self.exploreLogic.RobotStarted
            if self.RobotLife:
                self.logExploreThread(str(self.PROBTOMOVE))
                self.searchDirection()
                self.move()

    def searchDirection(self):
        if self.isSearching:
            # think best way with the nnet return 0-1 where 1 is a secure way
            bestWay = 1
            # search a possible direction to move, it do not cares the range of distance
            self.exploreLogic.searchDirection(bestWay)
            self.moveEstimation = self.exploreLogic.estimation

    def move(self):
        if self.isMoving:
            if self.isTransition:
                self.inTransition()
            self.logExploreThread("moving robot" + str(self.actualDistance - self.error))
            self.exploreLogic.move(self.actualDistance - self.error)
            threading._sleep(1)
            self.logLogicThread("FINISHING MOVE")
            self.actualAngle = 0
            self.actualDistance = 0
            self.isMoving = False
            self.isSearching = True
            # track route could be saved in middleterm(graph)

    def inTransition(self):
        self.logExploreThread("in transition")
        self.PROBTOMOVE = self.actualEstimation/1.1
        self.moveEstimation = 0
        print "PROBTOMOVE::",self.PROBTOMOVE
        print "Best way for laser::", self.actualAngle, ":::", self.actualDistance
        self.exploreLogic.transitionMove(self.actualAngle)
        self.isTransition = False

    def logLogicThread(self, message):
        print self.logic + ": " + message

    def logSenseThread(self, message):
        print self.sense + ": " + message

    def logExploreThread(self, message):
        print self.explore + ": " + message
