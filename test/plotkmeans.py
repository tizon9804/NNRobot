while True:
    if self.Smemory.kmeans.plot:
        A = self.Smemory.kmeans.A
        B = self.Smemory.kmeans.B
        C = self.Smemory.kmeans.C
        D = self.Smemory.kmeans.D
        E = self.Smemory.kmeans.E
        F = self.Smemory.kmeans.F
        Z = self.Smemory.kmeans.z
        center = self.Smemory.kmeans.center
        # Plot the data
        plt.scatter(A[:, 0], A[:, 1])
        plt.scatter(B[:, 0], B[:, 1], c='r')
        plt.scatter(C[:, 0], C[:, 1], c='b')
        plt.scatter(D[:, 0], D[:, 1], c='y')
        plt.scatter(E[:, 0], E[:, 1], c='g')
        plt.scatter(F[:, 0], F[:, 1], c='r')
        plt.scatter(center[:, 0], center[:, 1], s=80, c='y', marker='s')
        plt.xlabel('Height'), plt.ylabel('Weight')
        plt.show()