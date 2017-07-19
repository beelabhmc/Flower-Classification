from MappingProject import *
import cv2
from collections import Counter
import numpy as np


output = np.zeros((1455,1308,3), np.uint8)

mp = MappingProject()
mp.readProjectKmlFiles("stitchTest/footprints-agi.kml", "stitchTest/extrapolationOrtho.kml", 8725, 6814)
img162 = cv2.imread('images/stitchTest/DJI_0162_class.png')
img163 = cv2.imread('images/stitchTest/DJI_0163_class.png')
img169 = cv2.imread('images/stitchTest/DJI_0169_class.png')
img170 = cv2.imread('images/stitchTest/DJI_0170_class.png')
#stitch = cv2.imread('images/stitchTest/extrapolationOrtho.jpg')

for i in xrange(5527, 6835):
    print i
    for j in xrange(3010, 4465):
        pointIn162 = mp.stitchToOriginal("DJI_0162.JPG", i, j)
        pointIn163 = mp.stitchToOriginal("DJI_0163.JPG", i, j)
        pointIn169 = mp.stitchToOriginal("DJI_0169.JPG", i, j)
        pointIn170 = mp.stitchToOriginal("DJI_0170.JPG", i, j)
        
        pixels = []
        
        if pointIn162 != None:
            pixels += [tuple(img162[pointIn162[1]-1, pointIn162[0]-1])]
        if pointIn163 != None:
            pixels += [tuple(img163[pointIn163[1]-1, pointIn163[0]-1])]
        if pointIn169 != None:
            pixels += [tuple(img169[pointIn169[1]-1, pointIn169[0]-1])]
        if pointIn170 != None:
            pixels += [tuple(img170[pointIn170[1]-1, pointIn170[0]-1])]
            
        c = Counter(pixels)
        common = c.most_common()
        if common != []:
            vote, _ = common[0]
            output[j-3010, i-5527] = vote
            
cv2.imwrite('output3.jpg', output)       