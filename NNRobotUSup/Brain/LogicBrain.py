from NNRobotUSup.Memory import LongTerm as lt
import NNRobotUSup.Memory.ShortTerm as S

import NNRobotUSup.ImageRecognition.SightSense as sight
import NNRobotUSup.Network.Routes as ro
import numpy as np
import time
import psutil as psu
import TExplore as TE
import TLogic as TL
import TSense as TS

class BrainParams:
    def __init__(self):
        self.debugLogic = True
        self.debugSense = False
        self.debugExplore = False
        self.debugNetwork = False
        self.debugExploreLogic = False
        self.debugRobotSystem = False
        self.net = ro.Network(self.debugNetwork)
        self.PROBTOMOVE = 0.8  # is temp 1
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
        self.isVideoStreaming = False
        self.targetList = []
        self.Lmemory = lt.LongTerm()
        self.Smemory = S.ShortTerm()
        self.sight = sight.SightSense(self.isVideoStreaming, self.Smemory, self.Lmemory)
        # robot indicators
        self.laserData = []
        self.posData = []
        self.nlogic = 0
        self.nimage = 0
        self.nexplore = 0
        self.logic = "Logic"
        self.sense = "Sense"
        self.explore = "Explore"

    def ips(self, last_time, diffs):
        # Add new time diff to list
        new_time = time.clock()
        if len(diffs) > 10000:
            diffs = []
        diffs.append(new_time - last_time)
        last_time = new_time
        # Clip the list
        ips = 1 / (sum(diffs) / len(diffs))
        return [last_time, diffs, ips]

    def sendDataVA(self):
        self.net.sendData(self.laserData, self.posData, self.nlogic, self.nimage, self.nexplore, psu.cpu_percent(),
                         psu.virtual_memory().percent)

    def sendDataSight(self):
        cluster = self.Smemory.itemsZip
        center = self.Smemory.centersZip
        #print cluster.shape
        #print center.shape
        clus = []
        i=0
        for cl in cluster:
            clus.append({"x": cl[0], "y": cl[1], "range": cl[2],"index": i })
            i = i + 1
        for cl in center:
            clus.append({"x": cl[0], "y": cl[1], "range": -1})
        # envia informacion para visualizar
        self.net.sendDataSight(clus)
    # ----------------------------------------------------------------------------------
    # LOGS
    # ---------------------------------------------------------------------------------

    def logExploreThread(self, message):
        if self.debugExplore:
            print self.explore + ": " + message

    def logSenseThread(self, message):
        if self.debugSense:
            print self.sense + ": " + message


    def logLogicThread(self, message):
        if self.debugLogic:
            print self.logic + ": " + message


class LogicBrain:
    def __init__(self):
        self.brainParams = BrainParams()
        # init in new thread the part of the brain that take the sensors
        self.Sense = TS.Sense(self.brainParams)
        # init in new thread the part of the brain that have actuators
        self.Explore = TE.Explore(self.brainParams)
        # init in new thread the part of the brain that take decisions
        self.Logic = TL.Logic(self.brainParams,self.Explore,self.Sense)





