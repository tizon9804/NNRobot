import threading
import ExplorationLogicBrain as ELB
import time
class Explore:
    def __init__(self,BrainP):
        self.bparm = BrainP
        time.sleep(5)
        tExplore = threading.Thread(target=self.loopExplore)
        tExplore.start()

    def loopExplore(self):
        self.bparm.logExploreThread("thread started...")
        self.exploreLogic = ELB.Explore(self.bparm.explore,self.bparm.debugExploreLogic,self.bparm.debugRobotSystem,self.bparm.isVideoStreaming,self.bparm)
        last_time = time.clock()
        diffs = []
        while self.bparm.exploreLife:
            # register iterations per second
            self.bparm.logExploreThread("exploring...")
            last_time, diffs, ips = self.bparm.ips(last_time, diffs);
            self.bparm.nexplore = ips
            self.bparm.RobotLife = self.exploreLogic.RobotStarted
            if self.bparm.RobotLife:
                try:
                    self.bparm.laserData, self.bparm.posData = self.exploreLogic.robotSystem.getLaserBuffer()
                except Exception,ex:
                    print "ErrorLaserBuffer loopExplore $$$$",str(ex)
                    #self.bparm.exploreLife = False
                self.searchDirection()
                self.move()

    # ----------------------------------------------------------------------------------
    # EXPLORE
    # ---------------------------------------------------------------------------------

    def searchDirection(self):
        if self.bparm.isSearching:
            # search a possible direction to move, it do not cares the range of distance
            self.exploreLogic.searchDirection()
            self.bparm.logExploreThread(str(self.bparm.PROBTOMOVE))
            # think best way with the nnet return 0-1 where 1 is a secure way

    def move(self):
        if self.bparm.isMoving:
            if self.bparm.isTransition:
                self.badAngle()
                self.inTransition()
            self.bparm.logExploreThread("moving robot" + str(self.bparm.actualDistance - self.bparm.error))
            self.exploreLogic.move(self.bparm.actualDistance - self.bparm.error)
            threading._sleep(2)
            self.bparm.logLogicThread("FINISHING MOVE")
            self.bparm.actualAngle = 0
            self.bparm.actualDistance = 0
            self.bparm.isMoving = False
            self.bparm.isSearching = True
            # track route could be saved in middleterm(graph)

    def inTransition(self):
        self.bparm.logExploreThread("in transition")
        self.exploreLogic.estimation = 0
        print "Best way for laser::", self.bparm.actualAngle, ":::", self.bparm.actualDistance, "PROBTOMOVE::", self.bparm.PROBTOMOVE
        self.exploreLogic.transitionMove(self.bparm.actualAngle)
        self.bparm.isTransition = False

    def badAngle(self):
        self.exploreLogic.transitionMove(self.bparm.badActualAngle)
        self.bparm.isBadWay = True
        threading._sleep(5)
        self.bparm.isBadWay = False



