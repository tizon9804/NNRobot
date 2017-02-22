from NNRobotUSup.Memory import LongTerm as lt
import ExplorationLogicBrain as ELB
import NNRobotUSup.ImageRecognition.SightSense as sight
import threading


class LogicBrain:
    def __init__(self):
        self.logicLife = True
        self.senseLife = True
        self.exploreLife = True
        self.RobotLife = False
        self.targetList = []
        self.longTerm = lt.LongTerm()
        # init in new thread the part of the brain that take decisions
        tLogic = threading.Thread(target=self.loopLogic)
        tLogic.start()
        # init in new thread the part of the brain that take the sensors
        tSense = threading.Thread(target=self.loopSense)
        tSense.start()
        # init in new thread the part of the brain that have actuators
        tExplore = threading.Thread(target=self.loopExplore)
        #tExplore.start()

    def loopLogic(self):
        self.logic = "Logic"
        self.logLogicThread("thread started...")

    def loopSense(self):
        self.sense = "Sense"
        self.logSenseThread("thread started...")
        self.sight = sight.SightSense()
        while self.senseLife:
            self.sight.getRoute()
            if self.RobotLife:
                self.logSenseThread("sense laser:" + str(self.RobotLife))

    def loopExplore(self):
        self.explore = "Explore"
        self.logExploreThread("thread started...")
        self.exploreLogic = ELB.Explore(self.explore)
        while self.exploreLife:
            self.RobotLife = self.exploreLogic.RobotStarted

    def logLogicThread(self, message):
        print self.logic + ": " + message

    def logSenseThread(self, message):
        print self.sense + ": " + message

    def logExploreThread(self, message):
        print self.explore + ": " + message
