import networkx as nx

G = nx.Graph()
with open('input.txt') as file:
    for line in file:
        N,NN = line.strip().split(': ')
        for n in NN.split(' '):
            G.add_edge(N, n)
#%%            
Nl = list(G.nodes)
_, C = nx.stoer_wagner(G)
print('Part one: ' + str(len(C[0])*len(C[1])))
        