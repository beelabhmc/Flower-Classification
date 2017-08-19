from KmlReader import *

class MappingProject:
    """
    The Class Module for finding a projection between original image coordinates
    and stitch image coordinates. 
    
    Attributes:
        originals: a dictionary that maps the img names to OriginalImage objects
        stitch: a StitchImage object
    """
    originals = {}
    stitch = None
    
    def readProjectKmlFiles(self, originalKml, stitchKml, stitchWidth, stitchHeight, scheme=False):
        """
        This function reads in the original image information and stich image information.
        
        Args:
            originalKml: path to the original image kml file
            stitchKml: path to the stitch image kml file
            stitchWidth: width (in pixels) of the stitch image
            stitchHeight: height (in pixels) of the stitch image
            scheme: whether we are reading from the scheme file.
        """
        self.originals = originalReader(originalKml)
        if scheme:
            self.stitch = stitchSchemeReader(stitchKml, stitchWidth, stitchHeight)
        else:
            self.stitch = stitchReader(stitchKml, stitchWidth, stitchHeight)
        
        
    def originalToStitch(self, originalImgName, l, m):
        """
        This function maps original coords space to the stitch coords space.
        
        Args:
            originalImgName
            l: x coord in the original image space
            m: y coord in the original image space
        
        Returns:
            ll: x coord in the stitch image space
            mm: y coord in the stitch image space
        """
        x, y = self.originals[originalImgName].originalToGpsCoord(l, m)
        ll, mm = self.stitch.gpsToStitchCoord(x, y)
        return ll, mm
        
        
    def stitchToOriginal(self, originalImgName, l, m):
        """
        This function maps stitch coords space to the original coords space.
        
        Args:
            originalImgName
            l: x coord in the stitch image space
            m: y coord in the stitch image space
        
        Returns:
            ll: x coord in the original image space
            mm: y coord in the original image space
        """
        x, y = self.stitch.stitchToGpsCoord(l, m)
        ll, mm = self.originals[originalImgName].gpsToOriginalCoord(x, y)
        return ll, mm
    
    
    def originalCornerInStitch(self, originalImgName, width=4000, height=3000):
        """
        This function maps the corner of an original image to the stitch space.
        
        Args:
            originalImgName
            width: default 4000. Width of the original image
            height: default 3000. Height of the original image
        
        Returns:
            a list of the corner coordinates in the stitch space.
        """
        corners = [[0, 0], [width, 0], [width, height], [0, height], [0, 0]]
        output = []
        for corner in corners:
            projx, projy = self.originalToStitch(originalImgName, corner[0], corner[1])
            output.append((projx, projy))
        return output
        
        
    def fromOriginals(self, l, m, fromImages=None):
        """
        Given a coordinate in the stitch, this funtion returns a list of original
        images that contain this point.
        
        Args:
            l, m: x and y coordinate of the stitch
            fromImages: default None (aka look at all original images). A list of original 
            images to check from.
        
        Returns:
            a list original images.
        """
        x, y = self.stitch.stitchToGpsCoord(l, m)
        originals = []
        
        if fromImages == None:
            fromImages = self.originals.keys()
        for k in iter(fromImages):
            if self.originals[k].includes(x, y):
                originals += [k]
        return originals
        
#mp = MappingProject()

# My own test stitches
#mp.readProjectKmlFiles("stitchTest/my-footprints.kml", "stitchTest/my-stitched-footprint.kml", 1000, 1000)
#print mp.originalCornerInStitch("DJI_0162.JPG")
#print mp.fromOriginals(499, 1000)
#print mp.originalToStitch("DJI_0162.JPG", 2000, 0)
#print mp.stitchToOriginal("DJI_0162.JPG", 0, 0)

# Try mapping the point of interest from stitched map to individual originals
#mp.readProjectKmlFiles("stitchTest/footprints.kml", "stitchTest/stitched footprint.kml", 2726, 2695)
#print mp.stitchToOriginal("DJI_0162.JPG", 1363, 1342)
#print mp.stitchToOriginal("DJI_0163.JPG", 1363, 1342)
#print mp.stitchToOriginal("DJI_0169.JPG", 1363, 1342)
#print mp.stitchToOriginal("DJI_0170.JPG", 1363, 1342)

#print mp.originalToStitch("DJI_0163.JPG", 1873, 2188)

#mp.readProjectKmlFiles("footprints copy.kml", "stitched footprint copy.kml", 2, 2)
#
#print mp.stitchToOriginal("test.JPG", 1, 1)
