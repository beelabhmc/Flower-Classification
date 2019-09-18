from PIL import Image
from ImageProcess import * 

im = Image.open('images/Research_April24_S3P4.jpg')
count, pixList = textureAnalysis(im)
pixels = im.load() 

contrast, dissim, homog, energy, corr,ASM  = GLCM(im)

