#Line algorithm, Noise model,

import numpy as np
import matplotlib.pyplot as plt

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

def lidar(map,pos,nlaserbeam, fig,ax,r1,viz):
    lidardata = np.zeros(nlaserbeam)
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
                        dist.append(5)
            else:
                dist.append(5)
            # ax.scatter(ip[0],ip[1], c='red')
        lidardata[i] = min(dist)
        idx = dist.index(min(dist))
        line2 = linefrommap(map[idx,:])
        ip = normpos(np.cross(line1,line2))
        if viz:
            ax.plot([pos[0], ip[0]],[pos[1], ip[1]], c='red')
            ax.scatter(ip[0],ip[1], c='black')
            for i in range(map.shape[0]):
                ax.plot([map[i,0],map[i,2]],[map[i,1],map[i,3]], c='black') 
            ax.scatter(pos[0],pos[1])
    #print(lidardata)
    return lidardata