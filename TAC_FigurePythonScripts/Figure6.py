# Script for plotting Fig 6.
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
verbose = False


max_it = 50
num_ave = 100
BFS_counter = np.zeros(max_it-1)
BFS_kstars = [0 for k in range(2,max_it+1)]
DFS_kstars = [0 for k in range(2,max_it+1)]
greed = [0 for k in range(2,max_it+1)]
for its in range(2,max_it+1):
	# Generate a problem with m agents and n tasks.
	m= its
	n= its
	
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
		agents = [Agent(i,C[i]) for i in range(m)] #DFS
		agents2 = [AgentBFS(i,C[i]) for i in range(m)] # BFS
		agentsCBAA = [AgentCBAA(i,1./C[i]) for i in range(m)] #Greedy
		
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
				greed[its-2] = greed[its-2] + j
				break
		
		qqq=0
		for j in range(m):
			if 1 in agentsCBAA[j].x_i:
				#print(agents[j].costs[agentsCBAA[j].x_i.index(1)])
				qqq = np.max([agents[j].costs[agentsCBAA[j].x_i.index(1)],qqq])
		
		counter = 0
		while agents[0].matching_exists:
			newmax = sb.arg_max(adj,agents,D)
			if newmax<qqq:
				break
			counter = sb.aug_path(adj,agents,D)
			DFS_kstars[its-2] = DFS_kstars[its-2] + counter + 1
			
		
		counter = 0
		while agents2[0].matching_exists:
			newmax = sb.arg_max(adj,agents2,D)
			if newmax<qqq:
				break
			counter = sb.aug_path(adj,agents2,D)
			BFS_kstars[its-2] = BFS_kstars[its-2] + counter + 1
			
			
		print(its,aves)	
plt.rc('text',usetex=True)
plt.rc('font',family='serif')
plt.figure(figsize=(15,5))
plt.xlabel(r'Number of tasks, n',fontsize=18)
plt.ylabel(r'Average time steps',fontsize=18)
plt.plot([i for i in range(2,max_it+1)],np.divide(DFS_kstars,num_ave),'b.',label="AugDFS()")
plt.plot([i for i in range(2,max_it+1)],np.divide(BFS_kstars,num_ave),'rx',label="AugBFS()")
plt.plot([i for i in range(2,max_it+1)],np.divide(greed,num_ave),'k*',label="Greedy")
plt.xticks(np.arange(2,max_it+2,2))
plt.xlim(2,max_it)
plt.legend(loc='upper left', prop={'size':14})
plt.show()



