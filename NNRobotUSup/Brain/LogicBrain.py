from NNRobotUSup.Memory import LongTerm as lt
import NNRobotUSup.Memory.ShortTerm as S
import NNRobotUSup.ImageRecognition.SightSense as sight
import NNRobotUSup.Network.Routes as ro
import NNRobotUSup.Network.FtpSender as ftp
import Libraries.Persistence.TargetManager as T
import time
import psutil as psu
import TExplore as TE
import TLogic as TL
import TSense as TS
import numpy as np
import random

class BrainParams:
    def __init__(self):
        self.debugLogic = True
        self.debugSense = True
        self.debugExplore = True
        self.debugNetwork = False
        self.debugExploreLogic = False
        self.debugRobotSystem = False
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
        self.numReportSecure = 0
        self.isMoving = False
        self.isTransition = False
        self.isVideoStreaming = True
        self.isBadWay = False
        self.targetList = []
        self.ftpSender = ftp.FtpSender()
        self.persistence = T.targetManager()
        self.net = ro.Network(self.debugNetwork, self)
        self.Lmemory = lt.LongTerm(self.persistence,self.ftpSender,self)
        self.Smemory = S.ShortTerm()
        self.sight = sight.SightSense(self.isVideoStreaming, self.Smemory, self.Lmemory, self.ftpSender,self)
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
        try:
            pred = 'Is a Bad Direction' if self.Lmemory.conscience.prediction == 1 else 'Is a good Direction'
            prob = self.Lmemory.conscience.probability
        except Exception,ex:
            pred=0
            prob=0
        self.net.sendData(self.laserData, self.posData, self.nlogic, self.nimage, self.nexplore, psu.cpu_percent(),
                         psu.virtual_memory().percent,pred,prob)

    def sendDataSight(self):
        cluster = self.Smemory.itemsZip
        center = self.Smemory.centersZip
        clus = []
        i=0
        for cl in cluster:
            clus.append({"x": cl[0], "y": cl[1], "range": cl[2],"index": i })
            i = i + 1
        #if len(clus) > 600:
         #   random.shuffle(clus)
          #  clus = clus[:600]
        i = 0
        for cl in center:
            clus.append({"x": cl[0], "y": cl[1], "range": i, "index": -1})
            i = i + 1
        reportTraining = self.getTrainingStatistics()
        # envia informacion para visualizar
        self.net.sendDataSight(clus)

    def sendDataNnet(self):
        reportTraining = self.getTrainingStatistics()
        # envia informacion para visualizar
        if self.isNewReportSecure or self.numReportSecure == 0:
            self.net.sendDataNnet(reportTraining)

    def getTrainingStatistics(self):
        reportCost = np.array([])
        reportSecure = np.array([])
        iterP = 0
        iterS = 0
        self.isNewReportSecure = False
        if self.Lmemory.isTraining:
            reportCost = self.Lmemory.trainMind.reportCost
            reportSecure = self.Lmemory.trainMind.reportSecure
            numSecure = reportSecure.shape[0]
            if numSecure > self.numReportSecure:
                print "##############################", numSecure
                self.isNewReportSecure = True
                self.numReportSecure= numSecure
            iterP = self.Lmemory.trainMind.i
            iterS = self.Lmemory.trainMind.y.shape[0]
        else:
            self.numReportSecure = 0
        lambdaNN = self.Lmemory.lambdaNN
        maxIter = self.Lmemory.maxIter
        accurExpected = self.Lmemory.accuracyExpected
        report = ({'rcost':[reportCost],
                   'rsecure':[reportSecure],
                   'iterp':[iterP],
                   'iters':[iterS],
                   'lambdann':[lambdaNN],
                   'maxiter':[maxIter],
                   'accurExp':[accurExpected],
                   'isTraining':[self.Lmemory.isTraining]
                   })

        return report
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





