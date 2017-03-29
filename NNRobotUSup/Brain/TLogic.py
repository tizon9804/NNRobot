import threading,time
import numpy as np

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
            self.bparm.logLogicThread("Thinking...")
            self.bparm.sendDataVA()
            self.bparm.sendDataSight()
            last_time, diffs, ips = self.bparm.ips(last_time, diffs);
            self.bparm.nlogic = ips
            self.isSearchingLogic()

    # ----------------------------------------------------------------------------------
    # LOGIC
    # ---------------------------------------------------------------------------------

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


