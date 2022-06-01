#Script for Fig 5.
# Code written by Mitchell Khoo, PhD student at The University of Melbourne.

# Based on paper submitted to CDC:
# "Distributed Algorithm for Solving the Bottleneck Assignment Problem",
# Mitchell Khoo, Tony A. Wood, Chris Manzie, Iman Shames.


import numpy as np
import math
import networkx as nx
import matplotlib.pyplot as plt
from agentBAP1 import Agent
from agentBAP2 import AgentBFS
import subroutines as sb
import gen_cost as gc

from agentCBAA import AgentCBAA

# Toggle display/hide cost matrix and assignment
verbose = True


# Generate a problem with m agents and n tasks.
m= 50
n= 50
# maxCost = 50
# C = np.random.randint(1, maxCost+1, size=(m,n)) #Cost matrix
#Cost calculated from distances, all in postitive quadrant
cluster = 2 #1: normal distribution, 2: uniform distribution, 3: sparse uniform distribution
C, agent_pos, task_pos = gc.cost(math.floor(m/2),math.ceil(m/2),math.floor(n/2),math.ceil(n/2),cluster)

if verbose:
	print("Cost matrix\n", C)
	# print("Agent positions\n", agent_pos)
	# print("Task positions\n", task_pos)
	
# Generate communication graph. Here communication between agents is a cycle
# graph with diameter D.
# G=nx.cycle_graph(m)
# adj = nx.adjacency_matrix(G).toarray()
# D = math.ceil((m-1)/2)
G=nx.complete_graph(m)
adj = nx.adjacency_matrix(G).toarray()
D = 1

# Generate agent instances
agents = [Agent(i,C[i]) for i in range(m)]
agents2 = [AgentBFS(i,C[i]) for i in range(m)]
agentsCBAA = [AgentCBAA(i,1./C[i]) for i in range(m)]

greed = 0
for j in range(D*n):
	for i in range(len(agentsCBAA)):
		agentsCBAA[i].selectTask()
	sb.communicate(adj,agentsCBAA)
	for i in range(len(agentsCBAA)):
		agentsCBAA[i].consensus()
	sum_vec = np.add(agentsCBAA[0].x_i,agentsCBAA[1].x_i)
	for i in range(2,len(agentsCBAA)):
		sum_vec = np.add(sum_vec,agentsCBAA[i].x_i)
	if np.max(sum_vec)==1 and np.min(sum_vec)==1:
		greed = j
		break
qqq=0
for j in range(m):
	if 1 in agentsCBAA[j].x_i:
		#print(agents[j].costs[agentsCBAA[j].x_i.index(1)])
		qqq = np.max([agents[j].costs[agentsCBAA[j].x_i.index(1)],qqq])
print(qqq)

DFS_cost = []
BFS_cost = []
BFS_time = [0]
DFS_time = [0]
counter = 0
# Begin distributed algorithm
# Agent 0 was used here, but ALL agents know if a matching exists or not.
while agents[0].matching_exists:
	max = sb.arg_max(adj,agents,D)
	counter = sb.aug_path(adj,agents,D)
	DFS_time.append(counter + 1)
	DFS_cost.append(max)
DFS_cost.append(max)


if verbose:
	print("\nAllocations made by distBAP:")
	print("Agent //","Allocated Task //","Cost")
	fmt = '{:<8} {:<17} {:<4}'
	for j in range(m):
		if agents[j].matchedTo!=-1:
			print(fmt.format(j, math.floor(agents[j].matchedTo), C[j][math.floor(agents[j].matchedTo)]))
		else:
			print(fmt.format(j, "Unmatched",""))

print("\n-------------------------------")

counter = 0
while agents2[0].matching_exists:
	max = sb.arg_max(adj,agents2,D)
	counter = sb.aug_path(adj,agents2,D)
	BFS_time.append(counter + 1)
	BFS_cost.append(max)
BFS_cost.append(max)

if verbose:
	print("\nAllocations made by new method:")
	print("Agent //","Allocated Task //","Cost")
	fmt = '{:<8} {:<17} {:<4}'
	for j in range(m):
		if agents2[j].matchedTo!=-1:
			print(fmt.format(j, math.floor(agents2[j].matchedTo), C[j][math.floor(agents2[j].matchedTo)]))
		else:		
			print(fmt.format(j, "Unmatched",""))
			

limit = np.sum(DFS_time)
plt.figure(figsize=(15,5))
plt.rc('text',usetex=True)
plt.rc('font',family='serif')
plt.xlabel("Number of time steps",fontsize=18)
plt.ylabel("Weight of largest edge",fontsize=18)
plt.plot(np.cumsum(DFS_time),DFS_cost,'b.',label="AugDFS()")
plt.plot(np.cumsum(BFS_time),BFS_cost,'rx',label="AugBFS()")
plt.plot([k for k in range(limit)],[qqq for i in range(limit)],'k')
plt.plot(greed,qqq,'k*',label="CBAA")
plt.xlim(0,limit)
#plt.xticks(np.arange(0,limit+2,10))
plt.legend(loc='upper right', prop={'size':14})
plt.show()