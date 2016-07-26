from ImageProcess import * #Import the same functions from image process for density stuff. 

def oneSpeciesOverlap((i,j), n, imageName, overlap, subTileDict, fit, scaler): 
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
  #  print metricTotal
    num = 1/(overlap**2)
    avgMetric = [a/num for a in metricTotal] #Compute the average 
    # print avgMetric
    scaledMetric = scaler.transform(avgMetric) #Scale the metric 
    species = fit.predict(scaledMetric) #Find which species this is. 
    speciesProb = fit.predict_proba(scaledMetric) #Calculate the probability of the species. 
    return list(species), list(speciesProb) #return species and matching prob of those species. 
    
    
def allSpeciesOverlap(n, imageName, overlap, densityList, metricList, fit, scaler): 
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
            currentSpecies, currentProb = oneSpeciesOverlap((m,k), n, imageName, overlap, subTileDict, fit, scaler)
            allSpecies += currentSpecies #Add the species to the list 
            allProb += currentProb #Add the probability of that species being correct to a seperate list 
    return allSpecies, allProb #return one map of species and one map of the corresponding probability. 

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
   # v = numpy.linspace(min(species), max(species), 20, endpoint=True)
    fig = plt.contourf(grid_x, grid_y, data, alpha = 0.4, antialiased = True)

    
    mapIm = Image.open(imageName)
    plt.imshow(mapIm)
    x = plt.colorbar(fig)
    plt.savefig('Test.jpg')
    
def SingleSpeciesProbMap(prob,imageName, overlap, n):
    """Creates a map of the locations of a single species, overlaid with the original map. The map is shaded by the probability 
    of that species being correct, as calculated by the machine learning prediction algorithm. 
    This is not necessarily available from every classification algorithm, so check that the fit used to predict the densities does in 
    fact produce a probability, and ensure that the probability calcualtion function is called correctly in oneSpeciesOverlap. 
    
    Species = list of the species in the map 
    imageName = the image that the species are being calculated for 
    overlap = the overlap between tiles (1/overlap = integer)
    n = tile size """
    
    image = Image.open(imageName) #open the image
    imageSize = image.size
    overlapSize = int(overlap*n)
    width = imageSize[0] 
    height = imageSize[1] 
    rowTiles = int((width-n)/(overlapSize))+1
        
    pointsx = [] #find the points where species was determined
    pointsy = []
    for i in range(len(prob)):
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
    prob = numpy.array(prob)
    data = griddata((pointsx, pointsy), prob, (grid_x, grid_y), method = 'nearest')
    
    #Plotting stuff
    #v = numpy.linspace(min(species), max(species), 20, endpoint=True)
    fig = plt.contourf(grid_x, grid_y, data, alpha = 0.4, antialiased = True)

    mapIm = Image.open(imageName)
    plt.imshow(mapIm)
    x = plt.colorbar(fig)
    plt.savefig('SpeciesTest.jpg')
    plt.show()

def classifyMapProb(classifier, speciesList, metricList,scaler, SPECIES):
    Species, Prob = allSpeciesOverlap(50, "0015_Cassie.JPG", 0.2, speciesList, metricList, classifier, scaler)
    for i in range(len(Species)):  
        if Species[i]!= SPECIES: #If this pixel isn't the species we are interested in            
            Prob[i] = 0 #Set the probability of being SPECIES to 0. 
        else: 
          #  print(Prob[i])
            ProbList = Prob[i] 
            Prob[i] = ProbList[SPECIES]
            print(Prob[i])
    SingleSpeciesProbMap(Prob, "0015_Cassie.JPG", 0.2, 50)  #Map the probabilities  
    return