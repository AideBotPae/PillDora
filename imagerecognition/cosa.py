from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import argparse
import cv2

kernel = np.ones((3,3), np.uint8)

# Imagen
original = cv2.imread("/home/paesav/PAET2019/PillDora/imagerecognition/imagenes/pills2.jpg")
#cv2.imshow("Imagen Original", original)

# Escala de grises
grises = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

# Suavizado Gaussiano
gauss = cv2.GaussianBlur(grises, (3,3), 0)

#cv2.imshow("suavizado", gauss)



shifted = cv2.pyrMeanShiftFiltering(original, 25, 180)
#cv2.imshow("erosion binariz", shifted)
erosion = cv2.erode(shifted, kernel, iterations=2)
#cv2.imshow("erosion", erosion)
TopHat = shifted-erosion
#cv2.imshow("TopHat", TopHat)


#gradient = cv2.morphologyEx(grises, cv2.MORPH_GRADIENT, kernel)
#cv2.imshow("gradient", gradient)

#shifted = cv2.pyrMeanShiftFiltering(gradient, 21, 80)

# Deteccion de bordes
canny = cv2.Canny(erosion, 50, 150)

cv2.imshow("canny", canny)

# Buscamos contornos
contours, image = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Output
print("Hay {} objetos".format(len(contours)))

cv2.drawContours(original,contours,-1,(0,0,255), 2)
#cv2.imshow("contornos", original)

#cv2.waitKey(0)
