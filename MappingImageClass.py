from ImageGPSMapping import *
import numpy as np


"""
The original image class
"""
class OriginalImage:
    a = np.matrix([])
    b = np.matrix([])
    cornerGps = []
    
    def __init__(self, cornerGps):
        self.cornerGps = cornerGps
        self.a, self.b = imageToGpsCoeff(cornerGps)
    
    def originalToGpsCoord(self, l, m):
        return imageToGpsCoord(l, m, self.a, self.b)
    
    def gpsToOriginalCoord(self, x, y):
        return gpsToImageCoord(x, y, self.a, self.b)
    
    def includes(self, x, y):
        return isInImage(self.cornerGps, x, y)
        
        
"""
The stitched image class
"""
class StitchImage:
    cornerGps = []
    a = np.matrix([])
    b = np.matrix([])
    
    def __init__(self, cornerGps, width, height):
        self.cornerGps = cornerGps
        self.a, self.b = imageToGpsCoeff(cornerGps, imgWidth=width, imgHeight=height)
        
    def stitchToGpsCoord(self, l, m):
        return imageToGpsCoord(l, m, self.a, self.b)
    
    def gpsToStitchCoord(self, x, y):
        return gpsToImageCoord(x, y, self.a, self.b)
    
    def includes(self, x, y):
        return isInImage(self.cornerGps, x, y)