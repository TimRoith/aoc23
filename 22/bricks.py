import numpy as np
import matplotlib.pyplot as plt

class brick:
    def __init__(self, a, b, idx):
        self.c = np.array([a,b])
        self.zmin = np.min(self.c[:,2])
        self.idx = idx
        self.xslice = slice(self.c[0,0], self.c[1,0]+1)
        self.yslice = slice(self.c[0,1], self.c[1,1]+1)
        self.zslice = slice(self.c[0,2], self.c[1,2]+1)
        
    def __repr__(self):
        return str(self.c)
       
B = []
with open('input.txt') as file:
    for i,line in enumerate(file):
        a,b = line.strip().split('~')
        B.append(brick([int(g) for g in a.split(',')], 
                       [int(g) for g in b.split(',')], i+1))
        
cmax = [0 for _ in range(3)]
for b in B:
    for i in range(3):
        cmax[i] = max(cmax[i], np.max(b.c[:,i])+1)
F = np.zeros(cmax)
B.sort(key=lambda x: x.zmin)
#%% Falling
def fall(F,B, mmin=1):
    for i in range(len(B)):
        idx = np.where(np.sum(F[B[i].xslice, ...][:,B[i].yslice, :],axis=(0,1)) > 0)[-1]
        m = 0
        if len(idx) > 0:
            m = max(idx)
        m+=mmin
        F[B[i].xslice, B[i].yslice, m:(m+B[i].c[1,2]-B[i].c[0,2]+1)] = B[i].idx
    return F,B
#%%
F,B = fall(np.zeros_like(F),B)
Sup = {}
By = {i:[] for i in range(1,len(B)+1)}
for i in range(1,len(B)+1):
    idx = np.where(F==i)
    g = np.unique(F[idx[0],idx[1],np.max(idx[2])+1])
    g = np.setdiff1d(g,[0])
    Sup[i] = g
    for j in g:
        By[j].append(i)
  
res = 0
for i in Sup.keys():
    dis = True
    for j in Sup[i]:
        if len(By[j]) == 1:
            dis = False
    if dis:
        res+=1
        if False:
            G = F.copy()
            G[np.where(F==i)]=0
            BB = [B[j] for j in range(len(B)) if B[j].idx != i]
            FF,_ = fall(0*G, BB)
            diff = np.sum(FF-G)
            print(diff)

print('Part one: ' +str(res))
#%% part two
res = 0 
for i in Sup.keys():
    G = F.copy()
    G[np.where(F==i)]=0
    BB = [B[j] for j in range(len(B)) if B[j].idx != i]
    FF,_ = fall(0*G, BB)
    f_num = len(np.setdiff1d(np.unique(G[np.where(np.abs(G-FF) > 1e-6)]), [0]))
    res += f_num
    
print('Part two: ' +str(res))