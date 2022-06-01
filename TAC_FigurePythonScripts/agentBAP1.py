# Agent class showing behaviour of individual agents.
# Code written by Mitchell Khoo, PhD student at The University of Melbourne.

# Based on paper submitted to CDC:
# "Distributed Algorithm for Solving the Bottleneck Assignment Problem",
# Mitchell Khoo, Tony A. Wood, Chris Manzie, Iman Shames.

import numpy as np
import math
class Agent:

	def __init__(self, id, costs):
		self.id = id
		self.costs = costs #Local cost vector.
		self.assig = [x for x in range(len(costs))] # Local assignment vector.
		self.stack = []
		
		# Start with matching as main diagonal of assignment matrix.
		if id<len(costs):
			self.matchedTo = id
		else:
			self.matchedTo = -1
			
		self.matching_exists = True
		
	# The message this agent will send to its neighbours.
	def get_outgoing_message(self):
		return self.out_message
	
	# Collect the messages received from neighbours.
	def receive(self,y_k):
		self.receivedLists = np.append(self.receivedLists,[y_k],axis=0)
	
	
	# Choose local candidate edge for removal. Here it is the edge this agent is
	# matched to. See Remark 4 of CDC paper.
	def find_local_candidate(self):
		L_i = -1.0
		J_i = -1.0
		I_i = -1.0
		if len(self.assig) != 0 and self.matchedTo!=-1:
			L_i = self.costs[math.floor(self.matchedTo)]
			J_i = self.matchedTo
			I_i = self.id
		self.out_message = [L_i,J_i,I_i]
		self.receivedLists = [self.out_message]
	
	# Converge to consensus on edge for removal. Here it is the largest edge in
	# the matching.
	def find_global_candidate(self):
		Lmax = self.receivedLists[0][0]
		K = self.receivedLists[0][2]
		temp = 0
		for i in range(1,len(self.receivedLists)):
			if Lmax < self.receivedLists[i][0]:
				Lmax = self.receivedLists[i][0]
				K = self.receivedLists[i][2]
				temp = i
			elif Lmax == self.receivedLists[i][0]:
				if K>self.receivedLists[i][2]:
					K = self.receivedLists[i][2]
					temp = i
		
		self.out_message = self.receivedLists[temp]	
		self.receivedLists = [self.out_message]
	
	# Remove all edges incident to this agent that are larger than or equal to 
	# the candidate edge. See Remark 4 of CDC paper.
	def removeEdge(self):
		for i in range(len(self.assig)-1,-1,-1):
			if self.assig[i]!=self.matchedTo:
				if self.costs[self.assig[i]]>= self.out_message[0]:
					self.assig.remove(self.assig[i])
		self.ibar = self.out_message[2]
		if self.out_message[2] == self.id:
			self.assig.remove(self.out_message[1])
			self.matchedTo = -1

################################################################################
	#Functions for Depth-first Search

	# Begin search for augmenting path.
	def distributed_aug_init(self):
		self.f_i = False
		self.newMatch = self.matchedTo
		self.search_complete = False
		self.root = self.out_message[1]
		self.stack = [self.root]
	
	# Unexplored agents determine if they have an edge to the current task in the
	# search.
	def local_choose_agent_to_explore(self):
		t = math.floor(self.stack[-1])
		if self.f_i == False and (t in self.assig):
			L_i = self.costs[t]
		else:
			L_i = 1000 # Big M notation.
		J_i = self.matchedTo
		I_i = self.id
		
		self.out_message = [L_i,J_i,I_i]
		self.receivedLists = [self.out_message]
	
	# Agents reach consensus on which agent is the next to be explored.
	def converge_agent_to_explore(self):
		Lmin = self.receivedLists[0][0]
		K = self.receivedLists[0][2]
		temp = 0
		for i in range(1,len(self.receivedLists)):
			if Lmin > self.receivedLists[i][0]:
				Lmin = self.receivedLists[i][0]
				K = self.receivedLists[i][2]
				temp = i
			elif Lmin == self.receivedLists[i][0]:
				if K>self.receivedLists[i][2]:
					K = self.receivedLists[i][2]
					temp = i
		
		self.out_message = self.receivedLists[temp]	
		self.receivedLists = [self.out_message]
		
	# Determine the status of the search. The search may be a success, a failure
	# or not complete.
	def distributed_aug_status(self):
		t = math.floor(self.stack[-1])
		Lmin = self.out_message[0]
		tstar = self.out_message[1]
		astar = self.out_message[2]
		self.out_message = [0,0,0]
		# Search unsuccessful
		if Lmin==1000 and t == self.root:
			if self.ibar==self.id:
				self.matchedTo = self.root
				self.assig = np.append(self.assig,self.root)
			self.search_complete = True
			self.matching_exists = False
		# Search not complete, but reached a dead end.
		elif Lmin==1000 and t != self.root:
			if self.matchedTo==t:
			#self.out_message[1] = self.newMatch
				self.newMatch = self.matchedTo
			del self.stack[-1]
		# Search successful
		elif Lmin!=1000 and tstar==-1:
			if self.id == astar:
				self.newMatch=t
			self.search_complete = True
			self.matchedTo = self.newMatch
		# Search not complete, can still proceed down this branch.
		elif Lmin!=1000:
			if self.id == astar:
				self.newMatch = t
				self.f_i = True
			self.stack.append(tstar)
		
	# Agents decide how to proceed based on the status of the search.
	def distributed_aug_converge(self):
		# Receive status update from neighbours.
		self.out_message[1] = np.max([self.receivedLists[i][1] for i in range(len(self.receivedLists))])
		self.out_message[2] = np.min([self.receivedLists[i][2] for i in range(len(self.receivedLists))])
		
		# Search was successful according to message received from a neighbour.
		if self.out_message[2]==-1:
			self.search_complete = True
			self.matchedTo = self.newMatch
		# Search unsuccessful according to message received from a neighbour.
		if (not self.matching_exists) and self.ibar==self.id:
			self.matchedTo = self.root
			self.assig = np.append(self.assig,self.root)

