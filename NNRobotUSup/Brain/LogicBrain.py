from NNRobotUSup.Memory import LongTerm as lt
import ExplorationLogicBrain as ELB
#import NNRobotUSup.ImageRecognition.SightSense as sight
import NNRobotUSup.Network.Routes as ro
import threading
import numpy as np
import time
import psutil as psu
import datetime as dt


class LogicBrain:
    def __init__(self):
        self.net = ro.Network()
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
        #robot indicators
        self.laserData = []
        self.posData = []
        self.nlogic = 0
        self.nimage = 0
        self.nexplore = 0
        # init in new thread the part of the brain that take decisions
        tLogic = threading.Thread(target=self.loopLogic)
        tLogic.start()
        # init in new thread the part of the brain that take the sensors
        tSense = threading.Thread(target=self.loopSense)
        tSense.start()
        # init in new thread the part of the brain that have actuators
        tExplore = threading.Thread(target=self.loopExplore)
        tExplore.start()

    def loopLogic(self):
        self.logic = "Logic"
        self.logLogicThread("thread started...")
        last_time = time.clock()
        diffs = []
        while self.logicLife:
            # register iterations per second
            self.logLogicThread("Thinking...")
            last_time,diffs,ips = self.ips(last_time,diffs);
            self.nlogic = ips
            if self.RobotLife:
                if self.isSearching:
                    self.isSearchingLogic()

    def loopSense(self):
        self.sense = "Sense"
        self.logSenseThread("thread started...")
        last_time = time.clock()
        diffs = []
        #self.sight = sight.SightSense()
        while self.senseLife:
            #register iterations per second
            last_time, diffs, ips = self.ips(last_time, diffs);
            self.nimage = ips
            #self.sight.getRoute()
            #time.sleep(0.5)
            self.net.sendData(self.laserData,self.posData,self.nlogic,self.nimage,self.nexplore,psu.cpu_percent(),psu.virtual_memory().percent)
            if self.RobotLife:
                self.laserData,self.posData = self.exploreLogic.robotSystem.getLaserBuffer()

    def loopExplore(self):
        self.explore = "Explore"
        self.logExploreThread("thread started...")
        self.exploreLogic = ELB.Explore(self.explore)
        last_time = time.clock()
        diffs = []
        while self.exploreLife:
            # register iterations per second
            last_time, diffs, ips = self.ips(last_time, diffs);
            self.nexplore = ips
            self.RobotLife = self.exploreLogic.RobotStarted
            if self.RobotLife:
                self.searchDirection()
                self.move()

    def isSearchingLogic(self):
        if np.absolute(self.exploreLogic.angle) > 180 or self.moveEstimation >= self.PROBTOMOVE*0.90:  # TODO
            self.isSearching = False
            threading._sleep(0.2)
            self.logLogicThread("###SEARCHED###")
            self.logLogicThread(":::" + str(self.moveEstimation))
            while len(self.exploreLogic.tempMoves) == 0:
                print "waiting.."
            self.actualAngle, self.actualDistance, self.actualEstimation = self.exploreLogic.getAngleMaxDistanceTemp()
            self.exploreLogic.rotationRate -= (1 - self.actualEstimation) / 4  # TODO
            self.logLogicThread(" rotation rate::: " + str(self.exploreLogic.rotationRate))
            self.error = self.actualDistance * 0.3
            self.startMoving()

    def startMoving(self):
        self.isTransition = True
        self.isMoving = True

    def searchDirection(self):
        if self.isSearching:
            # think best way with the nnet return 0-1 where 1 is a secure way
            bestWay = 1
            # search a possible direction to move, it do not cares the range of distance
            self.exploreLogic.searchDirection(bestWay)
            self.logExploreThread(str(self.PROBTOMOVE))
            self.moveEstimation = self.exploreLogic.estimation

    def move(self):
        if self.isMoving:
            if self.isTransition:
                self.inTransition()
            self.logExploreThread("moving robot" + str(self.actualDistance - self.error))
            self.exploreLogic.move(self.actualDistance - self.error)
            threading._sleep(0.2)
            self.logLogicThread("FINISHING MOVE")
            self.actualAngle = 0
            self.actualDistance = 0
            self.isMoving = False
            self.isSearching = True
            # track route could be saved in middleterm(graph)

    def inTransition(self):
        self.logExploreThread("in transition")
        self.PROBTOMOVE = 0.7
        self.moveEstimation = 0
        print "Best way for laser::", self.actualAngle, ":::", self.actualDistance,"PROBTOMOVE::",self.PROBTOMOVE
        self.exploreLogic.transitionMove(self.actualAngle)
        self.isTransition = False

    def logLogicThread(self, message):
        print self.logic + ": " + message

    def logSenseThread(self, message):
        print self.sense + ": " + message

    def logExploreThread(self, message):
        print self.explore + ": " + message

    def ips(self,last_time,diffs):
        # Add new time diff to list
        new_time = time.clock()
        if len(diffs) > 10000:
            diffs = []
        diffs.append(new_time - last_time)
        last_time = new_time
        # Clip the list
        ips= 1/(sum(diffs)/len(diffs))
        return [last_time,diffs,ips]

