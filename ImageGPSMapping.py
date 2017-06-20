"""
Details for quadrilateral -> rectangle mapping can be found @ the following link:
https://www.particleincell.com/2012/quad-interpolation/
"""
from numpy import matrix, sqrt, cross, sign, append, reshape


"""
Calculating the mapping coeff vectors a, b given the bounding box of an image

@param imageCornerGps: a list of Gps coordinates describing the quadrilateral of
image of interest.
@param imgWidth: width of the image in pixels. Default is set as 4000 for the 
original images.
@param imgHeight: height of the image in pixels. Default is set as 3000 for the 
original images.
@returns: the coeff vectors a, b as described above.
"""
def imageToGpsCoeff(imageCornerGps, imgWidth=4000, imgHeight=3000):
    """
    From original space to stitched space: (l, m) -> (x, y)
    The vectors a, b in the method is corresponding to a_1~4, b_1~4 as follows: 
    x = a_1 + a_2*l + a_3*m + a_4*m*l
    y = b_1 + b_2*l + b_3*m + b_4*m*l
    Let x = A * a, then we have a = A^(-1) * x
    Similarly, b = A^(-1) * y
    """
    cornerGps = imageCornerGps[:4]
    A = matrix([[1, 0, 0, 0], 
                [1, imgWidth, 0, 0],
                [1, imgWidth, imgHeight, imgWidth * imgHeight],
                [1, 0, imgHeight, 0]])
    AI = A.getI()
    
    px = matrix([i[0] for i in cornerGps])
    py = matrix([i[1] for i in cornerGps])  
    
    a = AI * px.getH()
    b = AI * py.getH()
    return a, b


"""
Mapping from image space to world space (GPS coordinates)

@param l: the horizontal coordinates from the image space
@param m: the vertical coordinates from the image space
@param a: the mapping coeff vector a from this specific image
@param b: the mapping coeff vector b from this specific image
@returns: the longitude and latitude of the point in the world view
"""
def imageToGpsCoord(l, m, a, b):
    AB = append(a.tolist(), b.tolist())
    AB = matrix(reshape(AB, (2, 4)))
    xy = AB * matrix([[1], [l], [m], [m*l]])
    return xy.item(0), xy.item(1)

    
"""
Mapping from world space (GPS coordinates) to image space

@param x: the longitude of the point of interest
@param y: the latitude of the point of interest
@param a: the mapping coeff vector a from this specific image
@param b: the mapping coeff vector b from this specific image
@returns: a pair of integers indicating the coordinates in the image space
""" 
def gpsToImageCoord(x, y, a, b):
    a = [item for sublist in a.tolist() for item in sublist]
    b = [item for sublist in b.tolist() for item in sublist]

    aa = a[3]*b[2] - a[2]*b[3];
    bb = a[3]*b[0] -a[0]*b[3] + a[1]*b[2] - a[2]*b[1] + x*b[3] - y*a[3];
    cc = a[1]*b[0] -a[0]*b[1] + x*b[1] - y*a[1];
 
    det = sqrt(bb*bb - 4*aa*cc);
    if (aa == 0.0):
        m = -cc/bb
    else:
        m = (-bb-det)/(2*aa);
    l = (x-a[0]-a[2]*m)/(a[1]+a[3]*m);
    return int(round(l)), int(round(m))


"""
Checks if a point (in GPS coords) is in a specific image

Due to the fact that the quadrilateral that describes each individual image
comes from a projection of the drone's camera window, we can assume that the
quadrilateral is always convex, and thus use the generalized triangle test.

@param imageCornerGps: a list of Gps coordinates describing the quadrilateral of
image of interest.
@param x: the longitude of the point of interest
@param y: the latitude of the point of interest
@return: a boolean indicating if the point is in the image
"""
def isInImage(imageCornerGps, x, y):
    crossDir = []
    for i in xrange(4):
        a = matrix(imageCornerGps[i][:2]) - matrix([x, y])
        b = matrix(imageCornerGps[i + 1][:2]) - matrix([x, y])
        crossProd = sign(cross(a, b))
        if crossProd == 0:
            continue
        elif crossDir == []:
            crossDir = crossProd
        else:
            if crossDir != crossProd:
                return False   
    return True

"""
Some random tests
"""
#sampleOriginalCoords = [[1, 0, 0], [2, 1, 0], [1, 2, 0], [0, 1, 0], [1, 0, 0]]
#a, b = imageToGpsCoeff(sampleOriginalCoords)
##sampleOriginalCoords = [[-117.7098247246, 34.1080103159, 402.999125], [-117.7097208338, 34.1080050844, 402.172537], [-117.7097231547, 34.1079251828, 401.102699], [-117.7098466889, 34.1079487191, 401.799658], [-117.7098247246, 34.1080103159, 402.999125]]
##getSourceToStitchCoeff(sampleOriginalCoords)
#print gpsToImageCoord(sampleOriginalCoords, 1, 1, a, b)
#
#print isInImage(sampleOriginalCoords, 1, 2)
##getSourceImages('footprints.kml')
