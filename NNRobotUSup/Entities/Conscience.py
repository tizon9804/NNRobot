from Libraries.NNET import NNCostFunction as nncost
import numpy as np

class Conscience:
    def __init__(self,id,name,data,persistence):
        self.name = name
        self.id = id
        self.mind = data
        self.isInitNN = False
        self.elements = np.array([])
        self.y = np.array([])
        self.persistence = persistence

    def initNN(self):
        if not self.isInitNN:
            try:
                win, wt, wout = self.persistence.state[self.name]
                self.win = win
                self.wt = wt
                self.wout = wout
                self.costgrads = nncost.costGrads(self.mind.thetain, self.mind.hiddenTheta, self.mind.thetaout)
                self.costgrads.setState(win, wt, wout)
                self.costgrads.createFunction()
                self.isInitNN = True
            except Exception,ex:
                print "Error: ", str(ex)
                self.isInitNN = False

    def collectDataImg(self, cap, init):
        if self.persistence.loadDataSet():
            self.X, self.y = self.persistence.dataset
            print "data loaded"
            save = True
            while (cap.isOpened()):
                init.convImage()
                X = init.convImg
                # X = X.reshape(1,X.shape[1]*X.shape[2]*X.shape[3])
                # X = X.reshape(1,X.shape[0]*X.shape[1])
                thread = threading.Thread(target=init.drawImage("todo", init.img))
                thread.start()
                if cv2.waitKey(1) & 0xFF == ord('z'):
                    break
                self.addDataToTrain(X, y, position)
            cv2.destroyAllWindows()
            print "saving..."
        if save:
            self.persistence.saveElements(self.elements)
            self.persistence.saveDataSet([self.X, self.y])
