import Libraries.CLUSTER.KMeans as C
import NNRobotUSup.Entities.Item as I
import numpy as np

class ShortTerm:
    def __init__(self):
        self.kmeans = C.KmeansFunctions()
        self.items = []
        self.Z = []

    def Cluster(self):
        item = I.Item()

        for it in self.items:
            item=it
            self.Z.append([item.momCentral,item.momEspacial])
            Z = np.float32(self.Z)
        if Z.shape[0]>50:
            self.kmeans.applyKM(Z,10)

