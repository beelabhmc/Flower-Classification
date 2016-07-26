from PIL import Image
from colorsys import *
from PIL import ImageFilter

def density(imageName): 
    """takes in an image name in a string and outputs
        the percent cover of the desired color in that image."""
    im = Image.open(imageName)
    im = im.filter(ImageFilter.BLUR)
    pix = im.load() #load in pixel array  
    #define HSV value ranges for yellow  
    #for now just base of Hue 
    #Pull hue and sat values from image + flower type you want. Add range for errors/small changes 
    
    ##CHANGE THESE VARIABLES (currently set at yellow flower values)
    minHue = 55/360.
    maxHue = 70/360.
    
    minSat = 0.15 
   # maxSat = 0.4
   
    minV = 0.5
    
    ####
    
    width, height = im.size  #find the size of the image 
    count = 0 #initialize a counter for yellow pixels.  
    for i in range(width): 
        for j in range(height): 
            (r,g,b) = pix[i,j] #pull out the current r,g,b values 
            (h,s,v) = rgb_to_hsv(r/255.,g/255.,b/255.) 
            if minHue<h and h<maxHue and minSat<s and s<maxSat and minV< v: 
                count += 1 #add one to the count 
    totalPix = width*height 
    portion = float(count)/totalPix
    #print(portion)
    return portion      
