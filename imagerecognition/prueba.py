# USAGE
# python watershed.py --image images/coins_01.png

# import the necessary packages
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#	help="path to input image")
#args = vars(ap.parse_args())


# Imagen
original = cv2.imread('/home/paesav/PAET2019/PillDora/imagerecognition/imagenes/pills2.jpg')

# Escala de grises
grises = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
 
# Suavizado Gaussiano
gauss = cv2.GaussianBlur(grises, (17,17), 0)
 
# Deteccion de bordes
canny = cv2.Canny(gauss, 70, 150)
 
# Buscamos contornos
contours, image = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(original,contours,-1,(0,0,0), 3)
#cv2.imshow("contornos", original)

# load the image and perform pyramid mean shift filtering
# to aid the thresholding step
image = original
shifted = cv2.pyrMeanShiftFiltering(image, 21, 80)

# convert the mean shift image to grayscale, then apply
# Otsu's thresholding

gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#MEDIDA PA CAMBIAR DE COLOR SI SE DETECTAN POCOS NEGROS (pastillas negras y fondo blanco)
height, width = thresh.shape
if cv2.countNonZero(thresh) > height*width/2:
	thresh = cv2.bitwise_not(thresh)


# compute the exact Euclidean distance from every binary
# pixel to the nearest zero pixel, then find peaks in this
# distance map
D = ndimage.distance_transform_edt(thresh)
localMax = peak_local_max(D, indices=False, min_distance=20,
	labels=thresh)

# perform a connected component analysis on the local peaks,
# using 8-connectivity, then appy the Watershed algorithm
markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=thresh)
print("Se han detectado {} pastillas".format(len(np.unique(labels)) - 1))

