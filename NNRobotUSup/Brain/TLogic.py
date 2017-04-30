import threading,time
import numpy as np
from NNRobotUSup.Memory import LongTerm as lt
import NNRobotUSup.Memory.ShortTerm as S
import TExplore as TE
import cv2

class Logic:
    def __init__(self,BrainP,Explore,Sense):
        self.explore = Explore # type: TE.Explore
        self.sense = Sense
        self.bparm = BrainP
        self.conscienceNameExp="NAV"
        self.path = r'../../VaNN/public/stream'
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
            self.bestWay()
            self.isSearchingLogic()
            self.learnObjects()

    # ----------------------------------------------------------------------------------
    # LOGIC
    # ---------------------------------------------------------------------------------

    def bestWay(self):
        lMemory = self.bparm.Lmemory # type: lt.LongTerm
        if lMemory.bestWay.shape[0] > 0:
            isnav,navMind  = self.createConscienceExp()
            if isnav:
                lMemory.think(navMind.name,lMemory.bestWay)
    def trainBestWay(self):
        self.bparm.logLogicThread("training best way..")
        lMemory = self.bparm.Lmemory  # type: lt.LongTerm
        if lMemory.bestWay.shape[0] > 0:
            cv2.imwrite(self.path + '/image_stream_best.jpg', lMemory.bestWayO)
            isnav, navMind = lMemory.lookForConscience(self.conscienceNameExp)
            if isnav:
                print "picture best way...."
                lMemory.trainConscience(navMind.name,lMemory.bestWay)
    def trainBadWay(self):
        self.bparm.logLogicThread("training worst way..")
        lMemory = self.bparm.Lmemory  # type: lt.LongTerm
        if lMemory.bestWay.shape[0] > 0:
            cv2.imwrite(self.path + '/image_stream_bad.jpg', lMemory.bestWayO)
            isnav,c = lMemory.lookForConscience(self.conscienceNameExp)
            if isnav:
                print "picture bad way...."
                lMemory.addDataToTrain(lMemory.bestWay,1)

    def createConscienceExp(self):
        lMemory = self.bparm.Lmemory  # type: lt.LongTerm
        isnav,navMind = lMemory.lookForConscience(self.conscienceNameExp)
        if not isnav:
           lMemory.createConscience(self.conscienceNameExp,lMemory.bestWay.shape[1],3,100,2)
        return isnav,navMind


    def learnObjects(self):
        sMemory = self.bparm.Smemory # type: S.ShortTerm
        state = len(sMemory.Z) % 500
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
                #Primera derivada difgradiente
                difGrad = costdif/costdifAct
                antCost = cost
                costdif = costdifAct
                if i == 1:
                   costdifAct = cost
                   costdif = costdifAct
                if difGrad > 2:
                    isbreak = True
            self.bparm.sendDataSight()
            sMemory.clustering = False


    def isSearchingLogic(self):
        if self.bparm.RobotLife:
            if self.bparm.isSearching:
                lmemory = self.bparm.Lmemory # type: lt.LongTerm
                if not self.explore.exploreLogic.action:
                    try:
                        pred = lmemory.conscience.prediction
                        prob = lmemory.conscience.probability
                    except Exception,ex:
                        prob=0
                        pred=0
                    probTotal = prob * self.explore.exploreLogic.estimation
                    if prob==0:
                        pred = 0
                        probTotal = self.explore.exploreLogic.estimation
                    if  pred == 0 and probTotal >= self.bparm.PROBTOMOVE:
                        self.bparm.PROBTOMOVE = prob*0.5 if prob > 0 else self.bparm.PROBTOMOVE
                        self.isSearching = False
                        threading._sleep(0.5)
                        self.bparm.logLogicThread("###SEARCHED###")
                        self.bparm.logLogicThread(":::" + str(probTotal)+ ":::" +str(pred))
                        while len(self.explore.exploreLogic.tempMoves) == 0:
                            self.bparm.logLogicThread("waiting..")
                        self.bparm.actualAngle, self.bparm.actualDistance, self.bparm.actualEstimation = self.explore.exploreLogic.getAngleMaxDistanceTemp(self.explore.exploreLogic.tempMoves)
                        self.bparm.badActualAngle,distance, estimation = self.explore.exploreLogic.getAngleMinDistanceTemp(self.explore.exploreLogic.tempMovesBad)
                        self.bparm.logLogicThread(
                            str(self.bparm.actualAngle) + "$$" + str(self.bparm.actualDistance) + "$$" + str(self.bparm.actualEstimation))
                        self.bparm.logLogicThread(" rotation rate::: " + str(self.explore.exploreLogic.rotationRate))
                        self.bparm.error = self.bparm.actualDistance * 0.2
                        self.explore.exploreLogic.needOther = False
                        self.startMoving()
                    else:
                        self.explore.exploreLogic.action = True
                        self.explore.exploreLogic.needOther = True





    def startMoving(self):
        self.bparm.isTransition = True
        self.bparm.isMoving = True
        num = 0
        while self.bparm.isTransition:
            if self.bparm.isBadWay and num < 2:
                self.bparm.logLogicThread("waiting to train best way...")
                self.trainBadWay()
                num += 1
        self.trainBestWay()

    #----------------------------------------------------------------------------------------------
    # visual analitics
    #-----------------------------------------------------------------------------------------------

    def sendStatistics(self):
        self.bparm.sendDataVA()
        self.bparm.sendDataNnet()


