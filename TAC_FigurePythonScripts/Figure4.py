# Script for plotting Fig 4.
# Code written by Mitchell Khoo, PhD student at The University of Melbourne.

# Based on paper submitted to CDC:
# "Distributed Algorithm for Solving the Bottleneck Assignment Problem",
# Mitchell Khoo, Tony A. Wood, Chris Manzie, Iman Shames.

# THIS SCRIPT IS DIFFERENT TO OTHER FIGURE GENERATION SCRIPTS.
# MUST CHANGE subroutines.py AND agentBAP2.py TO OUTPUT len(self.receivedLists)
# THIS IS THE EASIEST WAY TO GRAB NUMBER OF EXPLORED AGENTS.

import numpy as np
import math
import networkx as nx
import matplotlib.pyplot as plt
from agentBAP1 import Agent
from agentBAP2 import AgentBFS
import subroutines as sb
import gen_cost as gc
import statistics

# Toggle display/hide cost matrix and assignment
verbose = False


max_it = 50
num_ave = 100
BFS_biggest = np.zeros(max_it-1)
BFS_all = np.zeros(max_it-1)
DFS = np.ones(max_it-1)
for its in range(2,max_it+1):
	# Generate a problem with m agents and n tasks.
	m= its
	n= its
	
	allall_sizes = []
	for aves in range(num_ave):
		#Cost calculated from distances, all in postitive quadrant
		cluster = 2 #1: normal distribution, 2: uniform distribution, 3: sparse uniform distribution
		C, agent_pos, task_pos = gc.cost(math.floor(m/2),math.ceil(m/2),math.floor(n/2),math.ceil(n/2),cluster)

		if verbose:
			print("Cost matrix\n", C)
			# print("Agent positions\n", agent_pos)
			# print("Task positions\n", task_pos)
			
		# Generate communication graph.
		G=nx.complete_graph(m)
		adj = nx.adjacency_matrix(G).toarray()
		D = 1

		# Generate agent instances
		agents2 = [AgentBFS(i,C[i]) for i in range(m)] # BFS
		
		all_sizes = []
		biggest = 0
		while agents2[0].matching_exists:
			sb.arg_max(adj,agents2,D)
			a,sizes = sb.aug_path(adj,agents2,D) #MUST CHANGE subroutines to output sizes
			
			all_sizes.extend(sizes)
			#print(sizes,statistics.mean(all_sizes),max(all_sizes))
		biggest = max(all_sizes)
		BFS_biggest[its-2] = BFS_biggest[its-2] + biggest
		print(its,aves)
		allall_sizes.extend(all_sizes)
	BFS_all[its-2] = statistics.mean(allall_sizes)		

scale = 2
plt.figure(figsize=(15,5))
plt.rc('text',usetex=True)
plt.rc('font',family='serif')
plt.xlabel("Number of tasks, n",fontsize=18)
plt.ylabel("Number of explored agents per D",fontsize=18)
plt.plot([i for i in range(2,max_it+1)],DFS,'b.',label="AugDFS()")
plt.plot([i for i in range(2,max_it+1)],BFS_biggest/num_ave,'rv',label="AugBFS() Maximum")
plt.plot([i for i in range(2,max_it+1)],BFS_all,'r*',label="AugBFS() Mean")
np.save('message_biggest.npy', np.array(BFS_biggest))
np.save('message_all.npy', np.array(BFS_all))
plt.xticks(np.arange(0,len(BFS_biggest)+scale,scale))
# plt.yscale('log')
plt.xlim(2,len(BFS_biggest)+1)
plt.legend(loc='upper left', prop={'size':14})
plt.show()