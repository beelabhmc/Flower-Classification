import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import sys
from SpeciesTest import *
#from SpeciesClass import *

SCALE = 4 # the ratio of the original picture size to that of the reduced size pictures

def drawMatches(img1, kp1, img2, kp2, matches):
    """
        This function takes in two images with their associated
        keypoints, as well as a list of DMatch data structure (matches)
        that contains which keypoints matched in which images.
        
        An image will be produced where a montage is shown with
        the first image followed by the second image beside it.
        
        Keypoints are delineated with circles, while lines are connected
        between matching keypoints.
        
        img1,img2 - Grayscale images
        kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint
        detection algorithms
        matches - A list of matches of corresponding keypoints through any
        OpenCV keypoint matching algorithm
        """
    
    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]
    
    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')
    
    # Place the first image to the left
    out[:rows1,:cols1] = img1
    
    # Place the next image to the right of it
    out[:rows2,cols1:] = img2
    
    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:
        
        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx
        
        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt
        
        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)
        
        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)

    
    # Also return the image if you'd like a copy
    return out

def getFiles(directory, directorySmall):
    """
        This function takes as input two directories, the first containing the 
        original photos and the second containing the smaller version of
        those photos.
        
        It returns the file name of the smaller version of the stitched picture,
        a list of the names smaller version of the sections, the name of the original
        stitched picture and a list of the names of the original sections
        """
    jpgList = []
    for filename in os.listdir(directory):
        if filename.endswith(".JPG"):
            jpgList.append("/Users/beelab/Desktop/Flower-Classification/"+directory + "/"+filename)
    bigPicture = jpgList[0]
    bigSections = jpgList[1:]
    jpgList = []
    for filename in os.listdir(directorySmall):
        if filename.endswith(".JPG"):
            jpgList.append("/Users/beelab/Desktop/Flower-Classification/"+directorySmall + "/"+filename)
    picture = jpgList[0]
    sections = jpgList[1:]
    return picture, sections, bigPicture, bigSections

def findSections(picture, sections, bigPicture, bigSections):
    '''Takes as input the stitched picture (bigPicture) and the smaller sections of that picture (sections)
        and returns the species color overlay  for those sections as well as a dictionary with species data by location'''
    
    #Load the small and original stitched map images
    img2 = cv2.imread(picture,1)
    bigImg2 = cv2.imread(bigPicture,1)
    
    #Convert small stitched image to grayscale and use sift to find key points
    gray2 = cv2.cvtColor(img2 , cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT()
    kp2, des2 = sift.detectAndCompute(gray2, None)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck =True)
    #Initialize overlay
    overlay = np.zeros(bigImg2.shape, np.uint8)
    
    #Intialize data dictionary
    speciesDataD = {}
    clf, speciesTrain, newMetrics, scaler, tileSize, overlap, kbest = SpeciesTest()
    for i in range(len(sections)):
        #Load the small and original individual images
        img1 = cv2.imread(sections[i])
        bigImg1 = cv2.imread(bigSections[i])
        
        #Convert the small individual image to grayscale and use sift to find keypoints
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        kp1, des1 = sift.detectAndCompute(gray1, None)
        
        #Find the matches between the keypoints in the small individual image and the small stitched image
        matches = bf.match(des1, des2)
        
        fig, coords, species = returnClassifyMap(clf, speciesTrain, newMetrics, scaler, img1, tileSize, overlap, kbest)
        coords = combine(coords[0], coords[1])

        #Find the best matches from smaller image to stitched image
        good = []
        for m in matches:
            if m.distance < 75:
                good.append(m)
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        
        #Calculate homography matrix
        homography, status = cv2.findHomography(src_pts, dst_pts)
        
        
        h,w,_ = img1.shape
        pts = np.float32([[0,0]]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,homography)
        dst = np.int32(dst)
        
        #Update data dictionary
        partialDict = transformData(homography, coords, species, dst[0][0][0], dst[0][0][1])
        speciesDataD.append(partialDict)


        startX = SCALE * dst[0][0][0]
        startY = SCALE * dist[0][0][1]
        for i in range(len(bigImg1)):
            for j in range(len(bigImg1[0])):
                locX = startX + i
                locY = startY + j
                val = fig[i][j]
                overlay[locX][locY]= val


##        img2 = cv2.polylines(img2,[dst],True,255,9, cv2.LINE_AA)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        threshS = cv2.resize(overlay, (1500, 1000))
        cv2.imshow('image',threshS)
        cv2.waitKey(0)

        cv2.destroyAllWindows()


def combine(x, y):
    '''Takes a list of x coordinates and y coordinates and combines them
    into a list of [x,y] coordinates'''
    returnPoints = []
    for i in range(len(x)):
        returnPoints.append([x[i], y[i]])
    return returnPoints

def transformData(homography, coords, species, x,y):
    '''Takes as input a homography matrix,coordinates to be transformed
        and the species at those coordinates and returns a dictionary
        with the updated locations fo those species'''
    dataDict = {}
    updatedCoords = []
    for coord in coords:
        newCoord = (coord[0] + x*SCALE, coord[1] + x*SCALE)
        updateDcoords.append(newCoord)
    updatedCoords = np.int32(updatedCoords)
    for i in range(len(updatedCoords)):
        dataDict[updatedCoords[i]] = species[i]
    return dataDict

