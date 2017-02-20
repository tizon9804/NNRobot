from NNRobotUSup.Memory import LongTerm as lt
import threading


class LogicBrain:
    def __init__(self):
        self.targetList = []
        self.longTerm = lt.LongTerm()
        # init in new thread the part of the brain that take decisions
        tLogic = threading.Thread(target=self.loopLogic())
        tLogic.start()
        # init in new thread the part of the brain that take the sensors
        tSense = threading.Thread(target=self.loopSense())
        tSense.start()
        # init in new thread the part of the brain that have actuators
        tExplore = threading.Thread(target=self.loopExplore())
        tExplore.start()

    def loopLogic(self):
        todo = True

    def loopSense(self):
        todo = True

    def loopExplore(self):
        todo = True
