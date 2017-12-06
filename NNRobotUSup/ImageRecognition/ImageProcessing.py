import numpy as np
import NNRobotUSup.Entities.Item as I
from NNRobotUSup.Memory import LongTerm as lt
import NNRobotUSup.Network.FtpSender as ftp
import cv2


class IMprocess:
    def __init__(self, Smemory, Lmemory,ftpSender):
        self.Lmemory = Lmemory # type: lt.LongTerm
        self.Smemory = Smemory
        self.ftpSender = ftpSender #type: ftp.FtpSender
        self.bestWay = []
        self.image = []
        self.moments = []
        self.tami=0
        self.path = r'../../VaNN/public/stream'
        self.path2 = '../../VaNN/public/stream'

    def contours(self, img):
        imgRGB = img.copy()
        self.img = img
        self.imFilt = img
        # self.gaussianBlur(False)
        self.gray(True)
        self.Lmemory.newImage(img)
        self.laplacian(True)
        self.gaussianBlur(False)
        # self.convolution(False)
        self.medianBlur(False)
        self.bilateralFilter(False)
        # self.medianBlur(False)
        # self.bilateralFilter(False)
        self.cannyEdges(True)
        self.img = self.imFilt
        # encuentra los contornos de los bordes
        im2, contours, hierarchy = cv2.findContours(self.imFilt.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        if not self.Smemory.clustering:
            # recorre cada contorno el cual es un potencial objeto
            for contour in contours:
                cnt = contour
                # delimita el contorno por medio de ptron hull ver opencv
                hull = cv2.convexHull(cnt)
                # delimita el contorno con un rectangulo
                rect = cv2.minAreaRect(cnt)
                w, h = rect[1]
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                max = 10000
                min = 5000
                area = w * h
                # obtiene el objeto del contorno que cumplen con rango de tamno
                if area < max and area > min and h > 50 and w > 50:
                    # obtiene los pedasos de imagenes, se realiza un proceso de descripcion
                    flood = self.obtainPieceOfImage(cnt, rect, imgRGB, self.img, i)
                    #cv2.imshow("rgb" + str(0), flood)
                    #cv2.cvWaitKey()
                    # dibuja sobre la imagen los contornos en forma de rectangulo y hull encontrados
                    cv2.drawContours(img, [box], -1, (114, 224, 150), 2)
                    cv2.drawContours(img, [hull], -1, (207, 252, 232), 1)
                i += 1
            # filtro que elimina el color de to_do lo que no es un controno
            self.floodImage(self.img, img, 0)
        #cv2.imshow("Contours", img)
        #cv2.waitKey(2)
        self.ftpSender.upload(img, 'image_stream')
        #cv2.imwrite(self.path + '/image_stream' + str(self.tami) + '.jpg', img)
        self.tami += 1




    #591337812
    def obtainPieceOfImage(self, cnt, rect, imageRGB, imgCont, i):
        # obtiene la matriz de rotacion del rect que senala un objeto
        rotMatrix = cv2.getRotationMatrix2D(rect[0], rect[2], 1.0)
        # rota la imagen con respecto ala matriz de rotacion
        rotated = cv2.warpAffine(imgCont, rotMatrix, imgCont.shape[:2], cv2.INTER_CUBIC)
        rotatedRGB = cv2.warpAffine(imageRGB, rotMatrix, (640, 480), cv2.INTER_CUBIC)
        w, h = rect[1]
        size = (int(w), int(h))
        # corta la imagen rotada con respecto a las cordenadas y tamano de la imagen
        cropImage = cv2.getRectSubPix(rotated, size, rect[0])
        cropImageRGB = cv2.getRectSubPix(rotatedRGB, size, rect[0])
        flood = self.describeImage(cnt, cropImage, cropImageRGB, i)
        return flood

    def describeImage(self, cnt, cropimage, imageColor, i):
        floodImg = self.floodImage(cropimage, imageColor, 1)
        item = I.Item
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        if area == 0:
            item.compacity = 0
        else:
            item.compacity = (np.power(perimeter, 2) / area)
        M = cv2.moments(cnt)
        item.momEspacial = M['m00']
        item.momCentral = M['mu20']
        item.momCentral2 = M['mu02']
        meanRGB = cv2.mean(floodImg)
        item.meanRed = meanRGB[2]
        item.meanGreen = meanRGB[1]
        item.meanBlue = meanRGB[0]
        self.addItems(item,floodImg)
        self.addMoments(item.momCentral, item.momEspacial, item.compacity)
        return floodImg

    def floodImage(self, cropimage, imageColor, i):
        floodimg = cropimage.copy()
        h, w = floodimg.shape[:2]
        # se crea una mascara de 0 (blanco)
        mask = np.zeros((h + 2, w + 2), np.uint8)
        # se rellena la forma extrerior del objeto con un mismo color blanco
        cv2.floodFill(floodimg, mask, (0, 0), 255)
        # obtiene la inversa de la mascara para que el objeto quede de color blanco
        im_floodfill_inv = cv2.bitwise_not(floodimg)
        # se obtiene el color RGB de la imagen del objeto generado por la mascara
        imgCrop = cv2.bitwise_and(imageColor, imageColor, mask=im_floodfill_inv)
        # todo calcular la posicion x,y del objeto
        # cv2.calcOpticalFlowPyrLK()
        # cv2.imshow("im_floodfill_inv"+str(i), im_floodfill_inv)
        # cv2.waitKey(1)
        # cv2.imshow("floodimg"+str(i), floodimg)
        # cv2.waitKey(1)
        return imgCrop

    def addMoments(self, x, y, object):
        self.moments.append({"x": x, "y": y, "range": object})

    def addItems(self, item,img):
        self.Smemory.items.append(item)
        self.Smemory.Z.append(
            [item.meanRed,
             item.meanGreen,
             item.meanBlue])
        tam = len(self.Smemory.Z)
        cv2.imwrite(self.path + '/image_stream_object_' + str(tam) + '.jpg', img)
        #self.ftpSender.upload(img, 'image_stream_object_'+str(tam))

    def gaussianBlur(self, show):
        self.img = self.imFilt
        self.imFilt = cv2.GaussianBlur(self.img, (7, 7), 0)
        #if show:
         #   cv2.imshow("GaussianBlur", self.imFilt)
          #  cv2.waitKey(1)

    def gray(self, show):
        self.img = self.imFilt
        self.imFilt = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        #if show:
         #   self.ftpSender.upload(self.imFilt, 'image_stream_gray')
          #  cv2.waitKey(1)

    def laplacian(self, show):
        self.img = self.imFilt
        dst = cv2.Laplacian(self.img, ddepth=cv2.CV_16S,
                            scale=2, delta=200, ksize=3, borderType=cv2.BORDER_CONSTANT)
        self.imFilt = cv2.convertScaleAbs(dst)
        #if show:
            #self.ftpSender.upload(self.imFilt, 'image_stream_laplacian')
           # cv2.waitKey(1)

    def medianBlur(self, show):
        self.img = self.imFilt
        self.imFilt = cv2.medianBlur(self.img, 5)
        #if show:
           # cv2.imshow("medianBlur", self.imFilt)
          #  cv2.waitKey(1)

    def bilateralFilter(self, show):
        self.img = self.imFilt
        self.imFilt = cv2.bilateralFilter(self.img, 10, 17, 17)
        #if show:
         #   cv2.imshow("bilateralFilter", self.imFilt)
          #  cv2.waitKey(1)

    def convolution(self, show):
        self.img = self.imFilt
        kernel = np.ones((5, 5), np.float32) / 25
        self.imFilt = cv2.filter2D(self.img, -1, kernel)
        #if show:
         #   cv2.imshow("convolution", self.imFilt)
          #  cv2.waitKey(1)

    def cannyEdges(self, show):
        self.img = self.imFilt
        self.imFilt = cv2.Canny(self.img, 0, 30)
        #if show:
            #self.ftpSender.upload(self.imFilt, 'image_stream_canny')
          #  cv2.waitKey(1)
