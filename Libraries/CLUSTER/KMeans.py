import cv2
import numpy as np


class KmeansFunctions:
    def __init__(self):
        # Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 1.0)
        # Set flags (Just to avoid line break in the code)
        self.flags = cv2.KMEANS_RANDOM_CENTERS
        self.center = []
        self.labels = []
        self.z = []

    def applyKM(self,Z,numK):
        Z = np.float32(Z)
        # Apply KMeans
        #compress data to 2 dimensions PCA
        mean, eigvectors = cv2.PCACompute(np.transpose(Z), mean=np.array([]), maxComponents=2)
        reduce = np.transpose(eigvectors)
        #execute kmean with de data reduce
        ret, label, center = cv2.kmeans(reduce, numK, None, self.criteria, 100, self.flags)
        self.labels = np.array([label.ravel()])
        #append compress data with result labels
        self.z = np.append(reduce,self.labels.T,1)
        self.center = center
        return ret