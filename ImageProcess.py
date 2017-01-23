# -*- coding: utf-8 -*-
from PIL import ImageFilter
import numpy
from PIL import Image
from PIL import ImageStat
from colorsys import * 
from operator import add
from sklearn import preprocessing
from skimage.feature import greycomatrix, greycoprops
from skimage import filters, color
from MachineLearning import * 
import matplotlib 
from scipy.stats import skew 

#Global Variables. 

NUMBERMETRICS = 19 #change the number of metrics used here. 

#############Calculating metrics ############################################
#############################################################################

def getMetrics(image):
    """Takes in a PIL image and outputs all of the metrics on that image in a list."""  
    avg = colorAvg(image) 
    yellow = findYellowFast(image) 
    edges = countEdgePixels(image) 
    var = colorVariance(image) 
    texture = textureAnalysis(image)
    (contrast, dissim, homog, energy, corr, ASM) =  GLCM(image)
    (Hstd, Sstd, Vstd, Hskew, Sskew, Vskew) = colorMoment(image)
    metrics = [avg[0], avg[1], avg[2], yellow, var, edges, texture, contrast, dissim, homog, energy, corr, ASM, Hstd, Sstd, Vstd, Hskew, Sskew, Vskew]
    return metrics 
    
#Extract all nxn rectangles from an image (these will be processed then used as inputs for ML algorithm). 
def getSub(n, imageName, overlap): 
    """Takes in n, an integer less than or equal to the minimum dimension of the image 
       and imageName, the string containing the name of the image to be processed.  
       Returns a list of metrics for each nxn subsection of the image.""" 
    # define overlap percentage for sub images        
    image = Image.open(imageName) #load in the image.
    #Find the size of the image. 
    size = image.size
    width = size[0] #pull out length and width 
    length = size[1] 

    smallTileSize = int(overlap*n)
    
    MetricDict = {} #initialize empty dict. 
    # Extract all tiles using a specific overlap (overlap depends on n)
    for i in range(0,width -int( overlap*n), int(overlap*n)): #Go through the entire image 
        for j in range(0, length - int(overlap*n), int(overlap*n)): 
            box = (i,j,i+smallTileSize, j+smallTileSize)  #edge coordinates of the next rectangle. 
            newImage = image.crop(box) #pull out the desired rectangle
            ### METRIC CALCULATIONS - Time counters commented out for now. 

            Metrics = getMetrics(newImage) #calculate all of the metrics on this cropped out image. 
            MetricDict[(i,j)] = Metrics #add these metrics to the metric dictionary with the upper left coordinates as the key. 
    return MetricDict
    
def allMetrics(dictionary,n, im, overlap): 
    """Takes in a dictionary of results from small tiles and calculates average metrics 
    	for a larger tile of size n, in image im, with overlap percentage im."""
    width, height = im.size 
    overlapSize = int(overlap*n)
    numberTiles = int((width-n)/(overlapSize)+1)*int(((height-n)/(overlapSize))+1)
    metricArray = numpy.zeros((NUMBERMETRICS, numberTiles))
    
    for i in range(0,width - n, overlapSize): 
        for j in range(0,height- n, overlapSize): 
            #you're at the start of a box
            metricTotals = len(dictionary[(0,0)])*[0.0]
            ##Adding up metrics from small tiles 
            for k in range(i,i+n-overlapSize+1, overlapSize): 
                for m in range(j, j+n-overlapSize+1, overlapSize): 
                    #pull out metrics 
                    metrics = dictionary[(k,m)]
                    #print metrics 
                    metricTotals = map(add, metricTotals, metrics) 
            ##Averaging metrics 
            num = 1/(overlap**2)
            newMetric = [a/num for a in metricTotals]
            
            ##Put all metrics metrics in an array. One metric per row. 
            for index in range(len(metricTotals)): 
                metricArray[index,int(i/(overlap*n) + j*(width-n)/((overlap*n)**2))] = newMetric[index] 
    #print metricArray 
    return metricArray 
                
def calcMetrics(imageName, tileSize, overlap): 
    """wrapper function to calculate metrics for each tile of the image.
        returns an array containing metric vectors in order by coordinates 
        of the upper left hand of the tile desired. Also returns a scalar object 
        for scaling future input data. """ 

    im = Image.open(imageName)
    subDict = getSub(tileSize, imageName, overlap)  #Get a dictionary of metrics for small tiles
    finalMetrics = allMetrics(subDict, tileSize, im, overlap, NUMBERMETRICS) #calculate metrics on larger tiles  
    #scaled, scaler = scaleMetrics(finalMetrics) ##Scale metrics 
    totalSize = finalMetrics.size #Find the size of this scaled metric array
    numCols = totalSize/NUMBERMETRICS  #Find the number of tiles =number of cols
    returnList = []
    for i in range(numCols): ##Change output into a list of lists 
        currentMetric = [] 
        for metric in range(NUMBERMETRICS): 
            currentMetric += [finalMetrics[metric, i]] 
        returnList += [currentMetric]
    return returnList #return the metrics for later
    
