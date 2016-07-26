from MachineLearning import * 
from FullProgram import * 
from ImageProcess import * 
from DensityAlignment import *



############Functions here were written for debugging purposes and are not used in 
############running the full program. 


def oneDensity((i,j), w, h, imageName): 
    densityList = [0.0,1.0, 0.99, 0.02, 0.64, 0.0, 0.1]

    image = Image.open(imageName) 
    
    box = (i,j,i+w, j+h)
    newImage = image.crop(box)
    
    
    f = open('metricList.txt', 'r')
    data = f.read()
    metricList = eval(data)
    scaledTraining, scaler = scaleMetrics(metricList)
    
    #Calculate metrics 
    avg = colorAvg(newImage) 
    yellow = findYellowFast(newImage) 
    edges = countEdgePixels(newImage) 
    var = colorVariance(newImage) 
    texture = textureAnalysis(newImage)
    Metrics = (avg[0], avg[1], avg[2], yellow, var, edges, texture)
   # print 'Original Metrics ', Metrics
    Metrics = scaler.transform(Metrics)
    print Metrics
    
    #Find fit 
    fit = svrAlg(scaledTraining, densityList)
        
    density = fit.predict(Metrics)
    return list(density)
 
 
def allDensities(w,h, imageName): 
    image = Image.open(imageName) 
    imageSize = image.size 
    width = imageSize[0]
    height = imageSize[1] 
    
    densityList = []
    for k in range(0, height -h, h): 
        for m in range(0, width - w, w): 
            currentDensity = oneDensity((m,k), h, w, imageName)
            densityList += currentDensity
    return densityList 
    
    
def findYellow(im):  #Use the fast version! (findYellowFast(im))
    """counts the number of yellow pixels in the given image.""" 
    #im = Image.open(imageName)
    pix = im.load() #load in pixel array  
    #define HSV value ranges for yellow  
    #for now just base of Hue - refine for actual yellows seen in field? 
    minHue = 50/360.
    maxHue = 61/360.
    width, height = im.size  #find the size of the image 
    count = 0 #initialize a counter for yellow pixels.  
    for i in range(width): 
        for j in range(height): 
            (r,g,b) = pix[i,j] #pull out the current r,g,b values 
            (h,s,v) = rgb_to_hsv(r/255.,g/255.,b/255.) 
            if minHue<=h and h<maxHue: 
                count += 1 #add one to the count 
    totalPix = width*height 
    portion = float(count)/totalPix
    #print(portion)
    return portion
    
def analysis(avg, yellow, var, edges, texture): 
    """analyze things to check if they work""" 
    r = [a[0] for a in avg]
    ravg = numpy.mean(r)
    rmin = min(r) 
    rmax = max(r)
    g = [a[1] for a in avg]
    gavg = numpy.mean(g)
    gmin = min(g) 
    gmax = max(g)
    b = [a[2] for a in avg]
    bavg = numpy.mean(b)
    bmin = min(b) 
    bmax = max(b)
    
    
    print('Red Statistics') 
    print('Average is ', ravg) 
    print('Min is ', rmin)
    print('Max is ', rmax)
    
    print('Green Statistics') 
    print('Average is ', gavg) 
    print('Min is ', gmin)
    print('Max is ', gmax)
    
    print('Blue Statistics') 
    print('Average is ', bavg) 
    print('Min is ', bmin)
    print('Max is ', bmax)
    
    
    yavg = numpy.mean(yellow)
    ymin = min(yellow)
    ymax = max(yellow)
    
    print 'Yellow Statistics' 
    print 'Average is ', yavg 
    print 'Min is ', ymin 
    print 'Max is ', ymax
    
    vavg = numpy.mean(var)
    vmin= min(var)
    vmax = max(var) 
    
    print 'Color Variance Statistics' 
    print 'Average is ', vavg 
    print 'Min is ', vmin 
    print 'Max is ', vmax
    
    eavg = numpy.mean(edges)
    emin= min(edges)
    emax = max(edges) 
    
    print 'Edge Count Statistics' 
    print 'Average is ', eavg 
    print 'Min is ', emin 
    print 'Max is ', emax
    
    tavg = numpy.mean(texture) 
    tmin= min(texture)
    tmax = max(texture) 
    print 'Texture Statistics' 
    print 'Average is ', tavg 
    print 'Min is ', tmin 
    print 'Max is ', tmax
    
def fullTest():  #we never use this now. 
    imageName = 'SmallTile.jpg'
    tileSize = 50 
    
    overlap = 0.1 
    imageSize = [472, 398]
    scaledMetrics, scaler= calcMetrics(imageName, tileSize, overlap) 
    
    learnSVR(scaledMetrics, tileSize, overlap, imageSize)
    