# import the necessary packages
#from picamera.array import PiRGBArray
#from picamera import PiCamera
from docutils.nodes import image

import NNRobotUSup.Network.ServerVideoStream as server
import time
import cv2
import numpy as np
import NNRobotUSup.Network.Routes as ro
import NNRobotUSup.Entities.Item as I

class Camera:
    def __init__(self,isVideoStream,Smemory):
        self.Smemory = Smemory
        self.image = []
        self.moments=[]
        self.debugNetwork = False
        self.net = ro.Network(self.debugNetwork)
        self.isVideoStream = isVideoStream
        if isVideoStream:
            self.server= server.VideStream()
        else:
            # initialize the camera and grab a reference to the raw camera capture
            camera = PiCamera()
            camera.resolution = (640, 480)
            camera.framerate = 30
            #dark
            #camera.framerate = Fraction(1, 6)
            #camera.shutter_speed = 6#000000
            #camera.exposure_mode = 'off'
            camera.iso = 800
            #camera.image_effect = 'emboss'
            camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2017 GSC'
            self.rawCapture = PiRGBArray(camera)
            # allow the camera to warmup
            time.sleep(0.1)
            self.camera = camera

    def getImage(self):
        if self.isVideoStream:
            img = self.netCapture()
        else:
            img = self.raspCapture()
        return img

    def raspCapture(self):
        # capture frames from the camera
        self.camera.capture(self.rawCapture, "bgr")
        # print 'Captured image: ', self.rawCapture.array.shape
        image =  self.rawCapture.array
        # cv2.imshow("Frame", self.image)
        # key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        self.rawCapture.truncate(0)
        return image

    def netCapture(self):
        if self.server.isVideoActive:
            img =  self.server.getImage()
        else:
            img =  self.server.acceptVideo()
        return img

    def show(self,image):
        try:
            cv2.imshow("EYES",image)
            key = cv2.waitKey(1) & 0xFF
        except Exception as ex:
            print "SENSE: SHOW error ",str(ex)

    def contours(self,img):
        imgRGB = img.copy()
        self.img = img
        self.imFilt = img
        self.gaussianBlur(False)
        self.gray(False)
        self.laplacian(True)
        self.gaussianBlur(False)
        self.convolution(False)
        self.medianBlur(False)
        self.bilateralFilter(False)
        self.medianBlur(False)
        self.bilateralFilter(True)
        self.cannyEdges(True)
        self.img = self.imFilt
        # encuentra los contornos de los bordes
        im2, contours, hierarchy = cv2.findContours(self.imFilt.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        #recorre cada contorno el cual es un potencial objeto
        for contour in contours:
            cnt = contour
            #delimita el contorno por medio de ptron hull ver opencv
            hull = cv2.convexHull(cnt)
            #delimita el contorno con un rectangulo
            rect = cv2.minAreaRect(cnt)
            w,h=rect[1]
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            max = 320
            min = 100
            # obtiene el objeto del contorno que cumplen con rango de tamno
            if w>=min and h>=min and w<=max and h<=max:
                #obtiene los pedasos de imagenes, se realiza un proceso de descripcion
                self.obtainPieceOfImage(cnt,rect,imgRGB,self.img,i)
                #dibuja sobre la imagen los contornos en forma de rectangulo y hull encontrados
                cv2.drawContours(img,[box], -1, (114, 224, 150),2)
                cv2.drawContours(img, [hull], -1, (207, 252, 232), 1)
            i += 1
        #filtro que elimina el color de to_do lo que no es un controno
        self.floodImage(self.img,img,0)
        cv2.imshow("Contours", img)
        cv2.waitKey(1)

    def obtainPieceOfImage(self,cnt, rect,imageRGB, imgCont, i):
        #obtiene la matriz de rotacion del rect que senala un objeto
        rotMatrix = cv2.getRotationMatrix2D(rect[0], rect[2], 1.0)
        #rota la imagen con respecto ala matriz de rotacion
        rotated = cv2.warpAffine(imgCont, rotMatrix, imgCont.shape[:2], cv2.INTER_CUBIC)
        rotatedRGB = cv2.warpAffine(imageRGB, rotMatrix, (640,480), cv2.INTER_CUBIC)
        w, h = rect[1]
        size = (int(w), int(h))
        #corta la imagen rotada con respecto a las cordenadas y tamano de la imagen
        cropImage = cv2.getRectSubPix(rotated, size, rect[0])
        cropImageRGB = cv2.getRectSubPix(rotatedRGB, size, rect[0])
        self.describeImage(cnt,cropImage,cropImageRGB,i)


    def describeImage(self,cnt,cropimage,imageColor,i):
        floodImg = self.floodImage(cropimage,imageColor,1)
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
        self.addItems(item)
        self.addMoments(item.momCentral, item.momEspacial, item.compacity)

    def floodImage(self,cropimage,imageColor,i):
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
        #todo calcular la posicion x,y del objeto
        #cv2.calcOpticalFlowPyrLK()
        cv2.imshow("im_floodfill_inv"+str(i), im_floodfill_inv)
        cv2.waitKey(1)
        cv2.imshow("floodimg"+str(i), floodimg)
        cv2.waitKey(1)
        cv2.imshow("rgb"+str(i), imgCrop)
        cv2.waitKey(1)
        return imgCrop

    def addMoments(self,x,y,object):
        self.moments.append({"x": x, "y": y, "range": object})

    def addItems(self,item):
        self.Smemory.items.append(item)
        self.Smemory.itemsZip.append(
            {"C":item.compacity,
             "ME":item.momEspacial,
             "MC":item.momCentral,
             "MC2":item.momCentral2,
             "MR":item.meanRed,
             "MG":item.meanGreen,
             "MB":item.meanBlue})
        self.Smemory.Cluster()


    def gaussianBlur(self,show):
        self.img = self.imFilt
        self.imFilt = cv2.GaussianBlur(self.img, (7, 7), 0)
        if show:
            cv2.imshow("GaussianBlur", self.imFilt)
            cv2.waitKey(1)

    def gray(self,show):
        self.img = self.imFilt
        self.imFilt = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        if show:
            cv2.imshow("COLOR_BGR2GRAY", self.imFilt)
            cv2.waitKey(1)

    def laplacian(self,show):
        self.img = self.imFilt
        dst = cv2.Laplacian(self.img, ddepth=cv2.CV_16S,
                            scale=2, delta=200, ksize=5, borderType=cv2.BORDER_CONSTANT)
        self.imFilt = cv2.convertScaleAbs(dst)
        if show:
            cv2.imshow("Laplacian", self.imFilt)
            cv2.waitKey(1)

    def medianBlur(self,show):
        self.img = self.imFilt
        self.imFilt = cv2.medianBlur(self.img, 5)
        if show:
            cv2.imshow("medianBlur", self.imFilt)
            cv2.waitKey(1)

    def bilateralFilter(self,show):
        self.img = self.imFilt
        self.imFilt = cv2.bilateralFilter(self.img, 10, 17, 17)
        if show:
            cv2.imshow("bilateralFilter", self.imFilt)
            cv2.waitKey(1)

    def convolution(self,show):
        self.img = self.imFilt
        kernel = np.ones((5, 5), np.float32) / 25
        self.imFilt = cv2.filter2D(self.img, -1, kernel)
        if show:
            cv2.imshow("convolution", self.imFilt)
            cv2.waitKey(1)

    def cannyEdges(self,show):
        self.img = self.imFilt
        self.imFilt = cv2.Canny(self.img, 0, 50)
        if show:
            cv2.imshow("edges1", self.imFilt)
            cv2.waitKey(1)


