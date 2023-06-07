#!/usr/bin/python

import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

import amcl
import lidar

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
        lidar.lidar(map,pos,nlaserbeam,fig, ax,r1)
        plt.show()

def on_move(event):

    if event.key=="d":
        r1.move_fwd()
        particles[:,1] = particles[:,1] + 0.05
    elif event.key=="c":
        r1.move_back()
        particles[:,1] = particles[:,1] - 0.05
    elif event.key=="x":
        r1.move_left()
        particles[:,0] = particles[:,0] - 0.05
    elif event.key=="v":
        r1.move_right()
        particles[:,0] = particles[:,0] + 0.05
    
    """if event.key=="d":
        r1y = r1y + 0.1
        print("key d")
    elif event.key=="x":
        r1x = r1x - 0.1
        print("key d")
    elif event.key=="v":
        r1x = r1x + 0.1
        print("key d")
    elif event.key=="c":d
        r1y = r1y - 0.1
        print("key d")"""

    pos = np.array([r1.x,r1.y,1], dtype=np.float64)
    ax.clear()
    lidardata = lidar.lidar(map,pos,nlaserbeam,fig,ax,r1,viz)
    plt.show()

    lidardatapart = np.ones((nparticles,nlaserbeam))*5
    for k in range(particles.shape[0]):
        if (particles[k,0] > 0 and particles[k,0] < 2 and particles[k,1] > 0 and particles[k,1] < 1):
            pos1 = np.array([particles[k,0],particles[k,1],1])
            lidardatapart[k,:] = lidar.lidar(map,pos1,nlaserbeam,fig,ax,r1,False)
    print(lidardatapart)
    

class robot():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_fwd(self):
        if((self.x > 0 and self.x < 2) and (self.y > 0 and self.y < 1)):
            self.y = self.y + 0.05
            return self.y
            
    def move_back(self):
        if((self.x > 0 and self.x < 2) and (self.y > 0 and self.y < 1)):
            self.y = self.y - 0.05
            return self.y
    def move_right(self): 
        if((self.x > 0 and self.x < 2) and (self.y > 0 and self.y < 1)):
            self.x = self.x + 0.05
            return self.x
    def move_left(self):
        if((self.x > 0 and self.x < 2) and (self.y > 0 and self.y < 1)):
            self.x = self.x - 0.05
            return self.x

if __name__ == '__main__':

    # Configuration variables
    nlaserbeam = 11
    nparticles = 30
    particles = np.zeros((nparticles,2))
    nretention = 0.4
    
    # Map defined as lines in x1,y1,x2,y2 format
    map = np.array([[0,0,0,1],
                    [0,1,2,1],
                    [0,0,2,0],
                    [2,1,2,0],
                    [0,0.75,0.75,0.75],
                    [0.75,0.25,1.5,1.0],
                    [1.5,0.5,2,0]])
    
    fig, ax = plt.subplots()

    low = np.array([0,0])
    high = np.array([2,1])
    particles = amcl.particle_samples(nparticles,low, high)
    amcl.plot_particle_samples(particles, fig, ax, size=1.0, axis=True)

    r1 = robot(0.15,0.4)
    pos = np.array([r1.x,r1.y,1])

    viz = True

    lidardata = lidar.lidar(map,pos,nlaserbeam,fig,ax,r1,viz)
    #print(lidardata)

    #binding_id = plt.connect('button_press_event', on_move)
    #plt.connect('button_press_event', on_click)
    binding_id = plt.connect('key_press_event', on_move)
    plt.show()