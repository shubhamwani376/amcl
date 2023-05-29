#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

def normpos(pos):
    if (pos[2]!=0):
        pos = pos/pos[2] # to normalise homogeneous coordinate
    return(pos)

def linefrommap(map):
    map = map.flatten()
    #line = np.array([map[1]-map[3],map[2]-map[0],map[0]*map[3]-map[1]*map[2]]) # line from x1 y1 x2 y2 format
    line = np.cross(np.array([map[0],map[1],1]) , np.array([map[2],map[3],1])) # line from x1 y1 x2 y2 format
    return line

def lidar(map,pos,nlaserbeam):
    lidardata = np.zeros(nlaserbeam)
    fig, ax = plt.subplots()
    for i in range(lidardata.shape[0]):
        line1 = np.array([np.tan(2*np.pi*i/nlaserbeam),-1,pos[1]-(pos[0]*np.tan(2*np.pi*i/nlaserbeam))])
        #inter = np.zeros((map.shape[0],3))
        dist = []
        for j in range(map.shape[0]):
            line2 = linefrommap(map[j,:])
            ip= normpos(np.cross(line1,line2))
            # mask to check if it lies on line
            if ((ip[0]>=map[j,0] and ip[0]<=map[j,2]) and (ip[1]>=map[j,1] and ip[1]<=map[j,3])):
                # dist.append(np.linalg.norm(pos[0:2] - ip[0:2]))
                dist.append(np.sqrt((pos[0] - ip[0])**2  + (pos[1] - ip[1])**2))
                ax.scatter(ip[0],ip[1], c='red')
        lidardata[i] = min(dist)
        print(dist)
        print(min(dist))
    for i in range(map.shape[0]):
        ax.plot([map[i,0],map[i,2]],[map[i,1],map[i,3]], c='black') 
    ax.scatter(pos[0],pos[1])
    plt.show()
    return lidardata

def visualize(map,pos,nlaserbeam,lidardata):
    fig, ax = plt.subplots()
    
    for i in range(map.shape[0]):
        ax.plot([map[i,0],map[i,2]],[map[i,1],map[i,3]], c='black') # + lidardata[j]*np.sin(2*np.pi*j/nlaserbeam) #+ lidardata[j]*np.cos(2*np.pi*j/nlaserbeam)
    for j in range(lidardata.shape[0]):
        ax.plot([pos[0], pos[0] + lidardata[j]*np.cos(2*np.pi*j/nlaserbeam)],[pos[1], pos[1] + lidardata[j]*np.sin(2*np.pi*j/nlaserbeam)], c='red')
    ax.scatter(pos[0],pos[1])
    plt.show()

if __name__ == '__main__':

    # Configuration variables

    nlaserbeam = 18
    nparticles = 50
    particles = np.zeros((50,3))
    nretention = 0.4


    # Map defined as lines in x1,y1,x2,y2 format
    map = np.array([[0,0,0,1],
                    [0,1,2,1],
                    [0,0,2,0],
                    [2,1,2,0],
                    [0,0.75,0.75,0.75],
                    [0.75,0.25,1.5,1],
                    [1.5,0.5,2,0]])
    
    pos = np.array([1.75,0.5,1])
    a = lidar(map,pos,nlaserbeam)
    # print(a)
    # visualize(map,pos,nlaserbeam,a)