# Extension to Agent class showing alternative behaviour of individual agents.
# Code written by Mitchell Khoo, PhD student at The University of Melbourne.

# Based on paper submitted to CDC:
# "Distributed Algorithm for Solving the Bottleneck Assignment Problem",
# Mitchell Khoo, Tony A. Wood, Chris Manzie, Iman Shames.


import numpy as np
import math
from agentBAP1 import Agent

class AgentBFS(Agent):
	def __init__(self,id,costs):
		Agent.__init__(self,id,costs)
		self.descendants = []
		
################################################################################
	#Overridden Functions for Breadth-first Search	
	
	def receive(self,y_k):
		#print(self.receivedLists,y_k)
		if np.isscalar(y_k[0]):
			self.receivedLists = np.append(self.receivedLists,[y_k],axis=0)
		else:
			self.receivedLists = np.append(self.receivedLists,y_k,axis=0)
		
	def distributed_aug_init(self):
		Agent.distributed_aug_init(self)
		self.receivedLists = [[-1,self.out_message[1]]]
		self.deadend = False
	
	def local_choose_agent_to_explore(self):
		self.out_message = [-1,-1]
		if self.f_i == False:
			for i in range(len(self.receivedLists)):
				if self.receivedLists[i][1] in self.assig:
					self.f_i = True
					self.descendants = [self.matchedTo]
					if self.matchedTo == -1:
						self.out_message = [self.receivedLists[i][1], (self.id+1)*-1]
					else:
						self.out_message = [self.receivedLists[i][1], self.matchedTo]
					self.newMatch = self.receivedLists[i][1]
					break
		elif self.f_i == True and self.deadend == False:
			# num_des = len(self.descendants)
			live = False
			for i in range(len(self.receivedLists)):
				if self.receivedLists[i][0] in self.descendants:
					self.descendants.append(self.receivedLists[i][1])
					live = True
				elif self.receivedLists[i][1] in self.descendants:
					live = True
			if live==False:
				self.deadend == True
		self.receivedLists = [self.out_message]
		#print(self.receivedLists)
		
	def converge_agent_to_explore(self):
		self.out_message = np.unique(self.receivedLists,axis=0)
		self.receivedLists = self.out_message
		
	def distributed_aug_status(self):
		self.receivedLists = self.receivedLists[np.invert(np.all(self.receivedLists[:]==[-1,-1],axis=1))]
		self.out_message = [-1,-1,-1]
		if len(self.receivedLists)==0:
			self.search_complete = True
			self.matching_exists = False
			#self.receivedLists = [self.out_message]
			if self.ibar==self.id:
				self.matchedTo = self.root
				self.assig = np.append(self.assig,self.root)
		#elif np.any(np.isin(self.receivedLists,[-1])):
		elif len(self.receivedLists[self.receivedLists<0])>0:
			#print(self.receivedLists,self.receivedLists[self.receivedLists<0],self.id)
			self.search_complete = True
			winner = np.min(self.receivedLists[self.receivedLists<0])
			#print(winner,self.id)
			if self.id+1 == -1*winner or self.receivedLists[np.where(self.receivedLists==winner)[0][0]][0] in self.descendants:
				self.matchedTo = self.newMatch
			# if self.f_i == True and self.matchedTo == -1:
				# self.out_message = [10,self.newMatch,self.id]
			# self.receivedLists = [self.out_message]
			#print(self.matchedTo,self.id)
	
	# def distributed_aug_converge(self):
		# if self.receivedLists[0][2] == self.id or self.receivedLists[0][1] in self.descendants:
			# self.matchedTo = self.newMatch
			
		
			