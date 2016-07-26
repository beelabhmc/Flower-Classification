from ImageProcess import * #Import the same functions from image process for density stuff. 

#No probabilities included 

def oneSpeciesOverlap((i,j), n, imageName, overlap, subTileDict, fit, scaler, reduceFeatures, featureSelect): 
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
    species = fit.predict(newMetric) #Find which species this is. 
    #speciesProb = fit.predict_proba(scaledMetric) #Calculate the probability of the species. 
   # return list(species), list(speciesProb) #return species and matching prob of those species. 
    return list(species)
def allSpeciesOverlap(n, imageName, overlap,fit, scaler, reduceFeatures, featureSelect): 
    """Computes all densities on a map with tilesize n, the given image as the map, and an overlap 1-overlap."""
    image = Image.open(imageName) 
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
            currentSpecies = oneSpeciesOverlap((m,k), n, imageName, overlap, subTileDict, fit, scaler, reduceFeatures, featureSelect)

            allSpecies += currentSpecies
          #  allProb += currentProb
    return allSpecies #return one map of species and one map of the corresponding probability. 

def SpeciesMapShort(species,imageName, overlap, n):
    image = Image.open(imageName) #open the image
    imageSize = image.size
    overlapSize = int(overlap*n)
    width = imageSize[0] 
    height = imageSize[1] 
    rowTiles = int((width-n)/(overlapSize))+1
        
    pointsx = [] #find the points where species was determined
    pointsy = []
    for i in range(len(species)):
        x = (i%rowTiles)*overlapSize + n/2
        y = (i/rowTiles)*overlapSize + n/2
        pointsx += [x]
        pointsy += [y]
    pointsx = numpy.array(pointsx)
    pointsy = numpy.array(pointsy)
    #print(points)

    #interpolation
    #points = tuple(points) #Convert array to numpy array. 
    grid_x, grid_y = numpy.mgrid[0:width, 0:height]

   # print(species)
    species = numpy.array(species)
    data = griddata((pointsx, pointsy), species, (grid_x, grid_y), method = 'nearest')
    
    #Plotting stuff
    #v = numpy.linspace(min(species), max(species), (max(species) - min(species)), endpoint=True)
    fig = plt.contourf(grid_x, grid_y, data, alpha = 0.6, antialiased = True)

    
    mapIm = Image.open(imageName)
    plt.imshow(mapIm)
    x = plt.colorbar(fig)
    plt.savefig('USS_June7_Classes.jpg')

def classifyMap(classifier, densityList, metricList,scaler,imageName, tileSize, overlap, featureSelect):
    reduceFeatures = 1 #reduce the number of features if 1, if 0 use all features.
    Species = allSpeciesOverlap(tileSize, imageName, overlap,classifier, scaler, reduceFeatures, featureSelect)
  #  print(Species)
    SpeciesMapShort(Species, imageName, overlap, tileSize) 
    return