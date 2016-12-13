#Algoritmo de deteccion de triangulos
#Por Glar3
#
#
#Detecta triangulos azules
 
import cv2
import numpy as np
 
#Iniciar camara
captura = cv2.VideoCapture(0)

imagen = cv2.imread('p.jpg')
if(True):

   #Caputrar una imagen y convertirla a hsv
   #C_, imagen = captura.read()
   hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

   #Guardamos el rango de colores hsv (azules)
   bajos = np.array([100,100,100], dtype=np.uint8)
   altos = np.array([200, 200, 200], dtype=np.uint8)

   #Crear una mascara que detecte los colores
   mask = cv2.inRange(hsv, bajos, altos)

   #Filtrar el ruido con un CLOSE seguido de un OPEN
   kernel = np.ones((7,7),np.uint8)
   mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
   mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

   #Difuminamos la mascara para suavizar los contornos y aplicamos filtro canny
   blur = cv2.GaussianBlur(mask, (5, 5), 0)
   edges = cv2.Canny(mask,1,2)

   #Si el area blanca de la mascara es superior a 500px, no se trata de ruido
   img,contours, hier = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
   areas = [cv2.contourArea(c) for c in contours]
   i = 0
   for extension in areas:
      if extension > 600:
         actual = contours[i]
         approx = cv2.approxPolyDP(actual,0.05*cv2.arcLength(actual,True),True)
         if len(approx)==3:
            cv2.drawContours(imagen,[actual],0,(0,255,255),2)
            cv2.drawContours(mask,[actual],0,(0,255,255),2)
      i = i+1

   cv2.imshow('mask', mask)
   cv2.imshow('Camara', imagen)
   cv2.waitKey(0)
   #tecla = cv2.waitKey(5) & 0xFF
  #C if tecla == 27:
    #C  break

#Ccv2.destroyAllWindows()