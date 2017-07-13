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
        if self.inRange(ll, mm):
            return ll, mm
        else:
            return None
    
    def originalCornerInStitch(self, originalImgName, width=4000, height=3000):
        corners = [[0, 0], [width, 0], [width, height], [0, height], [0, 0]]
        output = []
        for corner in corners:
            projx, projy = self.originalToStitch(originalImgName, corner[0], corner[1])
            output.append((projx, projy))
        return output
        
    def fromOriginals(self, l, m, fromImages=None):
        x, y = self.stitch.stitchToGpsCoord(l, m)
        originals = []
        
        if fromImages == None:
            fromImages = self.originals.keys()
        for k in iter(fromImages):
            if self.originals[k].includes(x, y):
                originals += [k]
        return originals
        
    def inRange(self, x, y, width=4000, height=3000):
        if x >= 0 and x <= width:
            if y >= 0 and y <= height:
                return True
        return False
        
mp = MappingProject()

# My own test stitches
#mp.readProjectKmlFiles("stitchTest/my-footprints.kml", "stitchTest/my-stitched-footprint.kml", 1000, 1000)
#print mp.originalCornerInStitch("DJI_0162.JPG")
#print mp.fromOriginals(499, 1000)
#print mp.originalToStitch("DJI_0162.JPG", 2000, 0)
#print mp.stitchToOriginal("DJI_0162.JPG", 0, 0)

#print "Mapping the point of interest from stitched map to individual originals"
#print "Original footprints & original stitch"
#mp.readProjectKmlFiles("stitchTest/footprints.kml", "stitchTest/stitched footprint.kml", 2726, 2695)
#print mp.stitchToOriginal("DJI_0162.JPG", 1363, 1342)
#print mp.stitchToOriginal("DJI_0163.JPG", 1363, 1342)
#print mp.stitchToOriginal("DJI_0169.JPG", 1363, 1342)
#print mp.stitchToOriginal("DJI_0170.JPG", 1363, 1342)
#
#print "Corrected footprints & extended stitch"
#mp.readProjectKmlFiles("stitchTest/footprints-agi.kml", "stitchTest/extrapolationOrtho.kml", 8725, 6814)
#print mp.stitchToOriginal("DJI_0162.JPG", 4836, 4107)
#print mp.stitchToOriginal("DJI_0163.JPG", 4836, 4107)
#print mp.stitchToOriginal("DJI_0169.JPG", 4836, 4107)
#print mp.stitchToOriginal("DJI_0170.JPG", 4836, 4107)
#
#print "Original footprints & extended stitch"
#mp.readProjectKmlFiles("stitchTest/footprints.kml", "stitchTest/extrapolationOrtho.kml", 8725, 6814)
#print mp.stitchToOriginal("DJI_0162.JPG", 4836, 4107)
#print mp.stitchToOriginal("DJI_0163.JPG", 4836, 4107)
#print mp.stitchToOriginal("DJI_0169.JPG", 4836, 4107)
#print mp.stitchToOriginal("DJI_0170.JPG", 4836, 4107)

#print "Mapping the point of interest from individual originals to stitched map"
#print "Original footprints & original stitch"
#mp.readProjectKmlFiles("stitchTest/footprints.kml", "stitchTest/stitched footprint.kml", 2726, 2695)
#print mp.originalToStitch("DJI_0162.JPG", 3114, 2815)
#print mp.originalToStitch("DJI_0163.JPG", 2098, 2957)
#print mp.originalToStitch("DJI_0169.JPG", 1615, 1565)
#print mp.originalToStitch("DJI_0170.JPG", 2661, 1390)
#
#print "Corrected footprints & extended stitch"
#mp.readProjectKmlFiles("stitchTest/footprints-agi.kml", "stitchTest/extrapolationOrtho.kml", 8725, 6814)
#print mp.originalToStitch("DJI_0162.JPG", 3114, 2815)
#print mp.originalToStitch("DJI_0163.JPG", 2098, 2957)
#print mp.originalToStitch("DJI_0169.JPG", 1615, 1565)
#print mp.originalToStitch("DJI_0170.JPG", 2661, 1390)
#
#print "Original footprints & extended stitch"
#mp.readProjectKmlFiles("stitchTest/footprints.kml", "stitchTest/extrapolationOrtho.kml", 8725, 6814)
#print mp.originalToStitch("DJI_0162.JPG", 3114, 2815)
#print mp.originalToStitch("DJI_0163.JPG", 2098, 2957)
#print mp.originalToStitch("DJI_0169.JPG", 1615, 1565)
#print mp.originalToStitch("DJI_0170.JPG", 2661, 1390)

print "Testing on larger testing images"
#mp.readProjectKmlFiles("stitchTest2/footprints.kml", "stitchTest2/stitchExtended.kml", 37599, 20369)
mp.readProjectKmlFiles("stitchTest2/footprints.kml", "stitchTest2/stitchOriginal.kml", 28909, 11771)
for no in xrange(463, 629, 5):
    imgName = "DJI_0" + str(no) + ".JPG"
    projection = mp.stitchToOriginal(imgName, 6788, 6790)
    if projection != None:
        print imgName, projection

print mp.originalToStitch("DJI_0493.JPG", 2859, 1816)
print mp.originalToStitch("DJI_0503.JPG", 1492, 1793)


#mp.readProjectKmlFiles("footprints copy.kml", "stitched footprint copy.kml", 2, 2)
#
#print mp.stitchToOriginal("test.JPG", 1, 1)
