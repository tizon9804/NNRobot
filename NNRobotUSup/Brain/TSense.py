import threading
import time
class Sense:
    def __init__(self,BrainP):
        self.bparm = BrainP
        tSense = threading.Thread(target=self.loopSense)
        tSense.start()

    def loopSense(self):
        self.bparm.logSenseThread("thread started...")
        last_time = time.clock()
        diffs = []
        while self.bparm.senseLife:
            #register iterations per second
            last_time, diffs, ips = self.bparm.ips(last_time, diffs);
            self.bparm.nimage = ips
            #self.bparm.logSenseThread("transmiting...")
            self.bparm.sight.see()
            #time.sleep(0.5)

