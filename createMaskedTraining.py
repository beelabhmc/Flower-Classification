# -*- coding: utf-8 -*-
import numpy as np
from Constants import * 
import ImageProcess as IP
from PIL import Image 

def readMask(filePath):
    image = Image.open(filePath)
    print image
    return image
    
readMask("research_may15/Research_May15_small.jpeg")