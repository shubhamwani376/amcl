#will take inputs from user and drive vehicle
# Vehicle Dynamics and Noise in Odometry

#!/usr/bin/python

import matplotlib as plt
import numpy as np

if __name__ == '__main__':

    # Configuration variables

    nlaserbeam = np.array([12])
    nparticles = np.array([50])
    nretention = np.array([0.4])


    # Map defined as lines in x1,y1,x2,y2 format
    map = np.array([[0,0,0,1],
                    [0,1,2,1],
                    [0,0,2,0],
                    [2,0,2,1],
                    [0,0.75,0.75,0.75],
                    [0.75,0.25,1.5,1],
                    [1.5,0.5,2,0]])
    print(map[0:1,:])

    