def scaleMetrics(metricArray): 
    """Takes in a array of metrics, scales them to have 
        mean 0 and stdev 1. returns both the metrics and the scaler object 
        which can be used to transform later data. """ 
        
    #First put all metrics into arrays with one metric 
    scaler = preprocessing.StandardScaler().fit(metricArray)
    scaledArray = scaler.transform(metricArray) 
    return scaledArray, scaler 

#######################Debugging Functions############################# 



def oneDensOverlap((i,j), n, imageName, overlap, subTileDict, fit, scaler): 
    """Computes the density of one tile with overlap""" 
    #Note that this algorithm assumes 1/overlap is an integer 
    shiftSize = int(n*overlap)
    #How many subtiles are in the width of the image? 
    numTiles =int( 1/overlap )
    metricTotal = len(subTileDict[(0,0)])*[0.0]
    for k in range(numTiles): 
        for m in range(numTiles): 
           # print (k,m)
            newMetrics = subTileDict[(i + m*shiftSize, j + k*shiftSize)]
            metricTotal = map(add, metricTotal, newMetrics)
    num = 1/(overlap**2)
    avgMetric = [a/num for a in metricTotal] #Compute the average 
    scaledMetric = scaler.transform(avgMetric) #Scale the metric 
    density = fit.predict(scaledMetric) 
    return list(density)
    
def allDensOverlap(n, imageName, overlap, densityList, metricList, fit, scaler): 
    """Computes all densities on a map with tilesize n, the given image as the map, and an overlap 1-overlap."""
    image = Image.open(imageName) 
    imageSize = image.size 
    width = imageSize[0]
    height = imageSize[1] 
    
    subTileDict = getSub(n, imageName, overlap) #Compute the metrics on subtiles 

    allDensities = []
    shiftSize = int(n*overlap)
    for k in range(0, height -n, shiftSize): 
        for m in range(0, width - n, shiftSize): 
            currentDensity = oneDensOverlap((m,k), n, imageName, overlap, subTileDict, fit, scaler)
            allDensities += currentDensity
    return allDensities 
    

######TRAINING SET CALCULATIONS#########################

def trainMetrics(imageName, density): 
    """Simple helper function. Opens the input image and calculates metrics on it. Then returns the metrics and associated data."""
    image = Image.open(imageName)  #open the relevant image as a PIL image. 
    metrics = getMetrics(image) #get all of the metrics calculated on this image. 
    return [metrics, density] 
    
def allTrainMetrics(imageList, densityList): 
    """Similar to train metrics, but takes in a series of images stored in a list and calculates metrics for all of them."""
    metricsList = []
    print 'images ', imageList 
    print 'densityList ', densityList
    for i in range(len(imageList)): 
        imageName = imageList[i]
        [metrics, density] = trainMetrics(imageName, densityList[i]) 
        metricsList += [metrics] 
    return metricsList, densityList
    
def allTrainMetricsTransect(imageList, densityList):  
    """takes in a list of images from a transect and calculates metrics for them. 
    Outputs a list of metrics and a list of the associated data."""
    metricsList = []
    for i in range(len(imageList)): #for all of the training images. 
        image = imageList[i] #pull out the next one. 
        metrics = getMetrics(image) #get the metrics for this image. 
        metricsList += [metrics] #add to the full metric list. 
    return metricsList, densityList  #return an ordered list of metrics and corresponding density or species. 
    
          
######################Start of helper functions for computing features. ##################################
#########################################################################################################   
def colorAvg(im): 
    """Takes in a string containing an image file name, returns the average red, blue, and green 
        values for all the pixels in that image.""" 
    imStats = ImageStat.Stat(im) 
    (redAv, greenAv, blueAv) = imStats.mean
    return redAv, greenAv, blueAv
    

def colorVariance(im):
    '''Calculates the diversity in color using a hue histogram'''
    
    # load image pixels
    pix = im.load()
    width, height = im.size
    
    # create empty histogram to be filled with frequencies
    histogram = [0]*360
    pixelHue = 0
    for i in range(width):
        for j in range(height):
            (r,g,b) = pix[i,j] #pull out the current r,g,b values 
            (h,s,v) = rgb_to_hsv(r/255.,g/255.,b/255.)
            pixelHue = int(360*h)
            #build histogram
            histogram[pixelHue] += 1
    #print histogram
    # calculate standard deviation of histogram
    return numpy.std(histogram)
        
    
      
