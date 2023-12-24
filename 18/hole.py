import numpy as np
import matplotlib.pyplot as plt
from skimage.segmentation import flood_fill
I = []
with open('input.txt') as file:
    for line in file:
        line = line.strip()
        R, N, C = line.split(' ')
        N = int(N)
        I.append([R,N,C])
#%%
def add_pos(a,b, f=1):
    return tuple(p+ f*q for p, q in zip(a, b))    
direcs = {'R':(0,1), 'L':(0,-1), 'D':(-1,0), 'U':(1,0)}

A = {((-1,0),(0,1),(-1,0)):0,  ((1,0),(0,1),(-1,0)) :1,
     ((-1,0),(0,1),(1,0)) :-1, ((1,0),(0,1),(1,0))  :0,
     # - left
     ((-1,0),(0,-1),(-1,0)):0, ((1,0),(0,-1),(-1,0))  :-1,
     ((-1,0),(0,-1),(1,0)) :1, ((1,0),(0,-1),(1,0)):0,
     # - up
     ((0,1),(1,0),(0,1)):0,   ((0,-1),(1,0),(0,1)):1,
     ((0,1),(1,0),(0,-1)):-1, ((0,-1),(1,0),(0,-1)):0,
     # - down
     ((0,1),(-1,0),(0,1)):0,   ((0,-1),(-1,0),(0,1)):-1,
     ((0,1),(-1,0),(0,-1)):1, ((0,-1),(-1,0),(0,-1)):0,
     }

def coord(I, p):
    c = []
    for i in range(len(I)):
        dp = direcs[I[i-1][0]]
        d  = direcs[I[i][0]]
        dn = direcs[I[(i+1)%len(I)][0]] 
        p = add_pos(p,d, f=I[i][1] + A[(dp,d,dn)])
        c.append(p)
        d_old = d
    C = np.array([p]+ c)
    for i in [0,1]:
        C[:,i] -= np.min(C[:,i])
    return C
  
def area(C):
    area = 0.
    for i in range(len(C)):
        d = C[i,:] - C[i-1,:]
        if np.abs(d[1]) > 0:
            d = d[1]
            g = float(C[i-1, 0])
            area+= d * g
    return np.abs(area)
#%%
p = (0,0)
C = coord(I, p)         
print('Part one: ' +str(area(C)))
#%% part two
direcs2 = {0:direcs['R'], 1:direcs['D'], 
           2:direcs['L'], 3:direcs['U']}

def to_inst(h):
    d = direcs2[int(h[-1])]
    n = int(h[1:-1], 16)
    return d, n

def coord2(I, p):
    c = []
    for i in range(len(I)):
        dp,_ = to_inst(I[i-1][-1][1:-1])
        d,n  = to_inst(I[i][-1][1:-1])
        dn, _ = to_inst(I[(i+1)%len(I)][-1][1:-1])
        p = add_pos(p,d, f=n + A[(dp,d,dn)])
        c.append(p)
        d_old = d
    C = np.array([p]+ c)
    for i in [0,1]:
        C[:,i] -= np.min(C[:,i])
    return C

p = (0,0)
C = coord2(I, p)

A = float(np.max(C[:,0])) * float(np.max(C[:,0]))
print('Part two: ' +str(area(C)))
        
    