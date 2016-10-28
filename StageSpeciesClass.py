from ImageProcess import * #Import the same functions from image process for density stuff. 
from Constants import *
#No probabilities included 

def oneSpeciesOverlap_2stage((i,j), n, imageName, overlap, subTileDict, fit_species, fit_flowers, scaler, reduceFeatures, featureSelect): 
    """Computes the species of one tile with overlap""" 
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
  #  print metricTotal
    num = 1/(overlap**2)
    avgMetric = [a/num for a in metricTotal] #Compute the average 
    # print avgMetric
    scaledMetric = scaler.transform(avgMetric) #Scale the metric 
    if reduceFeatures: 
        newMetric = featureSelect.transform(scaledMetric)
    flower = fit_flowers.predict(newMetric) #determine if this is a flower or not 
    if flower: 
        species = fit_species.predict(newMetric) #Find which species this is. 
    else: 
        species = flower #if not a flower, it can't have a species. 
        
    #speciesProb = fit.predict_proba(scaledMetric) #Calculate the probability of the species. 
   # return list(species), list(speciesProb) #return species and matching prob of those species. 
    return list(species)
def allSpeciesOverlap_2stage(n, imageName, overlap,fit_species, fit_flowers, scaler, reduceFeatures, featureSelect): 
    """Computes all species on a map with tilesize n, the given image as the map, and an overlap 1-overlap."""
    image =  Image.open(imageName) 
    imageSize = image.size 
    width = imageSize[0]
    height = imageSize[1] 
   # densityList = []
    
    subTileDict = getSub(n, imageName, overlap) #Compute the metrics on subtiles 

    allSpecies = []
    allProb = []
    shiftSize = int(n*overlap)
    for k in range(0, height -n, shiftSize): 
        for m in range(0, width - n, shiftSize): 
          #  print (m,k)
          #  currentSpecies, currentProb = oneSpeciesOverlap((m,k), n, imageName, overlap, subTileDict, fit, scaler)
            currentSpecies = oneSpeciesOverlap_2stage((m,k), n, imageName, overlap, subTileDict, fit_species, fit_flowers, scaler, reduceFeatures, featureSelect)

            allSpecies += currentSpecies
          #  allProb += currentProb
    return allSpecies #return one map of species and one map of the corresponding probability. 

def SpeciesMapShort(species,imageName, overlap, n):
    """Similar to densMapShort except it produces a map for species."""
    image = Image.open(imageName) #open the image
    imageSize = image.size #get the image size. 
    overlapSize = int(overlap*n)#Figure out how many pixels to shift by. 
    width = imageSize[0] 
    height = imageSize[1] 
    rowTiles = int((width-n)/(overlapSize))+1 #calculate the number of tiles in a row. 
        
    pointsx = [] #initialize empty lists to hold the point location data. 
    pointsy = []
    for i in range(len(species)):  #find the points where species was determined
        x = (i%rowTiles)*overlapSize + n/2
        y = (i/rowTiles)*overlapSize + n/2
        pointsx += [x]
        pointsy += [y]
    pointsx = numpy.array(pointsx) #convert points to numpy arrays for future operations. 
    pointsy = numpy.array(pointsy)
    #interpolation
    grid_x, grid_y = numpy.mgrid[0:width, 0:height] #create a grid to interpolate over.

   # print(species)
    species = numpy.array(species)
    data = griddata((pointsx, pointsy), species, (grid_x, grid_y), method = 'nearest')
    
    #Plotting stuff
    #v = numpy.linspace(min(species), max(species), (max(species) - min(species)), endpoint=True)
    fig = plt.contourf(grid_x, grid_y, data, alpha = 0.6, antialiased = True) #Plot the data overlaid with the orignial image. 

    
    mapIm = Image.open(imageName)
    plt.imshow(mapIm)
    x = plt.colorbar(fig) #show the colorbar
    plt.savefig(imageName + '_Classes.jpg') #Save the figure. Change the name here or rename the file after it has been saved. 

def classifyMap_2stage(classifier_species, classifier_flowers, densityList, metricList,scaler,imageName, tileSize, overlap, featureSelect):
    """Classify map calculates all of the species classes for an image and produces a map 
    of those species overlaid with the original map.
    classifier - a trained classification algorithm. 
    metricList - the list of training metrics (list) 
    scaler - the scaler used to scale the data 
    imageName - the name of the image to analyse (string) 
    tileSize - the desired size of tile to use in calcualting metrics (int)
    overlap - how much the tiles should overlap with each other
    featureSelect -  the test algorithm that will select which features to use. Only relevant if reduceFeatures is 1. """
    reduceFeatures = 1 #reduce the number of features if 1, if 0 use all features.
    Species = allSpeciesOverlap_2stage(tileSize, imageName, overlap,classifier_species, classifier_flowers, scaler, reduceFeatures, featureSelect) #Find all of the species classes. 
    SpeciesMapShort(Species, imageName, overlap, tileSize) #Display the map. 
    return Species #return the calculated species so that they can be analyzed for other purposes, i.e. clustering, etc. 