def countEdgePixels(im):
    ''' counts the number of pixels that make up the edges of features'''
    # define threshold for edges
    threshold = 150 
    
    # open image and filter
    im2 = im.filter(ImageFilter.FIND_EDGES)
    im2 = im2.convert("L")
	
    # load pixels and count edge pixels
    pix = im2.load()
    pixels = 0
    for x in range(0,im.size[0]):
        for y in range(0, im.size[1]):
            if pix[x,y] > threshold:
                pixels += 1

    return float(pixels) / (im.size[0]*im.size[1])
    
def textureAnalysis(im):
    ''' determines the proportion of the image that has texture'''
    # define texture threshold and grid size
    threshold = 100
    n = 7
    
    # open image
    width, height = im.size
    
    # loop across image
    count = 0
    for i in range(0,width-n,n):
        for j in range(0,height-n,n):
            
            # divide into small grids
            box = (i,j,i+n,j+n)
            imTemp = im.crop(box)
            
            # calculate intensity from RGB data
            pixels = list(imTemp.getdata())
            intensity =  [pixels[i][0]+pixels[i][1]+pixels[i][2] for i in range(len(pixels))]
                      
            # count as high texture if difference in intensity is 
            # greater than threshold
            if ((max(intensity) - min(intensity)) > threshold):
                count += 1
                
    # calculate the percentage of high texture grids
    
    if width/n == 0: #if width is less than n something is wrong! Check the width and make sure n is a reasonable value. 
        print width
        raw_input('Oops')
    return float(count)/((width/n)*(height/n))
    
def findYellowFast(im): 
    """counts the number of a given color pixels in the given image.""" 
 #   im = Image.open(imageName)
    #define HSV value ranges for yellow  
    #for now just base of Hue - refine for actual yellows seen in field? 
    minHue = 20/360.
    maxHue = 150/360.
    
    minSat = 5/360. 
   # maxSat = 0.4
   
    minV = 190/360.
    
    width, height = im.size  #find the size of the image 
    count = 0 #initialize a counter for yellow pixels.  
    rgbList = list(im.getdata())
    hsvList = map(getHSV, rgbList)
    for (h,s,v) in hsvList: 
        if minHue <h and h<maxHue and minSat<s and minV<v: 
            count += 1
    totalPix = width*height 
    portion = float(count)/totalPix
    return portion
    
def getHSV((r,g,b)): 
    return rgb_to_hsv(r/255., g/255., b/255.)
    
def GLCM(im):
    """Calculate the grey level co-occurrence matrices and output values for 
    contrast, dissimilarity, homogeneity, energy, correlation, and ASM in a list"""
    
    newIm = im.convert('L') #Conver to a grey scale image
    glcm = greycomatrix(newIm, [5], [0]) #calcualte the glcm  
    
    #Compute all of the grey co occurrence features. 
    contrast = greycoprops(glcm, 'contrast')[0][0]
    if numpy.isnan(contrast): #Make sure that no value is recorded as NAN. 
        contrast = 0 #if it is replace with 0. 
    dissim = greycoprops(glcm, 'dissimilarity')[0][0]
    if numpy.isnan(dissim): 
        dissim = 0
    homog = greycoprops(glcm, 'homogeneity')[0][0]
    if numpy.isnan(homog): 
        homog = 0
    energy = greycoprops(glcm, 'energy')[0][0]
    if numpy.isnan(energy): 
        energy = 0
    corr = greycoprops(glcm, 'correlation')[0][0]
    if numpy.isnan(corr): 
        corr = 0
    ASM = greycoprops(glcm, 'ASM')[0][0]
    if numpy.isnan(ASM): 
        ASM = 0
    return numpy.concatenate(([contrast], [dissim], [homog], [energy], [corr], [ASM]), 0) #concatenate into one list along axis 0 and return 
    
def colorMoment(im): 
    """Calculates the 2nd and 3rd color moments of the input image and returns values in a list."""
    #The first color moment is the mean. This is already considered as a metric for 
    #the red, green, and blue channels, so this is not included here. 
    #Only the 2nd and 3rd moments will be calculated here. 
    
    newIm = matplotlib.colors.rgb_to_hsv(im) #convert to HSV space 
     
    #Pull out each channel from the image to analyze seperately. 
    HChannel = newIm[:,:,0]
    SChannel = newIm[:,:,1]
    VChannel = newIm[:,:,2]
    
    #2nd moment = standard deviation. 
    Hstd = numpy.std(HChannel) 
    Sstd = numpy.std(SChannel) 
    Vstd = numpy.std(VChannel) 
    
    #3rd Moment = "Skewness". Calculate the skew, which gives an array.
    #Then take the mean of that array to get a single value for each channel. 
    Hskew = numpy.mean(skew(HChannel))
    Sskew = numpy.mean(skew(SChannel))
    Vskew = numpy.mean(skew(VChannel))
    
    
    return [Hstd, Sstd, Vstd, Hskew, Sskew, Vskew] #return all of the metrics. 

    
    
    
    