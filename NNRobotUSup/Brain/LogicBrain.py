from NNRobotUSup.Memory import LongTerm as lt
import NNRobotUSup.Memory.ShortTerm as S
import ExplorationLogicBrain as ELB
import NNRobotUSup.ImageRecognition.SightSense as sight
import NNRobotUSup.Network.Routes as ro
import threading
import numpy as np
import time
import psutil as psu
from matplotlib import pyplot as plt



class LogicBrain:
    def __init__(self):
        self.debugLogic = True
        self.debugSense = False
        self.debugExplore = False
        self.debugNetwork = False
        self.debugExploreLogic = False
        self.debugRobotSystem = False
        self.net = ro.Network(self.debugNetwork)
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
        self.isVideoStreaming = True
        self.targetList = []
        self.Lmemory = lt.LongTerm()
        self.Smemory = S.ShortTerm()
        #robot indicators
        self.laserData = []
        self.posData = []
        self.nlogic = 0
        self.nimage = 0
        self.nexplore = 0
        # init in new thread the part of the brain that take decisions
        tLogic = threading.Thread(target=self.loopLogic)
        #tLogic.start()
        # init in new thread the part of the brain that take the sensors
        tSense = threading.Thread(target=self.loopSense)
        tSense.start()
        # init in new thread the part of the brain that have actuators
        tExplore = threading.Thread(target=self.loopExplore)
        #tExplore.start()
        while True:
            if self.Smemory.kmeans.plot:
                A = self.Smemory.kmeans.A
                B = self.Smemory.kmeans.B
                C = self.Smemory.kmeans.C
                D = self.Smemory.kmeans.D
                E = self.Smemory.kmeans.E
                F = self.Smemory.kmeans.F
                Z = self.Smemory.kmeans.z
                center = self.Smemory.kmeans.center
                # Plot the data
                plt.scatter(A[:, 0], A[:, 1])
                plt.scatter(B[:, 0], B[:, 1], c='r')
                plt.scatter(C[:, 0], C[:, 1], c='b')
                plt.scatter(D[:, 0], D[:, 1], c='y')
                plt.scatter(E[:, 0], E[:, 1], c='g')
                plt.scatter(F[:, 0], F[:, 1], c='r')
                plt.scatter(center[:, 0], center[:, 1], s=80, c='y', marker='s')
                plt.xlabel('Height'), plt.ylabel('Weight')
                plt.show()

    def loopLogic(self):
        self.logic = "Logic"
        self.logLogicThread("thread started...")
        last_time = time.clock()
        diffs = []
        while self.logicLife:
            # register iterations per second
            #self.logLogicThread("Thinking...")
            self.sendDataVA()
            last_time,diffs,ips = self.ips(last_time,diffs);
            self.nlogic = ips
            self.isSearchingLogic()

    def loopSense(self):
        self.sense = "Sense"
        self.logSenseThread("thread started...")
        last_time = time.clock()
        diffs = []
        self.sight = sight.SightSense(self.isVideoStreaming,self.Smemory)
        while self.senseLife:
            #register iterations per second
            last_time, diffs, ips = self.ips(last_time, diffs);
            self.nimage = ips
            self.logSenseThread("transmiting...")
            self.sight.getRoute()
            #time.sleep(0.5)

    def loopExplore(self):
        self.explore = "Explore"
        self.logExploreThread("thread started...")
        self.exploreLogic = ELB.Explore(self.explore,self.debugExploreLogic,self.debugRobotSystem)
        last_time = time.clock()
        diffs = []
        while self.exploreLife:
            # register iterations per second
            last_time, diffs, ips = self.ips(last_time, diffs);
            self.nexplore = ips
            self.RobotLife = self.exploreLogic.RobotStarted
            if self.RobotLife:
                self.laserData, self.posData = self.exploreLogic.robotSystem.getLaserBuffer()
                self.searchDirection()
                self.move()
#----------------------------------------------------------------------------------
#LOGIC
#---------------------------------------------------------------------------------
    def isSearchingLogic(self):
        if self.RobotLife:
            if self.isSearching:
                if np.absolute(self.exploreLogic.cumulateAngle) > 3 or self.moveEstimation >= self.PROBTOMOVE*0.90:  # TODO
                    self.isSearching = False
                    threading._sleep(0.5)
                    self.logLogicThread("###SEARCHED###")
                    self.logLogicThread(":::" + str(self.moveEstimation))
                    while len(self.exploreLogic.tempMoves) == 0:
                        self.logLogicThread( "waiting..")
                    self.actualAngle, self.actualDistance, self.actualEstimation = self.exploreLogic.getAngleMaxDistanceTemp(self.exploreLogic.tempMoves)
                    self.logLogicThread(str(self.actualAngle)+"$$"+str(self.actualDistance)+"$$"+str(self.actualEstimation))
                    #threading._sleep(5)
                    #self.exploreLogic.rotationRate -= (1 - self.actualEstimation) / 4  # TODO
                    self.logLogicThread(" rotation rate::: " + str(self.exploreLogic.rotationRate))
                    self.error = self.actualDistance * 0.1
                    self.startMoving()

    def startMoving(self):
        self.isTransition = True
        self.isMoving = True

# ----------------------------------------------------------------------------------
# EXPLORE
# ---------------------------------------------------------------------------------

    def searchDirection(self):
        if self.isSearching:
            # search a possible direction to move, it do not cares the range of distance
            self.exploreLogic.searchDirection()
            self.logExploreThread(str(self.PROBTOMOVE))
            # think best way with the nnet return 0-1 where 1 is a secure way
            bestWay = 1
            self.moveEstimation = bestWay - (1-self.exploreLogic.estimation)

    def move(self):
        if self.isMoving:
            if self.isTransition:
                self.inTransition()
            self.logExploreThread("moving robot" + str(self.actualDistance - self.error))
            self.exploreLogic.move(self.actualDistance - self.error)
            threading._sleep(0.5)
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

    # ----------------------------------------------------------------------------------
    # LOGS
    # ---------------------------------------------------------------------------------

    def logLogicThread(self, message):
        if self.debugLogic:
            print self.logic + ": " + message

    def logSenseThread(self, message):
        if self.debugSense:
            print self.sense + ": " + message

    def logExploreThread(self, message):
        if self.debugExplore:
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

    def sendDataVA(self):
        self.net.sendData(self.laserData, self.posData, self.nlogic, self.nimage, self.nexplore, psu.cpu_percent(),
                          psu.virtual_memory().percent)
