# Script for running plotting Fig 3.
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

# Toggle display/hide cost matrix and assignment
verbose = False


max_it = 50
num_ave = 100
BFS_counter = np.zeros(max_it-1)
DFS_counter = np.zeros(max_it-1)
for its in range(2,max_it+1):
	# Generate a problem with m agents and n tasks.
	m= its
	n= its
	
	for aves in range(num_ave):
		#Cost calculated from distances, all in postitive quadrant
		cluster = 3 #1: normal distribution, 2: uniform distribution, 3: sparse uniform distribution
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
		agents = [Agent(i,C[i]) for i in range(m)]
		agents2 = [AgentBFS(i,C[i]) for i in range(m)] # BFS

		
		while agents[0].matching_exists:
			sb.arg_max(adj,agents,D)
			DFS_counter[its-2] = DFS_counter[its-2] + sb.aug_path(adj,agents,D) + 1

		while agents2[0].matching_exists:
			sb.arg_max(adj,agents2,D)
			BFS_counter[its-2] = BFS_counter[its-2] + sb.aug_path(adj,agents2,D) + 1
		
		print(its,aves)
			

scale = 2
plt.figure(figsize=(15,5))
plt.rc('text',usetex=True)
plt.rc('font',family='serif')
plt.xlabel("Number of tasks, n",fontsize=18)
plt.ylabel("Average time steps",fontsize=18)
plt.plot([i for i in range(2,max_it+1)],DFS_counter/num_ave,'b.',label="AugDFS()")
plt.plot([i for i in range(2,max_it+1)],BFS_counter/num_ave,'rx',label="AugBFS()")
np.save('timevsn_DFS_sparse.npy', np.array(DFS_counter))
np.save('timevsn_BFS_sparse.npy', np.array(BFS_counter))
plt.xticks(np.arange(0,len(BFS_counter)+scale,scale))
# plt.yscale('log')
plt.xlim(2,len(BFS_counter)+1)
plt.legend(loc='upper left', prop={'size':14})
plt.show()