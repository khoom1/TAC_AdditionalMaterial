# Based on CBAA by Choi, Han-Lim, Luc Brunet, and Jonathan P. How,
# "Consensus-based decentralized auctions for robust task allocation",
# IEEE transactions on robotics 25.4 (2009): 912-926.

# Written by Mitchell Khoo, The University of Melbourne
import numpy as np
class AgentCBAA:

	def __init__(self,id,costs):
		self.id = id
		self.costs = costs
		self.numTasks = len(costs)
		self.x_i = [0 for x in range(self.numTasks)]
		self.y_i = [0 for x in range(self.numTasks)]
		
		self.out_message = self.y_i
		self.receivedLists = [self.out_message]
		self.winningAgentsList = [-1 for x in range(self.numTasks)]
		
	def selectTask(self):
		if np.sum(self.x_i)==0:
			h_i = [self.costs[i]>self.y_i[i] for i in range(self.numTasks)]
			#print(h_i,self.id)
			if np.sum(h_i)>0:
				self.J_i = np.argmax(np.multiply(h_i,self.costs))
				self.x_i[self.J_i]=1
				self.y_i[self.J_i]=self.costs[self.J_i]
				self.winningAgentsList[self.J_i] = self.id
			else:
				self.J_i = -1
		self.out_message = self.y_i
		self.receivedLists = [self.out_message]
		self.receivedAgentsList = [self.winningAgentsList]
		
	
	def get_outgoing_message(self):
		return [self.out_message,self.winningAgentsList,self.J_i]
	
	def receive(self,vector):
		y_k = vector[0]
		winningAgentsList = vector[1]
		J_i = vector[2]
		self.receivedLists = np.append(self.receivedLists,[y_k],axis=0)
		self.receivedAgentsList = np.append(self.receivedAgentsList, [winningAgentsList],axis=0)
		#self.receivedJs = np.append(self.receivedJs, J_i)
	

	
	def consensus(self):
		maxAtJ_i = self.y_i[self.J_i]
		z = self.id
		maxBids = self.y_i
		for i in range(1,len(self.receivedLists)):
			maxBids = np.maximum(maxBids,self.receivedLists[i])
		#print(maxBids)
		for i in range(1,len(self.receivedLists)):
			for j in range(self.numTasks):
				max = np.max([self.y_i[j],self.receivedLists[i][j]])
				if max==maxBids[j] and self.y_i[j]<max:
					self.y_i[j] = maxBids[j]
					self.winningAgentsList[j] = self.receivedAgentsList[i][j]
					if j==self.J_i:
						self.x_i[j] = 0
				if max==maxBids[j] and self.y_i[j]==self.receivedLists[i][j]:
					self.winningAgentsList[j] = np.max([self.winningAgentsList[j],self.receivedAgentsList[i][j]])
					if j==self.J_i and self.winningAgentsList[j]>self.id:
						self.x_i[j] = 0
			#if self.id==3:
			#	print(self.receivedJs[i]==self.J_i,self.receivedJs)
			#self.y_i = np.maximum(self.y_i,self.receivedLists[i])
			
			#if maxAtJ_i < self.receivedLists[i][self.J_i]:
			#	self.x_i[self.J_i] = 0
				
			#elif maxAtJ_i == self.receivedLists[i][self.J_i] and self.receivedJs[i]==self.J_i:
			#	if self.id > self.receivedIDs[i]:
			#		self.x_i[self.J_i] = 0
		#print(self.id,self.receivedLists,self.x_i,self.winningAgentsList)
		#print(" ")
	