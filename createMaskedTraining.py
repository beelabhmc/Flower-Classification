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
from PIL import Image 
import ImageProcess as IP


class CreateMaskedTraining:
    """
    The Class Module for creating training data from masks and an original image.
    Please create an instance of this class before calling the utility methods.
    
    Attributes:
        masks: a list of mask objects (class is defined as below)
        mp: corresponding instance of MappingProject class
        originalPath: path for the original image to apply the masks on
    """
    
    class Mask:
        """
        The Mask Class for pure convenience.
        """
        def __init__(self, path, species):
            self.path = path
            self.species = species
    
    masks = []
    mp = None
    originalPath = ""
      
                 
    def readMP(self, mappingProject):
        """
        Reading an MappingProject object
        """
        self.mp = mappingProject
        
        
    def readMasksFromXml(self, folderPath):
        """
        Read the masks from the .xml file. The masks and .xml file should be in the
        same folder.
        NOTE: the species here are NOT converted to shorthands or numerical value. 
        i.e: Pestemon spectabilis, not PESP or "3".
        
        Args:
            folderPath: the folder containing all the masks and .xml file
        """
        self.masks = []
        
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
            
            maskImg = cv2.imread(maskPath, cv2.IMREAD_GRAYSCALE)
            # If the mask is not empty, then create a Mask object and save to self
            if maskImg is not None:
                jpgPath = self.readColorPNGMask(maskPath)
                newMask = Mask(jpgPath, species)
                self.masks.append(newMask)

    
    def readColorPNGMask(self, path):
        """
        This is a helper function that reads in a color mask file (in .png), 
        convert it into bw image and save to .jpg at the same location.
        
        Args:
            path: location of the color mask.
            
        Returns:
            location of the converted .jpg bw mask.
        """
        # Skip if the file is not in .png format
        if not path.endswith(".png"):
            return None
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        bw = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)[1]
        newpath = path[:-3] + "jpg"
        cv2.imwrite(newpath, bw)
        return newpath
    
    
    def readColorPNGMasks(self, maskList):
        """
        This function does the same job as readColorPNGMask(^), but process .png
        files in batches.
        
        Args:
            maskList: a list of paths of the color mask.
            
        Returns:
            a list of the .jpg paths.
        """
        jpgPaths = []
        for path in maskList:
            jpgPath = self.readColorPNGMask(path)
            if jpgPath is not None:
                jpgPaths.append(jpgPath)
        return jpgPaths
            

    def tiledTraining(self, originalPath, maskList, speciesList, overlap=0.2, n=50):
        """
        This function creates training data by tiling up masked images.
        
        Args:
            originalPath: path to the original image to apply masks on
            maskList: a list of paths to the masks. These masks are already in 1D bw format.
            speciesList: a list of species, corresponding to each mask in the previous argument
            overlap: default 0.2
            n: default 50
            
        Returns:
            allMetrics: a list of metrics of every tile. Can be fed into training directly.
            allSpecies: a list of species of every tile.
        """
        allMetrics = []
        allSpecies = []
            
        original = cv2.imread(originalPath)
        
        for k in xrange(len(maskList)):
            # here we assume masks are already transformed into 1d bw images.
            maskPath = maskList[k]
            mask = cv2.imread(maskPath, cv2.IMREAD_GRAYSCALE)
            mask3d = np.zeros_like(original)
            for i in xrange(3):
                mask3d[:, :, i] = mask   # creating a 3d mask 
            
            # finding the rectangle bounding box of this mask
            x,y,w,h = cv2.boundingRect(mask)
                
            # apply the mask to the original image
            maskedImg = cv2.bitwise_and(original, mask3d)
        
            # maskedImgCrop: the mask applied to the original image, then cropped according
            # to the rectangle bounding box found above.
            # imgCrop: the original image cropped according to the rectangle bounding box.
            maskedImgCrop = Image.fromarray(maskedImg[y:(y+h), x:(x+w)])
            imgCrop = Image.fromarray(original[y:(y+h), x:(x+w)])
            
            metric, species = self.tiledTrainingHelper(maskedImgCrop, imgCrop, speciesList[k], overlap, n)

            allMetrics += metric
            allSpecies += species
        return allMetrics, allSpecies


    def tiledTrainingHelper(self, maskedImgCrop, croppedImg, species, overlap, n, qualityCheck=True): 
        """
        This function creates tiles from cropped masked images, then run optional quality check to see if 
        that at least 50% of each tile is the species of interest. If this tile passes the quality
        check, it will find the corresponding tile from the cropped original image and calculate the
        metrics.
        
        Args:
            maskedImgCrop: original image + mask, cropped
            croppedImg: the original image, cropped
            species: the corresponding species
            overlap:
            n:
            qualityCheck: default True. 
            
        Returns:
            a bunch of metrics and species, corresponding to tiles generated from the input mask.
        """ 
        count = 0
        imMetrics = [] #keep track of metrics for this image seperatly. 
        #Find the size of the image. 
        size = maskedImgCrop.size
        
        width = size[0] #pull out length and width 
        length = size[1] 
        smallTileSize = int(overlap*n) #Set the tilesize and overlap you want to train on. This should match the size you will test on. 
        # Extract all tiles using a specific overlap (overlap depends on n). This happens for each image.
        for k in range(0,width -smallTileSize, smallTileSize): #Go through the entire image 
            for j in range(0, length - smallTileSize, smallTileSize): 
                box = (k,j,k+smallTileSize, j+smallTileSize)  #edge coordinates of the current rectangle. 
                maskedTile = maskedImgCrop.crop(box) #pull out the desired rectangle from masked image.
                tile = croppedImg.crop(box)          #pull out the desired rectangle from origiinal image.
                if qualityCheck:
                    colorPixels = sum(maskedTile.point(lambda x: 1 if x else 0)
                                    .convert("L")
                                    .point(bool)
                                    .getdata())
                    if float(colorPixels) / (smallTileSize ** 2) < MASK_TRAINING_QUALITY:
                        continue
                        
                    #maskedTile.save("images/tiles/qualitytile_" + str(count) + ".jpg", "JPEG")
                    #tile.save("images/tiles/qualitytile_original_" + str(count) + ".jpg", "JPEG")
                    count += 1
                                    
                ### METRIC CALCULATIONS: Get the metrics for each subrectangle in the image. 
                    Metrics = IP.getMetrics(tile) #calculate all of the metrics on this cropped out image. 
                    imMetrics += [Metrics] #add these metrics to a list, imMetrics, that will keep track of metrics within each image. 
        imSpecies = len(imMetrics)*[species] #Extend the species list (mark all subrectangles as the same species)
        return imMetrics, imSpecies #Return the overal metric and species lists. These now include subdivided portions of each image. 
        
    
    def mainFunction(self):
        """
        NOTE: this is an unfinished function.
        This function tries to break a masked stitch into a bunch of original images.
            
        Prereq:
            self.readMP() and self.readMasksFromXml() need to be called
            
        Returns:
            metrics and species.
        """
        # find the cover
        # get training images
        
        # for every mask, 
        for i in xrange(len(self.masks)):
            # turn the mask into convex hull
            mask = self.masks[i]
            maskPath = mask.path
            maskImg = cv2.imread(maskPath, cv2.IMREAD_GRAYSCALE)
            maskSpecies = mask.species
            maskPoints = np.nonzero(maskImg)
            if len(maskPoints[0]) == 0:
                print maskPath + " is empty, skipping..."
                continue
                
            maskPoints = np.column_stack(maskPoints)
            hull = ConvexHull(maskPoints)
            hullBoundary = zip(maskPoints[hull.vertices, 1], maskPoints[hull.vertices, 0])
            hullBoundary.append(hullBoundary[0])
        
            # find the set of originals that intersect with the convex hull mask
            overlappingOriginals = []
            for original in self.mp.originals:
                originalProj = self.mp.originalCornerInStitch(original)
                originalPolygon = Polygon(originalProj)
                maskPolygon = Polygon(hullBoundary)
                intersection = originalPolygon.intersection(maskPolygon)
                
                if not intersection.is_empty:
                    overlappingOriginals.append(original)
            
            print maskPath
            print overlappingOriginals
            
            
            # TODO: while the mask is none-empty
                # find the original image that has the largest intersection area
                # with the current mask
                # get the mask from the original image space
                # update mask
                
            # TODO: make sliding windows for each fraction of mask
            originalImg = cv2.imread("images/Research_May15_small.jpeg")
            self.tiledTraining(originalImg, [maskPath], [maskSpecies])
                
            break

        
        # TODO: return the training images
        return

#bmt = CreateMaskedTraining()
#mt.tiledTraining(imageName, nonFlowerImgs, nonFlowerSpecies, n, overlap)
#mt = CreateMaskedTraining()
#mt.readMasks("images/new")
#mt.readMasksFromXml("images/research_may15")
#mt.mainFunction()