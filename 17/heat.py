import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from heapq import heappush, heappop

F = []
with open('input.txt') as file:
    for line in file:
        line = line.strip()
        F.append([int(l) for l in line])
        
F = np.array(F)
#%%
def all_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)
def same_direc(P):
    if None in P:
        return False
    else:
        R = [add_pos(P[i+1],P[i],f=-1) for i in range(len(P)-1)]
        return all_equal(R)

def add_pos(a,b, f=1):
    return tuple(p+ f*q for p, q in zip(a, b))
    
def rev_direc(p):
    return (-p[0], -p[1])

def in_bounds(p):
    if min(p) >= 0 and p[0] < F.shape[0] and p[1] < F.shape[1]:
        return True
    return False
direc = {(1,0):0, (-1,0):1, (0,1):2, (0,-1):3}
class node:
    def __init__(self, P, parent):
        self.parent = parent
        self.P = P
        
    def neigh(self,):
        N = []
        if self.P[-2] is not None:
            N.append(add_pos(self.P[-2],self.P[-1],f=-1))
        if same_direc(self.P):
            N.append(add_pos(self.P[-1],self.P[-2],f=-1))
        res = []
        for d in direc.keys():
            if not d in N:
                p_new = add_pos(self.P[-1], d)
                dirs = self.P[1:]
                dirs += (p_new,)
                if in_bounds(p_new):
                    res.append(node(dirs, self))
        return res
    def __repr__(self,):
        return str(self.P)
    def __lt__(self, other):
        return True
    def __le__(self, other):
        return True
#%% dijkstra
def dijkstra(h, s, t):
    vis = {}
    dists = {}
    dists[s] = 0
    term = False
    while len(h) > 0 and not term:
        d,N = heappop(h)
        if not vis.get(N.P, False):
            vis[N.P] = True
            Ns = N.neigh()
            hcur = dists.get(N.P, float('inf'))
            for g in Ns:
                if not vis.get(g.P,False):
                    dist = hcur + F[g.P[-1]]
                    if dist < dists.get(g.P,float('inf')):
                        dists[g.P] = dist
                        heappush(h, (dist,g))
        if N.P[-1] == target:
            if len(N.neigh())>0:
                term = True
                t_node = N
            else:
                dists[N.P] = float('inf')
    return t_node, dists
#%% part one
target = (F.shape[0]-1, F.shape[1]-1)
s = (None,None,None,(0,0))
h = []
heappush(h, (0, node(s, None)))
t_node, dists = dijkstra(h,s, target)     
#%% vis path
plt.close('all')
fig, ax = plt.subplots(1,2)
G = np.zeros(F.shape)
num = 0
t = t_node
while t:
    G[t.P[-1]] = num
    num +=1
    t = t.parent
plt.imshow(G)    

print('The result is: ' +str(dists[t_node.P]))   

#%% part two
class ultra_node(node):
    def __init__(self, P, parent):
        super().__init__(P, parent)
        
    def neigh(self):
        if not same_direc(self.P[-5:]) and self.P[-2] is not None:
            diff = add_pos(self.P[-1], self.P[-2], f=-1)
            p_new = add_pos(self.P[-1], diff)
            dirs = self.P[1:]
            dirs += (p_new,)
            if in_bounds(p_new):
                return [ultra_node(dirs, self)]
            else:
                return []
        else:
            N = []
            res = []
            if self.P[-2] is not None:
                N.append(add_pos(self.P[-2],self.P[-1],f=-1))
            if same_direc(self.P):
                N.append(add_pos(self.P[-1],self.P[-2],f=-1))
            for d in direc.keys():
                if not d in N:
                    p_new = add_pos(self.P[-1], d)
                    dirs = self.P[1:]
                    dirs += (p_new,)
                    if in_bounds(p_new):
                        res.append(ultra_node(dirs, self))
            return res

#%%
target = (F.shape[0]-1, F.shape[1]-1)
s = tuple([None for i in range(10)]) + ((0,0),)
h = []
heappush(h, (0, ultra_node(s, None)))
t_node, dists = dijkstra(h,s, target)
#%% vis path
plt.close('all')
fig, ax = plt.subplots(1,1)
G = np.zeros(F.shape)
num = 0
t = t_node
while t:
    if t.P[-1] == (0,10):
        gg = t
    G[t.P[-1]] = num
    num +=1
    t = t.parent

plt.imshow(G)    

print('The result is: ' +str(dists[t_node.P]))             
        
    


    
    
    
        
    

        
    
        
            
                    
        