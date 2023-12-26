import numpy as np
import networkx as nx

F = []
with open('input.txt') as file:
    for line in file:
        F.append([l for l in line.strip()])
#%%
F = np.array(F)
N,M = F.shape
direcs = {(0,-1):['#', '>'], (0,1):['#','<'], 
          (1,0):['#','^'], (-1,0):['#','v']}
slopes = {'>':(0,1), '<':(0,-1), 
          'v':(1,0), '^':(-1,0)}

G = nx.DiGraph()
Ch = {}
P = {(0,1):[]}
J = [(0,1)]
St = []
    
ar = np.array
while len(J) > 0:
    n = J.pop()
    Ch[n] = []
    Ts = []
    if F[n] == '.':
        for d in direcs.keys():
            t = tuple(ar(d) + ar(n))
            if np.min(t) >=0 and np.all(ar(t) < (N,M))\
                and (t not in G.pred.get(n,[])):
                    if F[t] not in direcs[d]:
                        Ts.append(t)
                
    elif F[n] in slopes.keys():
        t = tuple(ar(slopes[F[n]]) + ar(n))
        if np.min(t) >=0 and all(ar(t) < (N,M)) and F[t] != '#':
            Ts.append(t)
    for t in Ts:
        G.add_edge(n, t)
        J.append(t)


#%% Prune Graph
Str = [[(0,1)]]
BG = nx.DiGraph()
Vis = {}
while len(Str)>0:
    rem = []
    ls = len(Str)
    for i in range(ls):
        Vis[Str[i][-1]] = True
        N = G[Str[i][-1]]
        P = G.pred[Str[i][-1]]
        if len(N) == 0:
           BG.add_edge(Str[i][0],Str[i][-1], weight=len(Str[i])-1)
           rem.append(i)
        elif max(len(N),len(P)) == 1:
            n = list(N.keys())[0]
            if Vis.get(n):
                if len(G.pred[n])>1:
                    BG.add_edge(Str[i][0],n, weight=len(Str[i]))
                rem.append(i)
            else:
                Str[i].append(n)
        else:
            rem.append(i)
            BG.add_edge(Str[i][0],Str[i][-1], weight=len(Str[i])-1)
            for n in N:
                if not Vis.get(n):
                    Str.append([Str[i][-1],n])
    Str = [Str[i] for i in range(len(Str)) if not i in rem]
#%%
print('Part one: ' + str(nx.dag_longest_path_length(BG)))
   
#%% part two
BGG = BG.to_undirected(as_view=False)
s = (0,1)
t = (F.shape[0]-1,F.shape[1]-2)

def dfs(Vis, n, d):
    m = 0
    r = 0
    path = [n]
    if n == t:
        return 0,path
    for nn in BGG[n]:
        if not Vis.get(nn):
            r+=1
            VVis = Vis.copy()
            VVis[nn] = True
            l, p = dfs(VVis, nn,d+1)
            l+= BGG.edges[n,nn]['weight']
            if l > m:
                m = l
                path = [n] + p
    if r == 0:
        return -np.inf, path
    return m, path

res, path = dfs({}, s, 0) 
    
print('Part two: ' + str(int(res)))
#%% visualization 
import matplotlib.pyplot as plt  
plt.close('all') 
pos = {p:(p[1],F.shape[0]-p[0]) for p in G.nodes}

P = nx.DiGraph()
for i in range(len(path)-1):
    P.add_edge(path[i],path[i+1])

nx.draw(BG,pos=pos,node_color = 'r',edge_color='w', with_labels=True)
nx.draw(P,pos=pos,node_color = 'b',edge_color='b', with_labels=True)  
        