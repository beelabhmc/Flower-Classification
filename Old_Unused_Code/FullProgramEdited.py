# -*- coding: utf-8 -*-
from ImageProcess import * 
from MachineLearning import *
import DensityAlignment
import math

NUMBERMETRICS = 7 #Set the number of metrics as a global variable here. 
    
def totalSVR(densityList, imageName,tileSize, overlap, trainingType): 
    """Does a complete run of the SVR learning algorithm. Takes in a training set of density
        data, an imageName in a string, the size of tile desired and an overlap as a percentage."""
        
    #trainingType: 0 = transect 
    #              1 = picList 
    #              2 = previous data set 
    #              3 = Other kind of data set (experimenting)
                  
    ##Note that if you have multiple transects you can simply save each transects group of pictures as a picList and then use method 1. 
    
                  
    if trainingType == 0: ###You want to pull data from a transect picture. 
        
        #Get user inputs to determine the transect image being used, and the start and end coordinates of the transect. 
        TransectName = input("Please input the transect image name as a string:" )
        Start = input("Please input the coordinates at the START of the transect:")
        End = input("Please input the coordinates at the END of the transect:")

        #Based on those user inputs create a list of transect images 
        imageList = DensityAlignment.divideTransect(Start, End,TransectName) ## Divide the transect into 50 images. Store in a list. 
        
        
        ##Compute the metrics on each training image. 
        metricList, densityList = allTrainMetricsTransect(imageList, densityList)
        
        ### Save the training set  - metrics
        f = open('metricListTraining.txt', 'w')
        print >> f, list(metricList)
        f.close()
        
        ### Save the training set - densities 
        f = open('densityListTraining.txt', 'w')
        print >> f, densityList 
        f.close()
        
    if trainingType == 1:  ##pull in pictures titled '1.jpg', etc. 
        numpics = len(densityList)  ##Get the number of pics from the density List (they have to be the same size). 
        imageList = makePicList(numpics)
        
        metricList, densityList = allTrainMetrics(imageList, densityList)
        

        
        densityList = [int(i) for i in densityList]
        
        ### Save the training set  - metrics
        f = open('metricListTraining.txt', 'w')
        print >> f, list(metricList)
        f.close()
        
        ### Save the training set - densities 
        f = open('densityListTraining.txt', 'w')
        print >> f, densityList 
        f.close()        
        
    if trainingType == 2:  #Just read in old data that was already saved.
        f = open('metricListTraining.txt', 'r')
        data = f.read()
        metricList = eval(data)
        
        g = open('densityListTraining.txt', 'r')
        data = g.read()
        print data
        densityList = eval(data)

        
    if trainingType == 3:  ### Other types of training sets. Manually enter here so that the other code doesn't need to change. 
        imageList = ['test1.jpg', 'test2.jpg']
        densityList = [1, 0]
        metricList , densityList = allTrainMetrics(imageList, densityList)
        
    ##Step 2: Scale the incoming training data 
    
    scaledTraining, scaler = scaleMetrics(metricList)  #Scale the training metrics to mean 0 and std 1 
    
    ### Train the machine learning algorithm 
    fit = svrAlg(scaledTraining, densityList)  #fit the algorithm 
    
    print 'Machine Learning done'
    
    ###Calculate densities on full image 
    
    CalcMetrics = input("Would you like to calculate a new set of image metrics? True or False.")
    if True: #Make true if you need to calculate image metrics on a new image. Otherwise make false
        imageDens = allDensOverlap(tileSize, imageName, overlap, densityList, metricList, fit, scaler)
        fileName = imageName[0:-4] + 'Densities' +  '.txt'
        f = open(fileName, 'w')
        print >> f, list(imageDens)
        f.close()
    else: 
        fileName = imageName[0:-4] + 'Densities' +  '.txt'
        f = open(fileName, 'r')
        data = f.read()
        imageDens = eval(data)

    print 'Image densities computed'
    densMapShort(imageDens,imageName, overlap, tileSize)

