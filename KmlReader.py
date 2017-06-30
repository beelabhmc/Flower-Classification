from Constants import *
import xml.etree.ElementTree as ET
from MappingImageClass import *

"""
Helper functions for originalReader; translate a string of coordinates to a 
list of numerical values.

@param coordsStr: the list of coordinates in string form
@return: list of numerical coordinates
"""
def unzipCoords(coordsStr):
    numCoords = []
    coords = coordsStr.split(' ')
    for coord in coords:
        coord = coord.split(',')
        coord = [float(i) for i in coord]
        numCoords += [coord]
    return numCoords

"""
Reads in a kml file for the original footprints and converts to a dictionary of 
original images

@param kmlFilePath: the locaton of the kml file, based off /images/
@return: a dictionary of all the original images
"""
def originalReader(kmlFilePath):
    tree = ET.parse(IMAGE_PATH + kmlFilePath)
    root = tree.getroot()
    
    originalImages = {}
    for placemark in root.iter(KML_NAMESPACE + 'Placemark'):
        imageName = placemark.find(KML_NAMESPACE + 'name').text
        coord = placemark.find('.//' + KML_NAMESPACE + 'coordinates').text
        coord = unzipCoords(coord)
        originalImages[imageName] = OriginalImage(coord)

    return originalImages
    
"""
Reads in a kml file for the stitched map and converts to an stitched image obj.

@param kmlFilePath: the location fo the kml file, based off /images/
@param imgWidth: the width of the stitched map
@param imgHeight: the height of the stitched map
@return: a stitched image object
"""
def stitchReader(kmlFilePath, imgWidth, imgHeight):
    tree = ET.parse(IMAGE_PATH + kmlFilePath)
    root = tree.getroot()
    coords = []

    for latlonbox in root.iter(KML_NAMESPACE + 'LatLonBox'):
        north = float(latlonbox.find(KML_NAMESPACE + 'north').text)
        south = float(latlonbox.find(KML_NAMESPACE + 'south').text)
        east = float(latlonbox.find(KML_NAMESPACE + 'east').text)
        west = float(latlonbox.find(KML_NAMESPACE + 'west').text)
        
        coord = [[west, north], [east, north], [east, south], [west, south], [west, north]]
        coords += coord
    
    return StitchImage(coords, imgWidth, imgHeight)
    
"""
An alternate way of reading the stitched map. Use this method if and only if
you are reading scheme kml files.

@param kmlFilePath: the location fo the kml file, based off /images/
@param imgWidth: the width of the stitched map
@param imgHeight: the height of the stitched map
@return: a stitched image object
"""
def stitchSchemeReader(kmlFilePath, imgWidth, imgHeight):
    tree = ET.parse(IMAGE_PATH + kmlFilePath)
    root = tree.getroot()
    
    coord = None
    for lr in root.iter(KML_NAMESPACE + 'LinearRing'):
        coord = lr.find('.//' + KML_NAMESPACE + 'coordinates').text
        coord = unzipCoords(coord)
        
    return StitchImage(coord, imgWidth, imgHeight)

#print originalReader('stitchTest/footprints.kml')
#print stitchReader('stitchTest/stitched footprint.kml', 2726, 2695)
