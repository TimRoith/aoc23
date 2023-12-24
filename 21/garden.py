import numpy as np

G = []
enc = {'#':-2, '.':-1, 'S':0}
with open('input_ex.txt') as file:
    for line in file:
        G.append([enc[l] for l in line.strip()])
        
F = np.array(G)
#%%
def step(F,p, st):
    qs = [(p[0]+i, p[1]+ j) for (i,j) in [(-1,0),(1,0),(0,-1),(0,1)]]
    for q in qs:
        if min(q)>=0 and q[0] < F.shape[0] and q[1] < F.shape[1] and F[q]>=-1:
            F[q] = st
    return F

#%%
steps = 16
pos = np.where(F==0)
for i in range(steps):
    for j in range(len(pos[0])):
        F = step(F, (pos[0][j], pos[1][j]), i+1)
    pos = np.where(F==i+1)
    
print('Part one: ' +str(np.sum(F==steps)))

#%% part two
F = np.array(G)
r = 2*2 + 1
N,M = F.shape

st = np.arange(F.shape[0]//2, r*F.shape[0], F.shape[0])[:3]
tiles = []
for steps in st:
    BF = np.tile(F, [r,r]).copy()
    pos = ([r//2 * N + N//2], [r//2 * M + M//2])
    for i in range(steps):
        for j in range(len(pos[0])):
            BF = step(BF, (pos[0][j], pos[1][j]), i+1)
        pos = np.where(BF==i+1)
    tiles.append(np.sum(BF==steps))
p = np.polyfit(st[:len(tiles)], tiles, deg=2)
def pred(D,p):
    return np.sum([D**(len(p)-i-1)*p[i] for i in range(len(p))])
D = 26501365
print('Part one: ' +str(int(pred(D,p))))

        