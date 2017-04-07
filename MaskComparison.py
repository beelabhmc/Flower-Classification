from Constants import *
import xml.etree.ElementTree as ET

MaskPath = 'research_may15/'
May15MaskList = ['Research_May15_small_mask_0.png','Research_May15_small_mask_1.png',
'Research_May15_small_mask_3.png',
'Research_May15_small_mask_5.png','Research_May15_small_mask_6.png',
'Research_May15_small_mask_7.png','Research_May15_small_mask_8.png',
'Research_May15_small_mask_9.png','Research_May15_small_mask_10.png',
'Research_May15_small_mask_11.png','Research_May15_small_mask_12.png',
'Research_May15_small_mask_13.png','Research_May15_small_mask_14.png',
'Research_May15_small_mask_15.png','Research_May15_small_mask_16.png',
'Research_May15_small_mask_17.png','Research_May15_small_mask_18.png',
'Research_May15_small_mask_19.png',
'Research_May15_small_mask_27.png']


tree = ET.parse(IMAGE_PATH + MaskPath + 'Research_May15_small.xml')
root = tree.getroot()


