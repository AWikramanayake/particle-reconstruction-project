import numpy as np

#import HitData

def findPos(hitNum, hitMatrix):

    """
    Given a 3xn matrix of pixel IDs of the form [x_ID, y_ID, z_pos], where z_pos is location in cm
    returns the position of the bottom left corner of the pixel.
    
    Here down is defined to be the negative y direction and left is defined to
    be the negative x direction.
    
    Here z position is the z coord along the line (0,0,z) and x/y pos is distance on the orthogonal plane.
    
    If a non-standard detector configuration is used (i.e., different to the one
    presented in the original problem statement), then this function will have
    to be modified to accomodate this.
    """
    
    return np.array([-10 + (hitMatrix[hitNum, 0])*0.01, 
                     -10 + (hitMatrix[hitNum, 1])*0.01, 
                     (hitMatrix[hitNum, 2])])



def findGrads(hitMatrix):

    """
    Calculates the four limiting gradients in the x direction and y direction from the first pixel
    to all other pixels in the particle ID matrix.
    """
    
    initialHit = findPos(0, hitMatrix)
    xShallowGrad = (findPos(1, hitMatrix)[0] - initialHit[0]) / (findPos(1, hitMatrix)[2] - initialHit[2])
    xTTGrad = xShallowGrad
    xBBGrad = xShallowGrad
    xBTGrad = ((findPos(1, hitMatrix)[0] + 0.01) - initialHit[0]) / (findPos(1, hitMatrix)[2] - initialHit[2])
    xTBGrad = (findPos(1, hitMatrix)[0] - (initialHit[0] + 0.01)) / (findPos(1, hitMatrix)[2] - initialHit[2])
    
    yShallowGrad = (findPos(1, hitMatrix)[1] - initialHit[1]) / (findPos(1, hitMatrix)[2] - initialHit[2])
    yTTGrad = yShallowGrad
    yBBGrad = yShallowGrad
    yBTGrad = ((findPos(1, hitMatrix)[1] + 0.01) - initialHit[1]) / (findPos(1, hitMatrix)[2] - initialHit[2])
    yTBGrad = (findPos(1, hitMatrix)[1] - (initialHit[1] + 0.01)) / (findPos(1, hitMatrix)[2] - initialHit[2])
    
    incr = 1
    
    for hit in hitMatrix[1:,:]:
    
        xShallowGrad = (findPos(incr, hitMatrix)[0] - initialHit[0]) / (findPos(incr, hitMatrix)[2] - initialHit[2])
        if xTTGrad > xShallowGrad:
            xTTGrad = xShallowGrad
        if xBBGrad < xShallowGrad:
            xBBGrad = xShallowGrad
        if xBTGrad > ((findPos(incr, hitMatrix)[0] + 0.01) - initialHit[0]) / (findPos(incr, hitMatrix)[2] - initialHit[2]):
            xBTGrad = ((findPos(incr, hitMatrix)[0] + 0.01) - initialHit[0]) / (findPos(incr, hitMatrix)[2] - initialHit[2])
        if xTBGrad < (findPos(incr, hitMatrix)[0] - (initialHit[0] + 0.01)) / (findPos(incr, hitMatrix)[2] - initialHit[2]):
            xTBGrad = (findPos(incr, hitMatrix)[0] - (initialHit[0] + 0.01)) / (findPos(incr, hitMatrix)[2] - initialHit[2])
            
        yShallowGrad = (findPos(incr, hitMatrix)[1] - initialHit[1]) / (findPos(incr, hitMatrix)[2] - initialHit[2])
        if yTTGrad > yShallowGrad:
            yTTGrad = yShallowGrad
        if yBBGrad < yShallowGrad:
            yBBGrad = yShallowGrad
        if yBTGrad > ((findPos(incr, hitMatrix)[1] + 0.01) - initialHit[1]) / (findPos(incr, hitMatrix)[2] - initialHit[2]):
            yBTGrad = ((findPos(incr, hitMatrix)[1] + 0.01) - initialHit[1]) / (findPos(incr, hitMatrix)[2] - initialHit[2])
        if yTBGrad < (findPos(incr, hitMatrix)[1] - (initialHit[1] + 0.01)) / (findPos(incr, hitMatrix)[2] - initialHit[2]):
            yTBGrad = (findPos(incr, hitMatrix)[1] - (initialHit[1] + 0.01)) / (findPos(incr, hitMatrix)[2] - initialHit[2])
        incr += 1
    
    return np.array([xTTGrad, xBBGrad, xBTGrad, xTBGrad, yTTGrad, yBBGrad, yBTGrad, yTBGrad]).reshape(2,4)
    


