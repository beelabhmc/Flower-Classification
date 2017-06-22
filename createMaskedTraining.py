# -*- coding: utf-8 -*-
import numpy as np
from Constants import * 
from MappingProject import *
from PIL import Image 

def convertMask(filePath, saveToFile=False):
    image = Image.open(filePath)
    gray = image.convert('L')
    bw = gray.point(lambda x: 0 if x==0 else 255, '1')
    bw.save(filePath)
    return bw
    
#def 
    
def trainingForProject(originalFoorprint, stitchFootprint, stitchWidth, stitchHeight):
    mp = MappingProject()
    mp.readProjectKmlFiles(originalFoorprint, stitchFootprint, stitchWidth, stitchHeight)
    
    
    
    # read all masks
    # transform to bw masks
    
    # for every mask, 
        # find the cover
        # get training images
    
    
    # return the training images
    
convertMask("images/research_may15/Research_May15_small_mask_0.png", True)