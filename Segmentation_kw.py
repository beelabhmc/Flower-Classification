import numpy as np
import cv2
from matplotlib import pyplot as plt


# Watershed segmentation

img = cv2.imread('images/Research_May15_small.jpeg')
#img[:,:,0] = 0

#height, width, _ = img.shape
#for j in xrange(width):
#    for i in xrange(height):
#        img[i, j, 0] -= 160.75
#        img[i, j, 0] -= 140.25
#        img[i, j, 0] -= 126
#        
#        if img[i, j, 0] < 0:
#            img[i, j, 0] = 0
#        if img[i, j, 1] < 0:
#            img[i, j, 1] = 0
#        if img[i, j, 2] < 0:
#            img[i, j, 2] = 0


cv2.imwrite('images/RG.jpeg', img)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imwrite('images/gray2.jpeg', gray)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

cv2.imwrite('images/thresh.jpeg', thresh)

kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

cv2.imwrite('images/unknown.jpeg', unknown)
cv2.imwrite('images/sure_bg.jpeg', sure_bg)
cv2.imwrite('images/sure_fg.jpeg', sure_fg)

 # Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)
print markers

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]

cv2.imwrite('images/markers_orig.jpeg', img)

##cv2.
#
##159 119 83
##165 155 143
##168 147 130
##151 140 148
##
##160.75 140.25 126
#
## Subtraction of background + watershed
#height, width, channels = img.shape
#
#img2 = img
#
#for j in xrange(width):
#    for i in xrange(height):
#        img2[i, j, 0] -= 160.75
#        img2[i, j, 0] -= 140.25
#        img2[i, j, 0] -= 126
#        
#        if img2[i, j, 0] < 0:
#            img2[i, j, 0] = 0
#        if img2[i, j, 1] < 0:
#            img2[i, j, 1] = 0
#        if img2[i, j, 2] < 0:
#            img2[i, j, 2] = 0
#            
#cv2.imwrite('images/img2.jpeg', img2)