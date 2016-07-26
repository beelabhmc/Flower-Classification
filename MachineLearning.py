from sklearn.svm import SVR
import numpy
from PIL import Image
import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from sklearn.gaussian_process import GaussianProcess
import sklearn
import math
import OpenGL
from mpl_toolkits.mplot3d import Axes3D


def svrAlg(X, densities): 
    """Runs a Support Vector Regression Algorithm on X, an array of metrics 
        and densities, the corresponding densities. Note that X and densities should be updated 
        with actual field data collected."""
   # X = [[0, 0], [2, 2]] #X is the array of metrics 
    #densities = [0.5, 2.5] #densities are the measured densities 
    clf = SVR( kernel = 'rbf', gamma = 0.05, epsilon = 0.4) #initialize support vector regression thing. 

    clf.fit(X,densities) #trains the model 

    return clf
    
def gaussReg(metrics, densities): 
  #  metrics = [[0, 0], [2, 2]] #List of lists of metrics calculated 
   # densities =  [0.5, 2.5] #The corresponding densities 
    
    gp = GaussianProcess(corr='absolute_exponential', theta0=1e-1,
                     thetaL=1e-3, thetaU=1,
                     random_start=100)    #Change these parameters to get better fit...            
    gp.fit(metrics, densities)
    return gp


    ##Number of tiles in one row (width-n)/(overlapSize)+1)
def densMap(fit, metricArray, n, overlap, imageSize, imageName): 
    """Creates and saves a contour plot of densities based on an 
        input fit function, metrics, and image size characteristics."""
        
    if True: #Make true if you want to calculate densities (i.e. if you have a new fit/new density list)  
        print 'calculating densities'
        if type(fit)==sklearn.gaussian_process.gaussian_process.GaussianProcess: #If the fit is Gaussian
            densities, MSE = fit.predict(metricArray, eval_MSE =True)
            sigma = numpy.sqrt(MSE)
            print(sigma)
        else:
            densities = fit.predict(metricArray) #Use the ML fit to predict the density for each tile 
            #print len(densities)
        f = open('densities.txt', 'w')
        print >> f, list(densities)
        f.close()
    else: 
        f = open('densities.txt', 'r')
        data = f.read()
        densities = eval(data)
       # print densities
        densities = numpy.array(densities)
        f.close()
        imageName = 'FirstStitchLong.jpg'
        overlap = 0.2 
        n = 50
        image = Image.open(imageName) #open the image
        imageSize = image.size #get the image size 
 #   print 'Image Size is ', imageSize
 

    width = imageSize[0] 
    height = imageSize[1] 
   # print 'width ', width 
    #print 'height ', height
    overlapSize = int(overlap*n)
    rowTiles = int((width-n)/(overlapSize))+1
    print 'Row Tiles is ', rowTiles
    #colTiles = int(((height-n)/(overlapSize))+1)
    
    
 #   newArray = numpy.zeros((int((width-n)/(overlapSize)+1),int(((height-n)/(overlapSize))+1)))
 
    #newArray = numpy.zeros(width, height)
    #print newArray
    points = []
    for i in range(len(densities)):
        x = (i%rowTiles)*overlapSize + n/2
        y = (i/rowTiles)*overlapSize + n/2
        points += [[x,y]]
       # newArray[i%(rowTiles),i/(rowTiles)] = densities[i]
      # newArray[(i%(rowTiles)+1)*(n/2) , (i/(rowTiles)+1)*(n/2)] = densities[i]
      # points += [[(i%(rowTiles)+1)*(n/2), (i/(rowTiles)+1)*(n/2)]] #Consider the density to be at the center of each tile 
  #  print points
    grid_x, grid_y = numpy.mgrid[0:width, 0:height]  #create a meshgrid 
     
   # print densities
   # print('Points is ', points) 
   # print('Densities is ', densities)
    data = griddata(points, densities, (grid_x, grid_y), method = 'linear') #interpolate to get continuous function of points 
    #can change interpolation method
    print data.size

  #  print 'Max is ', numpy.amax(data)
   # min_max_scaler = sklearn.preprocessing.MinMaxScaler()
    #data_minmax = min_max_scaler.fit_transform(data) 
    
  
    
    ##Plotting 
    plt.figure(1)
    
    #plt.figure(figsize = (width, height))
  #  print "Hi Cassie"
    v = numpy.linspace(min(densities), max(densities), 20, endpoint=True)
    fig = plt.contourf(grid_x, grid_y, data, levels = v, alpha = 0.4, antialiased = True)
    
    mapIm = Image.open(imageName)
    plt.imshow(mapIm)
    maxDens = max(densities)
    print maxDens  
    x = plt.colorbar(fig)   
    plt.savefig('ContourPlot.jpg')
    return data
    
    
