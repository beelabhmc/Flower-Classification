from Constants import *
import xml.etree.ElementTree as ET
import createTraining as ct

def readMasks(MaskPath):
    MaskPath = 'research_may15/'
    tree = ET.parse(IMAGE_PATH + MaskPath + 'Research_May15_small.xml')
    root = tree.getroot()
    obj = root.findall('object') #Find all of the masks    
    species = []
    mask_names = []
    for mask in obj: #For each of these masks... 
        seg = mask.find('segm')
        if seg is None: 
            continue
        mask_name = seg.find('mask').text
        mask_names += [mask_name]
        name = mask.find('name').text
        species += [name] 
    mask_species = ct.numericalSpecies(species)
    return [mask_species, mask_names]