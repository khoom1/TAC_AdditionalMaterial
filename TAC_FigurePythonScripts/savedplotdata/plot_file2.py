import numpy as np
import matplotlib.pyplot as plt

a = np.load('timevsn_BFS.npy')
b = np.load('timevsn_DFS.npy')
c = np.load('timevsn_BFS_sparse.npy')
d = np.load('timevsn_DFS_sparse.npy')

max_it = 50
num_ave = 100
scale = 2
plt.figure(figsize=(15,5))
plt.rc('text',usetex=True)
plt.rc('font',family='serif')
plt.xlabel("Number of tasks, n",fontsize=18)
plt.ylabel("Average time steps",fontsize=18)
plt.plot([i for i in range(2,max_it+1)],b/num_ave,'b.',label="AugDFS()")
plt.plot([i for i in range(2,max_it+1)],a/num_ave,'rx',label="AugBFS()")

plt.plot([i for i in range(2,max_it+1)],d/num_ave,'b^',label="AugDFS(), sparse $\mathcal{G}_b$")
plt.plot([i for i in range(2,max_it+1)],c/num_ave,'rp',label="AugBFS(), sparse $\mathcal{G}_b$")

plt.xticks(np.arange(0,len(a)+scale,scale))
# plt.yscale('log')
plt.xlim(2,len(a)+1)
plt.legend(loc='upper left', prop={'size':14})
plt.show()

print(a,b)