def densMapShort(densities,imageName, overlap, n): 
    image = Image.open(imageName) #open the image
    imageSize = image.size
    overlapSize = int(overlap*n)
    width = imageSize[0] 
    height = imageSize[1] 
    rowTiles = int((width-n)/(overlapSize))+1
        
    points = [] #Compute the points where densities are being plotted
    for i in range(len(densities)):
        x = (i%rowTiles)*overlapSize + n/2
        y = (i/rowTiles)*overlapSize + n/2
        points += [[x,y]]
    #interpolation
    grid_x, grid_y = numpy.mgrid[0:width, 0:height]
    data = griddata(points, densities, (grid_x, grid_y), method = 'linear')
    
    #Plotting stuff
    v = numpy.linspace(min(densities), max(densities), 20, endpoint=True)
    fig = plt.contourf(grid_x, grid_y, data, levels = v, alpha = 0.4, antialiased = True)

    mapIm = Image.open(imageName)
    plt.imshow(mapIm)
    x = plt.colorbar(fig)
    plt.savefig('TransectContour.jpg')
    
def testDensMap(n, overlap, imageName): 
    densities = [] 
    image = Image.open(imageName) 
    imageSize = image.size 
    width = imageSize[0]
    overlapSize = int(n*overlap)
   # rowTiles = math.ceil((width-n)/(overlapSize))
    print imageSize
    for i in range(n/2, imageSize[1], int(overlap*n)): #For the entire height of the picture 
       # print 'row number ', i
        #for j in range(0,imageSize[0]/2,int(overlap*n)): #For the first third of the image 
        #    densities += [0.8] 
        # #   print 'j ', j
        #for k in range(imageSize[0]/2, imageSize[0]-n, int(overlap*n)): #For the rest of the image 
        #    densities += [0.2] 
        for m in range(0, imageSize[0]-n, int(overlap*n)): 
            if m < imageSize[0]/2: 
                densities += [0.8] 
            else: 
                densities += [0.2]

         #   print 'k ', k
   # print 'Densities are ', densities 
    print 'Densities computed! Plotting now...'
    densMapShort(densities, imageName,overlap,n) 
    
def overlayMap(mapName, contourName): 
    """Overlays the images of a contour map and the original aerial map. Saves the output.
    Note that the contour plot must be cropped to only include the contour image before 
    running this. """
    mapIm = Image.open(mapName) 
    contour = Image.open(contourName)
  #  contour.convert('RGBA')
   # contour.putalpha(30)
    plt.figure(2)
    plt.imshow(contour)
    mapIm.convert('RGBA') #Add a transparency layer to the image
    mapIm.putalpha(150) #higher number = darker image. Max = 255
    plt.imshow(mapIm) #Plot the overlaid map
    
    plt.savefig('OverlayMap.jpg')
    
    
def learnSVR(metricArray, n, overlap, imageSize, fit): 
    """A wrapper function for the machine learning algorithm and post-processing.""" 
   # fit = svrAlg() 
   # metricArray = [[1,1],[2,3],[4,5], [3,7],[70,20],[5,20],[9,18], [87,34],[43,127], [1,10],[5,3],[4,8], [3,90],[76,20],[500,20],[29,34], [38,34],[43,17]]
  #  n= 50  #Change your metrics here!!!!!!!!!
   # overlap = 0.3 
    #imageSize = [100,400]
    
    densMap(fit, metricArray, n, overlap, imageSize )
    overlayMap('SmallTile.jpg', 'ContourPlot.jpg') 
    # Final map is saved as OverlayMap.jpg
    
    
def learnGauss(metricArray): 
    """A wrapper function for the Gaussian machine learning algorithm and post-processing.""" 
    fit = gaussReg() 
    n= 100  #You should probably change this...
    overlap = 0.3 
    imageSize = [100,400]
    densMap(fit, metricArray, n, overlap, imageSize )
    overlayMap('SmallTile.jpg', 'ContourPlot.jpg') 
    # Final map is saved as OverlayMap.jpg
    
