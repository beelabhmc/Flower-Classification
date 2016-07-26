import numpy
from createTraining import * 
from DensityAlignment import *
#BSSA June 3 

def BSSTrainJune3():
    BSSA_locations = [20, 29, 30, 30, 31, 31, 32, 37, 38, 39, 40, 41, 42, 45, 47, 48, 49, 50]

    BSSA_Species = ["Brassica nigra","Brassica nigra", "Brassica nigra", "Pseudognaphalium californicus", "Pseudognaphalium californicus",  "Brassica nigra", "Brassica nigra", "Brassica nigra", "Brassica nigra", "Brassica nigra", "Brassica nigra", "Penstemon spectabilis", "Penstemon spectabilis", "Penstemon spectabilis", "Brassica nigra", "Brassica nigra", "Brassica nigra", "Brassica nigra"]
    BSSA_SpeciesNum = numericalSpecies(BSSA_Species)
    BSSA_training = numpy.zeros(50)

    BSSA_training = createTraining(BSSA_locations, BSSA_SpeciesNum)

    BSSIms = createImList("BSSA63", 48)

    BSSImList, BSS_Train = checkTrainingSize(BSSIms, BSSA_training)
    
    return BSSImList, BSS_Train
    
def GeneralTrainingList(Locations, Species, Name, imageName, Start, End):
    """Input the locations, species, and transect name, and imageName for any transect and get out a formatted list of images and training data."""
    
    imList = divideTransect(Start, End, imageName)#divide up the relevant transect into 1x2 m sections. 
   # print('imList is ', imList)
    saveTransect(imList, 1, Name) #save all of the transect images 
    
    
    SpeciesNum = numericalSpecies(Species) #convert species names to numbers
    Training = numpy.zeros(50) #initialize a training list defaulting to "other" 

    Training = createTraining(Locations, SpeciesNum) #create a training set. 

    Ims = createImList(Name, len(imList)) #create the image name list 

    TrainingIm, TrainingSpecies = checkTrainingSize(Ims, Training)#check that lists are the same size and rectify if not 
    
    return TrainingIm, TrainingSpecies  



