import threading,time
import numpy as np
from NNRobotUSup.Memory import LongTerm as lt
import NNRobotUSup.Memory.ShortTerm as S

class Logic:
    def __init__(self,BrainP,Explore,Sense):
        self.explore = Explore
        self.sense = Sense
        self.bparm = BrainP
        tLogic = threading.Thread(target=self.loopLogic)
        tLogic.start()

    def loopLogic(self):
        self.bparm.logLogicThread("thread started...")
        last_time = time.clock()
        diffs = []
        while self.bparm.logicLife:
            # register iterations per second
            #self.bparm.logLogicThread("Thinking...")
            self.sendStatistics()
            last_time, diffs, ips = self.bparm.ips(last_time, diffs);
            self.bparm.nlogic = ips
            self.isSearchingLogic()
            self.learnObjects()

    # ----------------------------------------------------------------------------------
    # LOGIC
    # ---------------------------------------------------------------------------------
    def learnObjects(self):
        sMemory = self.bparm.Smemory # type: S.ShortTerm
        state = len(sMemory.Z) % 100
        if state == 0 and len(sMemory.Z) > 0:
            sMemory.clustering = True
            costdif = 0
            antCost = 0
            isbreak = False
            #metodo de elbow
            for i in range(2,100):
                cost = sMemory.Cluster(i)
                if isbreak:
                    break
                costdifAct = antCost - cost
                #Primera derivada difgradiente todo segunda derivada
                difGrad = costdif/costdifAct
                antCost = cost
                costdif = costdifAct
                if i == 1:
                   costdifAct = cost
                   costdif = costdifAct
                if difGrad > 2:
                    isbreak = True

            sMemory.clustering = False


    def isSearchingLogic(self):
        if self.bparm.RobotLife:
            if self.bparm.isSearching:
                self.explore.exploreLogic
                if np.absolute(
                        self.explore.exploreLogic.cumulateAngle) > 3 or self.bparm.moveEstimation >= self.bparm.PROBTOMOVE * 0.90:  # TODO
                    self.isSearching = False
                    threading._sleep(0.5)
                    self.bparm.logLogicThread("###SEARCHED###")
                    self.bparm.logLogicThread(":::" + str(self.bparm.moveEstimation))
                    while len(self.explore.exploreLogic.tempMoves) == 0:
                        self.bparm.logLogicThread("waiting..")
                    self.bparm.actualAngle, self.bparm.actualDistance, self.bparm.actualEstimation = self.explore.exploreLogic.getAngleMaxDistanceTemp(self.explore.exploreLogic.tempMoves)
                    self.bparm.logLogicThread(
                        str(self.bparm.actualAngle) + "$$" + str(self.bparm.actualDistance) + "$$" + str(self.bparm.actualEstimation))
                    # threading._sleep(5)
                    # self.exploreLogic.rotationRate -= (1 - self.actualEstimation) / 4  # TODO
                    self.bparm.logLogicThread(" rotation rate::: " + str(self.explore.exploreLogic.rotationRate))
                    self.bparm.error = self.bparm.actualDistance * 0.1
                    self.startMoving()


    def startMoving(self):
        self.bparm.isTransition = True
        self.bparm.isMoving = True

    #----------------------------------------------------------------------------------------------
    # visual analitics
    #-----------------------------------------------------------------------------------------------

    def sendStatistics(self):
        self.bparm.sendDataVA()
        self.bparm.sendDataSight()

