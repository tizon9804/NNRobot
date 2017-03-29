import Libraries.CLUSTER.KMeans as C
import NNRobotUSup.Entities.Item as I
import numpy as np

class ShortTerm:
    def __init__(self):
        self.kmeans = C.KmeansFunctions()
        self.items = []
        self.itemsZip = []
        self.Z = []

    def Cluster(self,numk):
       return self.kmeans.applyKM(self.Z,numk)

