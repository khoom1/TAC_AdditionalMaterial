# Subroutines of PruneBAP
# Code written by Mitchell Khoo, PhD student at The University of Melbourne.

# Based on paper submitted to CDC:
# "Distributed Algorithm for Solving the Bottleneck Assignment Problem",
# Mitchell Khoo, Tony A. Wood, Chris Manzie, Iman Shames.

import numpy as np

# Max consensus algorithm.
def arg_max(adj,agents,D):
	# Each agent find its local candidate edge.
	for i in range(len(agents)):
		agents[i].find_local_candidate()
	# Agents compare their local candidate edges with other agents.
	for i in range(D):
		communicate(adj,agents)
		for j in range(len(agents)):
			agents[j].find_global_candidate()
	max = agents[0].out_message[0]
	return max

# Finding an augmenting path as described in CDC paper.
def aug_path(adj,agents,D):
	counter = 0
	for i in range(len(agents)):
		agents[i].removeEdge() # See Remark 4 of CDC paper
		agents[i].distributed_aug_init()
	# All agents have variable search_complete, all having the same value here.
	while not(agents[0].search_complete):
		counter = counter + 1
		for i in range(len(agents)):
			agents[i].local_choose_agent_to_explore()
			
		for i in range(D):
			communicate(adj,agents)
			for j in range(len(agents)):
				agents[j].converge_agent_to_explore()
			
		for i in range(len(agents)):
			agents[i].distributed_aug_status() #To run Figure4, MUST GRAB len(self.receivedLists) from this line
		
		# Depending on the status of the search, agents must decide how to proceed.
		# for i in range(D):
			# communicate(adj,agents)
			# for j in range(len(agents)):
				# agents[j].distributed_aug_converge()
	return counter

# Finding an augmenting path via an alternative method.
# We are still in the process of documenting this.
# def aug_path2(adj,agents,D):
	# counter = aug_path(adj,agents,D)

	# If search was successful, multiple free agents might be available.
	# if agents[0].matching_exists:
		# for i in range(D):
			# communicate(adj,agents)
			##Pick one free agent.
			# for j in range(len(agents)):
				# agents[j].find_global_candidate()
		## Update the new matching based on the augmenting path that was found.
		# for i in range(len(agents)):
			# agents[i].distributed_aug_converge()
	# return counter
	

def communicate(adj,agents):
	# Collect all outgoing messages from agents
	y = [agents[i].get_outgoing_message() for i in range(len(agents))]
	
	# Each agent receives the outgoing messages from its neighbours
	for i in range(len(agents)):
		neighbours_i = np.where(adj[i])[0]
		for j in range(len(neighbours_i)):
			agents[i].receive(y[neighbours_i[j]])


