# Script for generating cost matrices
# Code written by Mitchell Khoo, PhD student at The University of Melbourne.

# Based on paper submitted to CDC:
# "Distributed Algorithm for Solving the Bottleneck Assignment Problem",
# Mitchell Khoo, Tony A. Wood, Chris Manzie, Iman Shames.

import numpy as np
import math

# Generate agent and task locations and the corresponding cost matrix.
def cost(m1,m2,n1,n2,cluster=1):
    row = m1+m2
    col = n1+n2
    agent_pos, task_pos = mk_loc(m1,m2,n1,n2,cluster)
    C = np.zeros((row,col))
    for i in range(row):
        for j in range(col):
            rel_pos = agent_pos[i]-task_pos[j]
            C[i,j] = math.sqrt( (agent_pos[i][0]-task_pos[j][0])**2 + (agent_pos[i][1]-task_pos[j][1])**2 )
    
    if cluster == 3:
        C=C*2
        for i in range(col):
            if C[i,col-i-1]>=100:
                C[i,col-i-1] = C[i,col-i-1]/2
        C = np.multiply(C<100,C)+np.multiply(C>=100,200.0)
        
    # print(agent_pos,"\n",agent_pos[0])
    # print(task_pos,"\n",task_pos[0])
    # print(C)
    
    
    return C, agent_pos, task_pos
    
def mk_loc(m1,m2,n1,n2,cluster=1):
    agent_pos = []
    task_pos = []
    if cluster==1:
        std = 10.0
        #Cluster 1
        for i in range(m1):
            # mean, std, vector shape
            pos = np.random.multivariate_normal([40.0,60.0], [[std,0.0],[0.0,std]])
            np.reshape(pos,(2,1))
            agent_pos.append(pos)
        for i in range(n1):
            # mean, std, vector shape
            pos = np.random.multivariate_normal([40.0,60.0], [[std,0.0],[0.0,std]])
            np.reshape(pos,(2,1))
            task_pos.append(pos)
            
        #Cluster 2
        for i in range(m2):
            # mean, std, vector shape
            pos = np.random.multivariate_normal([60.0,40.0], [[std,0.0],[0.0,std]])
            np.reshape(pos,(2,1))
            agent_pos.append(pos)
        for i in range(n2):
            # mean, std, vector shape
            pos = np.random.multivariate_normal([60.0,40.0], [[std,0.0],[0.0,std]])
            np.reshape(pos,(2,1))
            task_pos.append(pos)
            
    elif cluster==2:
        #Create position vectors in the positive quadrant
        limits = 100.0
        for i in range(m1+m2):
            pos = np.random.uniform(0.0, limits, (2,1))
            agent_pos.append(pos)
        for i in range(n1+n2):
            pos = np.random.uniform(0.0, limits, (2,1))
            task_pos.append(pos)
    elif cluster==3:
        #Create position vectors in the positive quadrant
        limits = 100.0
        for i in range(m1+m2):
            pos = np.random.uniform(0.0, limits, (2,1))
            agent_pos.append(pos)
        for i in range(n1+n2):
            pos = np.random.uniform(0.0, limits, (2,1))
            task_pos.append(pos)
    else:
        for i in range(m1):
            pos = np.random.uniform([5.0, 5.0],[40, 40])
            np.reshape(pos,(2,1))
            agent_pos.append(pos)
        for i in range(n1):
            pos = np.random.uniform([5.0,5], [40,40.0])
            np.reshape(pos,(2,1))
            task_pos.append(pos)
            
        #Cluster 2
        for i in range(m2):
            pos = np.random.uniform([60.0, 60.0],[95, 95])
            np.reshape(pos,(2,1))
            agent_pos.append(pos)
        for i in range(n2):
            pos = np.random.uniform([60.0,60], [95,95.0])
            np.reshape(pos,(2,1))
            task_pos.append(pos)
    return agent_pos, task_pos
