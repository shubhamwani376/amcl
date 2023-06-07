#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

def normpos(pos):
    if (pos[2]!=0):
        pos = pos/pos[2] # to normalise homogeneous coordinate
    return(pos)

def linefrommap(map):
    map = map.flatten()
    line = np.cross(np.array([map[0],map[1],1]) , np.array([map[2],map[3],1])) # line from x1 y1 x2 y2 format
    return line

def within_range(ip, map):
    x1 = min(map[0],map[2])
    x2 = max(map[0],map[2])
    y1 = min(map[1],map[3])
    y2 = max(map[1],map[3])
    if y1 == y2:
        if (ip[0]>=x1 and ip[0]<=x2):
            return True
        else:
            return False
    elif x1 == x2:
        if (ip[1]>=y1 and ip[1] <= y2):
            return True
        else:
            return False
    else:
        if ((ip[0]>=x1 and ip[0]<=x2) and (ip[1]>=y1 and ip[1] <= y2)):
            return True
        else:
            return False

def lidar(map,pos,nlaserbeam, fig, ax):
    lidardata = np.zeros(nlaserbeam)
    print("In Lidar")
    for i in range(lidardata.shape[0]):
        line1 = np.array([np.tan(2*np.pi*i/nlaserbeam),-1,pos[1]-(pos[0]*np.tan(2*np.pi*i/nlaserbeam))])
        dist = []
        for j in range(map.shape[0]):
            line2 = linefrommap(map[j,:])
            ip = normpos(np.cross(line1,line2))
            if abs(np.arctan2((ip[1] - pos[1]) , (ip[0] - pos[0])) - (np.mod(2*np.pi*i/nlaserbeam, 2*np.pi) - np.pi)) < 1e-8:
                    if within_range(ip, map[j,:]):
                        dist.append(np.sqrt((pos[0] - ip[0])**2  + (pos[1] - ip[1])**2))
                    else:
                        dist.append(100)
            else:
                dist.append(100)
            # ax.scatter(ip[0],ip[1], c='red')
        lidardata[i] = min(dist)
        idx = dist.index(min(dist))
        line2 = linefrommap(map[idx,:])
        ip = normpos(np.cross(line1,line2))

        ax.plot([pos[0], ip[0]],[pos[1], ip[1]], c='red')
        ax.scatter(ip[0],ip[1], c='black')
    for i in range(map.shape[0]):
        ax.plot([map[i,0],map[i,2]],[map[i,1],map[i,3]], c='black') 
    ax.scatter(pos[0],pos[1])
    print("Out Lidar")
    return lidardata

def visualize(map,pos,nlaserbeam,lidardata):
    fig, ax = plt.subplots()
    
    for i in range(map.shape[0]):
        ax.plot([map[i,0],map[i,2]],[map[i,1],map[i,3]], c='black') # + lidardata[j]*np.sin(2*np.pi*j/nlaserbeam) #+ lidardata[j]*np.cos(2*np.pi*j/nlaserbeam)
    for j in range(lidardata.shape[0]):
        ax.plot([pos[0], pos[0] + lidardata[j]*np.cos(2*np.pi*j/nlaserbeam)],[pos[1], pos[1] + lidardata[j]*np.sin(2*np.pi*j/nlaserbeam)], c='red')
    ax.scatter(pos[0],pos[1])

def on_click(event):
    print(event.xdata,event.ydata)
    x = event.xdata
    y = event.ydata
    """if event.button is MouseButton.LEFT:
        print(f'data coords {event.xdata} {event.ydata},',
              f'pixel coords {event.x} {event.y}')
        #fig, ax = plt.subplots()
        if (event.xdata is not None and event.ydata is not None):
            pos = np.array([event.xdata,event.ydata,1], dtype=np.float64)
            lidar(map,pos,nlaserbeam,fig, ax)
        else:
            print("None")"""
    if ((x>=0 and x<=2) and (y>=0 and y<=1)):
        pos = np.array([x,y,1], dtype=np.float64)
        ax.clear()
        lidardata = lidar(map,pos,nlaserbeam,fig, ax)
        print(lidardata)
        plt.show()


def on_move(event):
    if event.button is MouseButton.RIGHT:
        print('disconnecting callback')
        plt.disconnect(binding_id)



if __name__ == '__main__':

    # Configuration variables
    nlaserbeam = 23
    nparticles = 50
    particles = np.zeros((50,3))
    nretention = 0.4

    # Map defined as lines in x1,y1,x2,y2 format
    map = np.array([[0,0,0,1],
                    [0,1,2,1],
                    [0,0,2,0],
                    [2,1,2,0],
                    [0,0.75,0.75,0.75],
                    [0.75,0.25,1.5,1.0],
                    [1.5,0.5,2,0]])
    
    pos = np.array([0.25,0.4,1])
    fig, ax = plt.subplots()
    lidar(map,pos,nlaserbeam,fig, ax)

    #binding_id = plt.connect('button_press_event', on_move)
    #plt.connect('button_press_event', on_click)
    binding_id = plt.connect('motion_notify_event', on_click)
    plt.show()