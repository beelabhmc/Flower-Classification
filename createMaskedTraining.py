# -*- coding: utf-8 -*-
import numpy as np
from Constants import * 
from MappingProject import *
import cv2
import os
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import shapely
from shapely.geometry import Polygon
from createTraining import tiledTraining


class Mask:
    image = None
    path = ""
    
    def __init__(self, image, path):
        self.image = image
        self.path = path
    
    def convertToBW(self, saveToFile=False):
        bw = cv2.threshold(self.image, 1, 255, cv2.THRESH_BINARY)[1]
        if saveToFile:
            newDir = os.path.join(os.path.dirname(self.path), "masks_bw")
            imgName = os.path.basename(self.path)
            if not os.path.exists(newDir):
                os.makedirs(newDir)
            cv2.imwrite(os.path.join(newDir, imgName), bw)
        self.image = bw

class CreateMaskedTraining:
    masks = {}
    mp = None
    
    def readMPFromFile(self, originalKml, stitchKml, stitchWidth, stitchHeight, scheme=False):
        self.mp = MappingProject()
        self.mp.readProjectKmlFiles(originalKml, stitchKml, stitchWidth, stitchHeight, scheme)
        
    def importMP(self, mappingProject):
        self.mp = mappingProject
        
    def readMasksFromXml(self, folderPath, save=False):
        self.masks = {}
        
        xmlPath = ""
        for filePath in os.listdir(folderPath):
            if filePath.endswith(".xml"):
                xmlPath = os.path.join(folderPath, filePath)
                
        tree = ET.parse(xmlPath)
        root = tree.getroot()
        obj = root.findall('object') #Find all of the masks    
        
        for mask in obj: #For each of these masks... 
            seg = mask.find('segm')
            if seg is None: 
                continue
                
            maskPath = os.path.join(folderPath, seg.find('mask').text)
            species = mask.find('name').text
            
            maskImg = cv2.imread(os.path.join(maskPath), cv2.IMREAD_GRAYSCALE)
            if maskImg is not None:
                newMask = Mask(maskImg, maskPath)
                newMask.convertToBW(saveToFile=save)
                self.masks[newMask] = species

    def tiledTraining(self, original, mask, overlap=0.2, n=50):
        mask3d = np.zeros_like(original)
        for i in xrange(3):
            mask3d[:, :, i] = mask.image
            
        x,y,w,h = cv2.boundingRect(mask.image)
        
        cv2.imwrite('images/maskss.jpg', mask.image)
            
        # apply the mask to your image
        maskedImg = cv2.bitwise_and(original, mask3d)
        cv2.imwrite('images/maskedImg.jpg', maskedImg)
    
        maskedImgCrop = maskedImg[y:(y+h), x:(x+w)]
        cv2.imwrite('images/maskedImgCropped.jpg', maskedImgCrop)
        
        return tiledTraining(['images/maskedImgCropped.jpg'], [self.masks[mask]], overlap, n, qualityCheck=True)
        
    
    def mainFunction(self):
        # find the cover
        # get training images
        
        # for every mask, 
        for mask in self.masks.iterkeys():
            # turn the mask into convex hull - done
        #    maskImg = mask.image
        #    maskPath = mask.path
        #    maskPoints = np.nonzero(maskImg)
        #    if len(maskPoints[0]) == 0:
        #        print maskPath + " is empty, skipping..."
        #        continue
        #        
        #    maskPoints = np.column_stack(maskPoints)
        #    hull = ConvexHull(maskPoints)
        #    hullBoundary = zip(maskPoints[hull.vertices, 1], maskPoints[hull.vertices, 0])
        #    hullBoundary.append(hullBoundary[0])
        #
        #    # find the set of originals that intersect with the convex hull mask
        #    overlappingOriginals = []
        #    for original in self.mp.originals:
        #        originalProj = self.mp.originalCornerInStitch(original)
        #        originalPolygon = Polygon(originalProj)
        #        maskPolygon = Polygon(hullBoundary)
        #        intersection = originalPolygon.intersection(maskPolygon)
        #        
        #        if not intersection.is_empty:
        #            overlappingOriginals.append(original)
        #    
        #    print maskPath
        #    print overlappingOriginals
        #    
            
            # while the mask is none-empty
                # find the original image that has the largest intersection area
                # with the current mask
                # get the mask from the original image space
                # update mask
                
            # make sliding windows for each fraction of mask
            originalImg = cv2.imread("images/Research_May15_small.jpeg")
            self.tiledTraining(originalImg, mask)
                
            break

        
        # return the training images
        return None

mt = CreateMaskedTraining()
mt.readMPFromFile("stitchTest/footprints.kml", "stitchTest/stitched footprint.kml", 2726, 2695)
mt.readMasksFromXml("images/research_may15")
mt.mainFunction()

#plt.plot(maskPoints[:,1], maskPoints[:,0], 'o')
#plt.plot(maskPoints[hull.vertices,1], maskPoints[hull.vertices,0], 'r--', lw=2)
#plt.show()