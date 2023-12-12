import numpy as np

G = []
GS = {}
with open('input.txt') as file:
    idx = 1
    for i,line in enumerate(file):
        GG = []
        line = line.strip()
        for j,l in enumerate(line):
            if l == '.':
                GG.append(0)
            else:
                GG.append(idx)
                idx+=1
                GS[(i,j)] = np.array([i,j],dtype=float)
        G.append(GG)
G = np.array(G)

add = 1
add = 1000000-1
for i in range(max(G.shape)):
    # rows
    if i < G.shape[0]:
        if np.sum(G[i,:]) == 0:
            for g in GS:
                if g[0]>i:
                    GS[g] += np.array([add,0])
    # cols
    if i < G.shape[1]:
        if np.sum(G[:,i]) == 0:
            for g in GS:
                if g[1]>i:
                    GS[g] +=  np.array([0,add])
                    
#%% compute dists
dists = []
GSL = list(GS.values())
for i in range(len(GS)):
    for j in range(i+1, len(GS)):
        dists.append(np.abs(GSL[i] - GSL[j]).sum())
        
res = sum(dists)
print(res)
        

        