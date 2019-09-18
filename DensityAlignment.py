from PIL import Image
import math
from Constants import *
import cv2
import diagonal_crop


#This file is used to create a transect image training set. You can divide a large transect image into square 
#meter portions. This set of images is then saved and can be read in. 
def divideTransect(Start, End, imageName): 
    """Takes in the pixel coordinates of a start and end for a transect. Divides into images that
        match the collected density data. Outputs a list of these PIL images.""" 
        
    image = Image.open(IMAGE_PATH + imageName)
    ##First, calculate the length of the transect. 
        
    dim1 = Start[0] - End[0] #width
    dim2 = Start[1] - End[1] #height
    
    imList = transectTotal(Start, End, image)
    #if dim1>dim2: 
    #    print 'Vertical'
    #    return transectVert(Start, End, image)
    #else: 
    #    print 'Horizontal'
    #    imList = transectHoriz(Start, End, image)
    return imList
    
def transectHoriz(Start, End, image): 
    """Transect runs up and down in the image."""
    length = int(math.sqrt(abs(Start[0] - End[0])**2 + abs(Start[1] - End[1])**2)) #Calculate the total length in pixels of the transect. 
    slope = abs(Start[1] - End[1])/length 
    meterSize = length/50 ##pixels/meter since we know the transect is 50 meters long. 
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
    
def transectTotal(Start, End, img): 
    length = int(math.sqrt(abs(Start[0] - End[0])**2 + abs(Start[1] - End[1])**2)) #Calculate the total length in pixels of the transect. 
    pix_per_meter = length/50 #How many pixels are in one meter, given the transect is 50 meters long. 
    horiz_length = Start[0] - End[0]
    h_pix_per_meter = horiz_length/50 #Determine how many pixels horizontally and vertically are required to move one meter along the direction of the transect. 
    vert_length = Start[1] - End[1] 
    v_pix_per_meter = vert_length/50  #pix per meter vertically. 
    
    angle = math.atan(vert_length/horiz_length) #Compute the angle at which the transect travels in radians 
    alpha = math.pi/2 - angle
   # img = Image.open(image) #open the image you are working with 
    #img2 = img.rotate(-angle,expand=True) #Rotate the image so that the transect is now vertical. 
    
    #Now that the image has been rotate, calculate the new starting and ending points.
    #xmid = img.size[0]/2
    #ymid = img.size[1]/2 
    #oldStart_x = Start[0] #The original coordinates
    #oldStart_y = Start[1]
    #newStart_x = int(-(oldStart_y-ymid)*math.sin(angle) + (oldStart_x-xmid)*math.cos(angle)) + xmid #The new starting coordinates in the rotated image. 
    #newStart_y = int((oldStart_y-ymid)*math.cos(angle) + (oldStart_x+xmid)*math.sin(angle)) + ymid
    #
    #oldEnd_x = End[0] #The original ending coordinates
    #oldEnd_y = End[1]     
    #newEnd_x = int(oldEnd_y*math.sin(angle) + oldEnd_x*math.cos(angle)) + xmid #The new ending coordinates in the rotated image. 
    #newEnd_y = int(oldEnd_y*math.cos(angle) - oldEnd_x*math.sin(angle)) + ymid
    
    imageList = []  
    height = pix_per_meter
    width = 2*pix_per_meter
    #rotated_meter_size = int((newEnd_x - newStart_x)/50) #The new image has a horizontal transect in it starting and ending at these coordinates, 50 m in length. 
    for i in range(50): #Go along the entire transect every meter. The transect should now be horizontal. 
      #  centerpix = newStart_x + i*rotated_meter_size #Find where you are on the transect now, at meter i 
      #  leftBound = centerpix #Determine the bounding edges of the box. The left edge starts at the meter you are on
      #  rightBound = centerpix + rotated_meter_size #The right edge is one meter away from the left edge 
      #  
      #  top = newStart_y - rotated_meter_size #The top is one meter above the y coordinate of the transect
      #  bottom = newStart_y + rotated_meter_size #The bottom is one meter below the y coordinate of the transect. 
      #  box = (leftBound,top, rightBound, bottom) #(27135, 27416, -3560, -4122)
      # # print(rightBound, leftBound, top, bottom) # (21860, 35332)
      ##  print(img2.size)
      #  subIm = img2.crop(box) #crop out the current box 
    
        base_pix = (Start[0] + (i+1)*h_pix_per_meter - pix_per_meter*math.cos(alpha), Start[1] + (i+1)*v_pix_per_meter + pix_per_meter*math.sin(alpha))
        subIm = diagonal_crop.crop(img, base_pix, angle, height, width)
        imageList += [subIm] #Add it to the list of images in this transect. 
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
        fileName = IMAGE_PATH + nameBase + str(currentNum) + '.jpg'
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
        print("Error! Transect length is not 50 meters.") 
    return stuff
