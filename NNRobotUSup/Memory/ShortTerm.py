import Libraries.CLUSTER.KMeans as C
import NNRobotUSup.Entities.Item as I
import numpy as np

class ShortTerm:
    def __init__(self):
        self.kmeans = C.KmeansFunctions()
        self.clustering = False
        self.items = []
        self.itemsZip = np.array([])
        self.centersZip = np.array([])
        self.Z = []

    def Cluster(self,numk):
       cost =  self.kmeans.applyKM(self.Z,numk)
       self.itemsZip = self.kmeans.z
       self.centersZip = self.kmeans.center
       return cost