def createAllTransectTraining(): 
    """Create a full transect training set.""" 
    
    ##Create species and image training lists for the 
    #USS May 25 - USS B (May 23)
    USSMay25Start = (5586, 9105)
    USSMay25End = (10932, 16608)
    USSMay25Locations = [4, 6, 11, 12, 13, 21, 14, 25, 39]
    USSMay25Species = ['Mirabilis laevis', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus']
    
    
    USSMay25TrainIm, USSMay25TrainSpecies = GeneralTrainingList(USSMay25Locations, USSMay25Species, 'USS_May25_', 'USS_May25.jpg', USSMay25Start, USSMay25End)
    
    
    #USS June 3 - USS A (May 31)
    USSJune3Start = (10864, 7165) 
    USSJune3End = (12446, 14564)
    USSJune3Locations = [2, 6, 17, 19, 27, 28, 34, 35, 39, 41, 42]
    USSJune3Species = ['Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus']
    
    
    USSJune3TrainIm, USSJune3TrainSpecies = GeneralTrainingList(USSJune3Locations, USSJune3Species, 'USS_June3_', 'USS_June3.jpg', USSJune3Start, USSJune3End)



    #USS June 7 - USS B (June 6)
    USSJune7Start = (5447, 8621) 
    USSJune7End = (10476, 15927)
    USSJune7Locations = [1, 2, 3, 4, 5, 6, 8, 9, 12, 14, 20, 21, 24, 30, 33, 35, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48, 50]
    USSJune7Species = ['Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus']
    
    
    USSJune7TrainIm, USSJune7TrainSpecies = GeneralTrainingList(USSJune7Locations, USSJune7Species, 'USS_June7_', 'USS_June7.jpg', USSJune7Start, USSJune7End)
    
    
    #NNG June 2 - NNG A (May 31 )
    NNGJune2Start = (5785, 27073)
    NNGJune2End = (4836, 13102)
    NNGJune2Locations = []
    NNGJune2Species = []
    
    NNGJune2TrainIm, NNGJune2TrainSpecies = GeneralTrainingList(NNGJune2Locations, NNGJune2Species, 'NNG_June2_', 'NNG_June2.jpg', NNGJune2Start, NNGJune2End)
    
    
    
    #BSS May 19 - BSS A (May 17)
    BSSMay19Start = (20955, 2382)
    BSSMay19End = (8515, 2643)
    BSSMay19Locations = [10, 20, 21, 22, 25, 27, 27, 28, 29, 30, 31, 31, 32, 35, 36, 38, 39, 40, 40, 41, 41, 42, 42, 43, 45, 46, 47, 48, 49, 50]
    BSSMay19Species = ['Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Marrubium vulgare', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Pseudognaphalium californicus', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Hirschfeldia incana', 'Brassica nigra', 'Penstemon spectabilis', 'Brassica nigra', 'Penstemon spectabilis', 'Brassica nigra', 'Brassica nigra', 'Penstemon spectabilis', 'Brassica nigra', 'Penstemon spectabilis', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra']
    
    BSSMay19TrainIm, BSSMay19TrainSpecies = GeneralTrainingList(BSSMay19Locations, BSSMay19Species, 'BSS_May19_', 'BSS_May19.jpg', BSSMay19Start, BSSMay19End)
    
    
    #BSS May 26 - BSS B (May 24)
    BSSMay26Start = (19870, 10738)
    BSSMay26End = (7740, 12406)
    BSSMay26Locations = [11, 15, 20, 22, 27, 33, 36, 40, 41, 42, 46, 47, 48, 49, 50]
    BSSMay26Species = ['Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Centaurea melitensis', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Hirschfeldia incana', 'Brassica nigra', 'Brassica nigra']
    
    BSSMay26TrainIm, BSSMay26TrainSpecies = GeneralTrainingList(BSSMay26Locations, BSSMay26Species, 'BSS_May26_', 'BSS_May26.jpg', BSSMay26Start, BSSMay26End)
    
    #BSS June 3 - BSS A (June 2)
    BSSJune3Start = (19236, 5244)
    BSSJune3End = (6800, 5577)
    BSSJune3Locations = [20, 29, 30, 30, 31, 31, 32, 37, 38, 39, 40, 41, 42, 45,47, 48, 49, 50]
    BSSJune3Species = ['Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Pseudognaphalium californicus', 'Pseudognaphalium californicus', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Penstemon spectabilis', 'Penstemon spectabilis', 'Penstemon spectabilis', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra']
     
    BSSJune3TrainIm, BSSJune3TrainSpecies = GeneralTrainingList(BSSJune3Locations, BSSJune3Species, 'BSS_June3_', 'BSS_June3.jpg', BSSJune3Start, BSSJune3End)
    
    
    #BSS June 8 - BSS B (June 7)
    BSSJune8Start = (18218, 9206)
    BSSJune8End = (8094, 10632)
    BSSJune8Locations = [23, 24, 33, 46, 50]
    BSSJune8Species = ['Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra', 'Brassica nigra']
    
    BSSJune8TrainIm, BSSJune8TrainSpecies = GeneralTrainingList(BSSJune8Locations, BSSJune8Species, 'BSS_June8_', 'BSS_June8.jpg', BSSJune8Start, BSSJune8End)
    
    
    #BRS May 27 - BRS B (May 26)
    BRSMay27Start = (5332, 15822)
    BRSMay27End = (18991, 12084)
    BRSMay27Locations = [2, 2, 23, 48]
    BRSMay27Species = ['Erodium cicutarium', 'Eriogonum fasciculatum', 'Eriogonum fasciculatum', 'Eriogonum fasciculatum']
    
    BRSMay27TrainIm, BRSMay27TrainSpecies = GeneralTrainingList(BRSMay27Locations, BRSMay27Species, 'BRS_May27_', 'BRS_May27.jpg', BRSMay27Start, BRSMay27End)
    
    
    
    
    FullTrainIm = USSMay25TrainIm + USSJune3TrainIm + USSJune7TrainIm + NNGJune2TrainIm + BSSMay19TrainIm + BSSMay26TrainIm + BSSJune3TrainIm + BSSJune8TrainIm + BRSMay27TrainIm
    FullTrainSpecies = numpy.concatenate((USSMay25TrainSpecies, USSJune3TrainSpecies, USSJune7TrainSpecies, NNGJune2TrainSpecies, BSSMay19TrainSpecies, BSSMay26TrainSpecies, BSSJune3TrainSpecies, BSSJune8TrainSpecies, BRSMay27TrainSpecies), axis = 0)
    
    return FullTrainIm, FullTrainSpecies 
    
    
    
    
    
    
    