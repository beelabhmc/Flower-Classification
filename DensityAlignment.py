from PIL import Image
import math
from Constants import *

#This file is used to create a training set. You can divide a large transect image into square 
#meter portions. This set of images is then saved and can be read in. 
def divideTransect(Start, End, imageName): 
    """Takes in the pixel coordinates of a start and end for a transect. Divides into images that
        match the collected density data. Outputs a list of these PIL images.""" 
        
    image = Image.open(IMAGE_PATH + imageName)
    ##First, calculate the length of the transect. 
        
    dim1 = Start[0] - End[0] #width
    dim2 = Start[1] - End[1] #height
    
    if dim1>dim2: 
        print 'Vertical'
        return transectVert(Start, End, image)
    else: 
        print 'Horizontal'
        imList = transectHoriz(Start, End, image)
    return imList
    
def transectHoriz(Start, End, image): 
    """Transect runs up and down in the image."""
    length = int(math.sqrt(abs(Start[0] - End[0])**2 + abs(Start[1] - End[1])**2))
    slope = abs(Start[1] - End[1])/length 
    meterSize = length/50 ##pixels/meter 
  #  print meterSize
   # print('meter size is ', Start[0] - End[0])
    meterSizeHoriz = (End[0] - Start[0])/50
    #print meterSizeHoriz
    imageList = []
    
    for i in range(Start[0], End[0], meterSizeHoriz): #Go along the entire transect every meter - in pixels
        ##Starting center pixel is Start[1]. 
        ##Ending center pixel is End[1] 
        ##Slope is calculated already as slope - interpolate assuming linear
        
        centerPix = Start[1] + slope*i #Intercept + slope*number of pixels you have moved. 
        
        leftBound = centerPix - meterSize 
        rightBound = centerPix + meterSize  
        box = (leftBound,i, rightBound, i+meterSize)
        
        subIm = image.crop(box)
        imageList += [subIm] 
    
    return imageList
        
def transectVert(Start, End, image): 
    """Transect runs left and right in the image.The left end is start.""" 
    length = int(math.sqrt(abs(Start[0] - End[0])**2 + abs(Start[1] - End[1])**2)) 
    slope = (End[0] - Start[0])/float(length)
    #print 'slope ', slope
    meterSize = length/50 ##pixels/meter     
    meterInc = int(math.sqrt(meterSize**2 - slope**2))
    imageList = []
    vertMeterSize = math.ceil((End[1] - Start[1])/50.)
    vertMeterSize = int(vertMeterSize)
    #print 'Meter size is ', meterSize
    #print 'Meter incremenents (vertically) are ', meterInc 
    #print 'Vertical Distance is ', Start[1] - End[1] 
    
    for i in range(Start[1], End[1], vertMeterSize): #Go along the entire transect every meter - in pixels
        ##Starting center pixel is Start[1]. 
        ##Ending center pixel is End[1] 
        ##Slope is calculated already as slope - interpolate assuming linear
        centerPix = Start[0] + int(slope*(i-Start[1])) #Intercept + slope*number of pixels you have moved. 
     #   print 'Center Pixel is ', centerPix
        leftBound = centerPix - meterSize 
        rightBound = centerPix + meterSize 
        box = (leftBound, i, rightBound, i+meterSize)
        subIm = image.crop(box)
        imageList += [subIm] 
    #print 'Final i is ', i 
    #print 'final center pix is ', centerPix
    #print 'Length is ', len(imageList)
    return imageList

def saveTransect(imageList, start, nameBase): 
    """Takes in a list of the images from a transect and saves each image so that it can be called 
        in the machine learning portion as a training set data point.
        Inputs: imageList, a list of PIL images 
        start: the file number you want to start saving images at. 
        No output, saves files in your current directory.""" 
    currentNum = start
    for quadrat in imageList: 
        fileName = nameBase + str(currentNum) + '.jpg'
        quadrat.save(fileName)
        currentNum += 1 
            
def main():  
    """Helper function to test the transect stitches and make sure they 
        are reasonable. Takes no arguments. Parameters are changed inside the function."""

    imageName = 'TransectStitch1.jpg'
    #End = (594, 1046)
    #Start = (1718, 460)

    Start = (1035,588)
    End = (456,1720)

  #  Start = tuple(raw_input('Please Input Start Coordinates'))
   # End  = tuple(raw_input('Please Input End Coordinates'))
   
    stuff= divideTransect(Start, End, imageName)
    if len(stuff) != 50: 
        print "Error! Transect length is not 50 meters." 
    return stuff