def reconstruct(hitMatrix):

    """
    Uses the four extremum gradients to estimate the highest point of impact on each subsequent pixel
    after the initial pixel.
    
    Returns a matrix with the midpoints of the possible hit ranges at each pixel, and the length of the range.
    Format: [x_mid_pos, x_range, y_mid_pos, y_range, z_pos].
    
    Here z position is the z coord along the line (0,0,z) and x/y pos is distance on the orthogonal plane.
    """
    
    recPoints = np.zeros(hitMatrix.shape[0]*5).reshape(hitMatrix.shape[0], 5)
    gradientArr = findGrads(hitMatrix)
    initialHit = findPos(0, hitMatrix)
    hitLoc = np.zeros(3)
    incr = 1
    bounds = np.zeros(4)
    recPoints[0] = ([(initialHit[0] + 0.005), 0, (initialHit[1] + 0.005), 0, initialHit[2]])
    
    for hit in hitMatrix[1:,:]:
        hitLoc = findPos(incr, hitMatrix)
        bounds[0] = (initialHit[0] + 0.01) + (gradientArr[0][0])*(hitLoc[2] - initialHit[2])
        bounds[1] = (initialHit[0] + 0.01) + (gradientArr[0][3])*(hitLoc[2] - initialHit[2])
        bounds[2] = initialHit[0] + (gradientArr[0][1])*(hitLoc[2] - initialHit[2])
        bounds[3] = initialHit[0] + (gradientArr[0][2])*(hitLoc[2] - initialHit[2])
    
        recPoints[incr][0:2] = ([(np.amax(bounds) + np.amin(bounds))/2,
                            abs(np.amax(bounds) - np.amin(bounds))])
        
        bounds[0] = (initialHit[1] + 0.01) + (gradientArr[1][0])*(hitLoc[2] - initialHit[2])
        bounds[1] = (initialHit[1] + 0.01) + (gradientArr[1][3])*(hitLoc[2] - initialHit[2])
        bounds[2] = initialHit[1] + (gradientArr[1][1])*(hitLoc[2] - initialHit[2])
        bounds[3] = initialHit[1] + (gradientArr[1][2])*(hitLoc[2] - initialHit[2])
        
        recPoints[incr][2:4] = ([(np.amax(bounds) + np.amin(bounds))/2,
                            abs(np.amax(bounds) - np.amin(bounds))])
        
        recPoints[incr][4] = hitLoc[2]
        
        incr += 1
        
    return recPoints
    
    
def bestFit(recData):
    
    """
    Input should be the matrix returned by the reconstruction function
    Performs linear regression to createe the reconstructed trajectory
    NOTE: the comments are shamelessly taken from the stackoverflow post from which
    the function was shamelessly ripped off.
    
    Output is a 6 component vector
    First 3 components are the x,y,z compponents of the direction vector of the reconstructed path
    Other 3 components are the x,y,z coordinates of a point along the reconstructed path (should be at z = 40cm detector)
    Together this info uniquely defines the reconstrcuted path
    """
    
    data = np.concatenate((recData[:,0][:, np.newaxis], 
                       recData[:,2][:, np.newaxis], 
                       recData[:,4][:, np.newaxis]), 
                      axis=1)


    # Calculate the mean of the points, i.e. the 'center' of the cloud
    datamean = data.mean(axis=0)

    # Do an SVD on the mean-centered data.
    uu, dd, vv = np.linalg.svd(data - datamean)

    # Now vv[0] contains the first principal component, i.e. the direction
    # vector of the 'best fit' line in the least squares sense.
    
    print("Reconstructed direction vector is:")
    print(vv[0])
    print("")
    print("passing through point:")
    print(datamean)

    return np.concatenate((vv[0], datamean))