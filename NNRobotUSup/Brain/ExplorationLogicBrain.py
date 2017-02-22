import Libraries.RobotSystem.Robot as R

class Explore:
    def __init__(self,thread):
        try:
            print thread + "init Explore"
            self.robotSystem = R.RobotDriver()
            self.RobotStarted = True
        except Exception as ex:
            print thread + "Cannot connect to Robot:" + ex
            self.RobotStarted = False
