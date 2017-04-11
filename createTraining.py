import numpy 
from Constants import * 
import ImageProcess as IP
from PIL import Image 

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
        currentPic = IMAGE_PATH + str(transectName) + str(i+1) + ".jpg"
        imList += [currentPic]
    return imList
    
    
def tiledTraining(imList, species, overlap, n): 
    """Take in a list of training images and their corresponding species. 
    Create a new set of images through tiling and return a list 
    of training metrics and species for each subimage.""" 
    metricList = [] #initialize an empty list of metrics. This will be used to track metrics for each data point. 
    speciesList = [] #initialize an empty list of species. This will be expanded to have multiple points for each photo. 
    for i in range(len(imList)): #for each image you are training on. 
        imMetrics = [] #keep track of metrics for this image seperatly. 
        image = Image.open(imList[i]) #load in the image.
    #Find the size of the image. 
        size = image.size
        width = size[0] #pull out length and width 
        length = size[1] 
        smallTileSize = int(overlap*n) #Set the tilesize and overlap you want to train on. This should match the size you will test on. 
    # Extract all tiles using a specific overlap (overlap depends on n). This happens for each image.
        for k in range(0,width -smallTileSize, smallTileSize): #Go through the entire image 
            for j in range(0, length - smallTileSize, smallTileSize): 
                box = (k,j,k+smallTileSize, j+smallTileSize)  #edge coordinates of the current rectangle. 
                newImage = image.crop(box) #pull out the desired rectangle
            ### METRIC CALCULATIONS: Get the metrics for each subrectangle in the image. 
                Metrics = IP.getMetrics(newImage) #calculate all of the metrics on this cropped out image. 
                imMetrics += [Metrics] #add these metrics to a list, imMetrics, that will keep track of metrics within each image. 
        imSpecies = len(imMetrics)*[species[i]] #Extend the species list (mark all subrectangles as the same species)
        metricList += imMetrics #add to the overall lists of metrics and species 
        speciesList += imSpecies 
    return metricList, speciesList #Return the overal metric and species lists. These now include subdivided portions of each image. 

    
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
        elif currentSpecies == "Penstemon spectabilis" or currentSpecies == 'penstemon spectabilis': 
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
        elif currentSpecies == "Cryptantha intermedia": 
            newSpecies[i] = 17
        elif currentSpecies == "Apiastrum angustifolium": 
            newSpecies[i] = 18   
        elif currentSpecies == "Salvia apiana": 
            newSpecies[i] = 19    
        else: 
            newSpecies[i] = 0 # species 0 for no flowers or some random unknown value. 
    return newSpecies
    
def checkTrainingSize(imList, trainingData):
    """check the training set sizes to make sure imList and trainingData are the same size.""" 
    if len(imList) != len(trainingData): 
        if len(imList) > len(trainingData): 
            imList = imList[0:len(trainingData)] 
        elif len(trainingData) > len(imList): 
            trainingData = trainingData[0:len(imList)]
    return imList, trainingData