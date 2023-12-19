import numpy as np
import matplotlib.pyplot as plt

F = []
with open('input.txt') as file:
    for line in file:
        line = line.strip()
        F.append(list(line))
        
F = np.array(F)
N,M = F.shape
#%%
def add_pos(p,v, f=1):
    return (p[0] + f* v[0], p[1] + f*v[1])


def move_single(p,v):
    p_new = add_pos(p,v)
    if p_new[0] >= N or min(p_new) < 0 or p_new[1] >= M:
        return []
    else:
        if F[p_new] == '.':
            return [[p_new, v]]
        elif F[p_new] == '-':
            if abs(v[1]) > 0:
                return [[p_new, v]]
            else:
                return [[p_new,(0,1)], [p_new,(0,-1)]]
        elif F[p_new] == '|':
            if abs(v[0]) > 0:
                return [[p_new, v]]
            else:
                return [[p_new,(1,0)], [p_new,(-1,0)]]
        elif F[p_new] == '\\':
            if abs(v[1]) > 0:
                return [[p_new, (v[1], 0)]]
            else:
                return [[p_new, (0, v[0])]]
        elif F[p_new] == '/':
            if abs(v[1]) > 0:
                return [[p_new, (-v[1], 0)]]
            else:
                return [[p_new, (0, -v[0])]]
        else:
            raise ValueError('That is weird!')
            
def move(s):
    new_s = []
    for p in s:
        m = move_single(p[0], p[1])
        new_s +=m
    return new_s
#%%
def num_eneg(s):
    direc = {(1,0):0, (-1,0):1, (0,1):2, (0,-1):3}
    seen = np.zeros((F.shape[0], F.shape[1], 4), dtype=bool)
    eneg = np.zeros(F.shape, dtype=bool)
    while len(s)>0:
        s = move(s)
        rem_idx = []
        for i,p in enumerate(s):
            dirdx = p[0] + (direc[p[1]],)
            if seen[dirdx]:
                rem_idx.append(i)
            else:
                seen[dirdx] = True
            eneg[p[0]] = True
        
        s = [s[i] for i in range(len(s)) if not i in rem_idx]
    return np.sum(eneg)
#%% part one
print('Part one: ' + str(num_eneg([[(0,-1),(0,1)]])))
#%%
m = 0
for n in range(F.shape[0]):
    for p in [[(n,-1),(0,1)], [(n,F.shape[1]),(0,-1)], 
              [(-1,n),(1,0)], [(F.shape[0],n),(-1,0)]]:
        s = [p]
        m = max(num_eneg(s),m)
    
print('Part two: ' +str(m))
    