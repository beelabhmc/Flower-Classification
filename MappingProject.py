from KmlReader import *

class MappingProject:
    originals = {}
    stitch = None
    
    def readProjectKmlFiles(self, originalKml, stitchKml, stitchWidth, stitchHeight, scheme=False):
        self.originals = originalReader(originalKml)
        if scheme:
            self.stitch = stitchSchemeReader(stitchKml, stitchWidth, stitchHeight)
        else:
            self.stitch = stitchReader(stitchKml, stitchWidth, stitchHeight)
        return
        
    def originalToStitch(self, originalImgName, l, m):
        x, y = self.originals[originalImgName].originalToGpsCoord(l, m)
        ll, mm = self.stitch.gpsToStitchCoord(x, y)
        return ll, mm
        
    def stitchToOriginal(self, originalImgName, l, m):
        x, y = self.stitch.stitchToGpsCoord(l, m)
        ll, mm = self.originals[originalImgName].gpsToOriginalCoord(x, y)
        return ll, mm
        
    def fromOriginals(self, l, m, fromImages=None):
        x, y = self.stitch.stitchToGpsCoord(l, m)
        originals = []
        
        if fromImages == None:
            fromImages = self.originals.keys()
        for k in iter(fromImages):
            if self.originals[k].includes(x, y):
                originals += [k]
        return originals
        
mp = MappingProject()

mp.readProjectKmlFiles("stitchTest/footprints.kml", "stitchTest/stitched footprint.kml", 2726, 2695)
print mp.fromOriginals(1000, 2000)

#print mp.stitchToOriginal("DJI_0162.JPG", 1363, 1342)
#print mp.stitchToOriginal("DJI_0163.JPG", 1363, 1342)
#print mp.stitchToOriginal("DJI_0169.JPG", 1363, 1342)
#print mp.stitchToOriginal("DJI_0170.JPG", 1363, 1342)

#print mp.originalToStitch("DJI_0163.JPG", 1873, 2188)

#mp.readProjectKmlFiles("footprints copy.kml", "stitched footprint copy.kml", 2, 2)
#
#print mp.stitchToOriginal("test.JPG", 1, 1)
