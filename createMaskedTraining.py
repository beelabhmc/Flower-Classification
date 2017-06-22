# -*- coding: utf-8 -*-
import numpy as np
from Constants import * 
from MappingProject import *
import cv2
import os
from scipy import spatial as sp


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
        return bw

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

    
    def mainFunction():
        # read all masks - done
        # transform to bw masks - done
        
        # for every mask, 
            # find the cover
            # get training images
        
        
        # return the training images
        return None

mt = CreateMaskedTraining()
mt.readMasksFromXml("images/research_may15")