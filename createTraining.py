import numpy 
def createTraining(locations, species): 
    """Do stuff"""
    training = numpy.zeros(50)
    for i in range(len(locations)):
        meter = locations[i] -1
        training[meter] = species[i]
    return training
    
def createImList(transectName, numPics): 
    """Create a list of image names for a give transect so that they can easily be read in.""" 
    imList = []
    for i in range(numPics):
        currentPic = str(transectName) + str(i+1) + ".jpg"
        imList += [currentPic]
    return imList
    
    
def numericalSpecies(species): 
    """Change the species from scientific names into corresponding numbers to be used in classification.
    This is necessary because not all algorithms support non-numerical class labels. In order to 
    test multiple algorithms and to have code that can easily be modified to use new algorithms, 
    class labels are integers rather than strings, as this extends more easily across algs.
    
    species: the list of string class labels""" 
    newSpecies = range(len(species))
    for i in range(len(species)): #for each species listed 
        currentSpecies = species[i]
        if currentSpecies == "Brassica nigra": 
            newSpecies[i] = 1 
        elif currentSpecies == "Pseudognaphalium californicus": 
            newSpecies[i] = 2
        elif currentSpecies == "Penstemon spectabilis": 
            newSpecies[i] = 3
        elif currentSpecies == "Eriogonum fasciculatum": 
            newSpecies[i] = 4
        elif currentSpecies == "Malosma laurina": 
            newSpecies[i] = 5
        elif currentSpecies == "Acmispon glaber": 
            newSpecies[i] = 6
        elif currentSpecies == "Eriogonum gracile": 
            newSpecies[i] = 7 
        elif currentSpecies == "Croton setigerus": 
            newSpecies[i] = 8 
        elif currentSpecies == "Hirschfeldia incana": 
            newSpecies[i] = 9
        elif currentSpecies == "Centaurea melitensis": 
            newSpecies[i] = 10
        elif currentSpecies == "Mirabilis laevis": 
            newSpecies[i] = 11
        elif currentSpecies == "Erodium cicutarium": 
            newSpecies[i] = 12
        elif currentSpecies == "Marrubium vulgare": 
            newSpecies[i] = 13
        elif currentSpecies == "Eriodictyon trichocalyx": 
            newSpecies[i] = 14
        elif currentSpecies == "Phacelia distans": 
            newSpecies[i] = 15
        elif currentSpecies == "Camissoniopsis bistorta": 
            newSpecies[i] = 16
        elif currentSpecies == "Cryptantha Species": 
            newSpecies[i] = 17
        elif currentSpecies == "Apiastrum angustifolium": 
            newSpecies[i] = 18      
        else: 
            newSpecies[i] = 0 # species 0 for no flowers or some random unknown value. 
    return newSpecies
    
def checkTrainingSize(imList, trainingData): 
    if len(imList) != len(trainingData): 
        if len(imList) > len(trainingData): 
            imList = imList[0:len(trainingData)] 
        elif len(trainingData) > len(imList): 
            trainingData = trainingData[0:len(imList)]
    return imList, trainingData