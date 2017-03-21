import cv2


class KmeansFunctions:
    def __init__(self):
        # Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        # Set flags (Just to avoid line break in the code)
        self.flags = cv2.KMEANS_RANDOM_CENTERS
        self.A = []
        self.B = []
        self.center = []
        self.plot = False

    def applyKM(self,Z,numK):
        # Apply KMeans
        ret, label, center = cv2.kmeans(Z, 6, None, self.criteria, 10, self.flags)

        self.A = Z[label.ravel() == 0]
        self.B = Z[label.ravel() == 1]
        self.C = Z[label.ravel() == 2]
        self.D = Z[label.ravel() == 3]
        self.E = Z[label.ravel() == 4]
        self.F = Z[label.ravel() == 5]
        self.z = Z
        self.center = center
        self.plot = True
        return (ret,label,center)