def totalGauss(densityList, imageName,tileSize, overlap, trainingType): 
    """Does a complete run of the SVR learning algorithm. Takes in a training set of density
        data, an imageName in a string, the size of tile desired and an overlap as a percentage."""
    image = Image.open(imageName)
    imageSize = image.size
    
    #trainingType: 0 = transect 
    #              1 = picList 
    #              2 = previous data set 
                  
    ##Note that if you have multiple transects you can simply save each transects group of pictures as a picList and then use method 1. 
    
                  
    if trainingType == 0: ###You want to pull data from a transect picture. 
        
        #Get user inputs to determine the transect image being used, and the start and end coordinates of the transect. 
        TransectName = input("Please input the transect image name as a string:" )
        Start = input("Please input the coordinates at the START of the transect:")
        End = input("Please input the coordinates at the END of the transect:")

        #Based on those user inputs create a list of transect images 
        imageList = DensityAlignment.divideTransect(Start, End,TransectName) ## Divide the transect into 50 images. Store in a list. 
        
        
        ##Compute the metrics on each training image. 
        metricList, densityList = allTrainMetricsTransect(imageList, densityList)
        
        ### Save the training set  - metrics
        f = open('metricListTraining.txt', 'w')
        print >> f, list(metricList)
        f.close()
        
        ### Save the training set - densities 
        f = open('densityListTraining.txt', 'w')
        print >> f, densityList 
        f.close()
        
    if trainingType == 1:  ##pull in pictures titled '1.jpg', etc. 
        numpics = len(densityList)  ##Get the number of training images from the density list (these must be the same length). 
        imageList = makePicList(numpics)
        
        metricList, densityList = allTrainMetrics(imageList, densityList)
        
        ### Save the training set  - metrics
        f = open('metricListTraining.txt', 'w')
        print >> f, list(metricList)
        f.close()
        
        ### Save the training set - densities 
        f = open('densityListTraining.txt', 'w')
        print >> f, densityList 
        f.close()        
            
        
    if trainingType == 2: 
        print('Using previously calculated metric and density lists for training.')
        f = open('metricListTraining.txt', 'r')
        data = f.read()
        metricList = eval(data)
        
        
        g = open('densityListTraining.txt', 'r')
        data = g.read()
        densityList = eval(data)
        
    if trainingType == 3: 
        print('Using other type of training data')
        imageList = ['test1.jpg', 'test2.jpg']
        densityList = [100, 0]
        metricList , densityList = allTrainMetrics(imageList, densityList)
        
    ##Step 2: Scale the incoming training data 
    
    scaledTraining, scaler = scaleMetrics(metricList) 
    

    fit = gaussReg(scaledTraining, densityList)  ## Fit using Gaussian Regression
    
    
    print 'Machine Learning done'
    
    ###Calculate densities on full image 
    
    if True: #Make true if you need to calculate image metrics on a new image. Otherwise make false
        imageDens = allDensOverlap(tileSize, imageName, overlap, densityList, metricList, fit, scaler)
        fileName = imageName[0:-4] + 'Densities' +  '.txt'
        f = open(fileName, 'w')
        print >> f, list(imageDens)
        f.close()
    else: 
        fileName = imageName[0:-4] + 'Densities' +  '.txt'
        f = open(fileName, 'r')
        data = f.read()
        imageDens = eval(data)

    print 'Image densities computed'
    densMapShort(imageDens,imageName, overlap, tileSize)
 


    
    
def makePicList(numSites): 
    """makes an image name list for a given number of sites.""" 
    nameList = []
    for i in range(numSites): #for each site 
        currentName = str(i+1)+".jpg" 
        nameList += [currentName]
    return nameList
        
#if __name__ == "__main__":
    
    #totalSVR(['SuperSmallTile.jpg'], [0.5], 'SmallTile.jpg', 75, 0.5)

    
    