import numpy as np
symbs = []
with open('input.txt', 'r') as file:
    for line in file:
        line = line.rstrip()
        symbs.append([l for l in line])
        
def get_symb(pos):
    if min(pos[0], pos[1]) < 0 or pos[1]>=symbs.shape[1] or pos[0]>=symbs.shape[0]:
        return None
    else:
        return symbs[pos]
#%%
symbs = np.array(symbs)
pos = np.where(symbs=='S')
pos = (pos[0][0], pos[1][0])
loop = [(pos,None)]
dir_dict = {'|':['N', 'S'], '-':['E', 'W'], 
            'F':['S', 'E'], 'J':['W', 'N'],
            'L':['N', 'E'], '7':['S', 'W']}
dir_neg = {'N':'S', 'S':'N', 'E':'W', 'W':'E'}

def comp(direc, symb):
    if symb not in dir_dict.keys():
        return False
    return dir_neg[direc] in dir_dict[symb]

def add_pos(p, pp, f=1):
    return (p[0]+ f* pp[0], p[1]+f*pp[1])

def get_dir(symb, d):
    ind = 0
    if d == dir_dict[symb][0]:
        ind = 1
    return dir_dict[symb][ind]

stencil = {'N':(-1,0), 'S':(1,0), 'W':(0,-1), 'E':(0,1)}
dists = -1* np.ones(symbs.shape, dtype=int)
dists[pos] = 0         
for d in stencil.keys():
    new_pos = add_pos(pos, stencil[d])
    if comp(d, get_symb(new_pos)):
        dists[new_pos]=1
        if len(loop) > 1:
            loop.insert(0, (new_pos, dir_neg[d]))
        else:
            loop.append((new_pos, dir_neg[d]))
#%%
term = False
while not term:
    for i in [0,-1]:
        e = loop[i]
        cur_symb = get_symb(e[0])
        d = get_dir(cur_symb, e[1])
        new_pos = add_pos(e[0], stencil[d])
        if dists[new_pos] >= 0:
            term = True
        else:
            if i == 0:
                loop.insert(i,(new_pos, dir_neg[d]))
            else:
                loop.append((new_pos, dir_neg[d]))
            dists[new_pos] = dists[e[0]] + 1
            
print('Max dist: ' +str(np.max(dists)))
#%% vis path
import matplotlib.pyplot as plt
I = np.zeros_like(dists, dtype=float)
I[np.where(dists>=0.)] = 1.
plt.imshow(I)


#%% part2
a = np.where(dists>=0)
xmin = a[0].min()
xmax = a[0].max()
ymin = a[1].min()
ymax = a[1].max()
pos_tile = -1*np.ones_like(dists)
ccs = []
idx = 0
for i in range(xmin,xmax):
    for j in range(ymin,ymax):
        if dists[i, j] == -1:
            ccs.append(([i], [j]))
            pos_tile[i,j] = idx
            idx+=1
            
loop_dict = {}
loop_vec = {}
for i in range(len(loop)):
    loop_dict[loop[i][0]] = i
       
def find_comp(s):
    num = pos_tile[s]
    for d in stencil:
        new_pos = add_pos(s, stencil[d])
        symb = get_symb(new_pos)
        if not symb is None:
            new_num = pos_tile[new_pos]
            if new_num != num:
                if  new_num >= 0:
                    c = ccs[new_num]
                    pos_tile[c] = num
                    cn = (ccs[num][0] + c[0], ccs[num][1] + c[1])
                    ccs[num] = cn
                    ccs[new_num] = cn
                elif new_pos not in loop_dict.keys():
                    pos_tile[new_pos] = num
                    cn = (ccs[num][0] + [new_pos[0]], ccs[num][1] + [new_pos[1]])
                    ccs[num] = cn
                    find_comp(new_pos)
                
            

a = np.where(pos_tile>=0.)
for i in range(len(a[0])):
    s = (a[0][i], a[1][i])
    find_comp(s)
 
ind = np.unique(pos_tile)[1:]
ccs = [ccs[i] for i in ind]

    
ov = {(0,-1):[(-1,0),(0,1)],
      (0,1):[(1,0),(0,1)],
      (1,0):[(0,-1),(1,0)],
      (-1,0):[(-1,0),(0,1)]}

plt.close('all')
fig, ax = plt.subplots(1,)
I = np.zeros((dists.shape[0],dists.shape[1],3))
I[...,1] = dists/dists.max()*0.99

    
#%%
I = np.zeros((2*dists.shape[0], 2*dists.shape[1],3))
for i in range(len(loop)):
    pp = loop[i-1][0]
    p = loop[i][0]
    d = add_pos(p, pp, f=-1)
    gg = add_pos(d,pp,f=2)
    pp = add_pos((0,0),p,f=2)
    I[...,0][gg]=1.
    I[...,0][pp]=1.
    
loop = loop[::-1]
#%%
cwd = {(-1,0):(0,1), (0,1):(1,0), (1,0):(0,-1), (0,-1):(-1,0)}
ccwd = {cwd[k]:k for k in cwd.keys()}
def angle(d,dd):
    return np.arccos(d[0]*dd[0] + d[1] * dd[1])

def rot(dds,cw=True):
    r=[]
    for dd in dds:
        if cw:
            r.append(cwd[dd])
        else:
            r.append(ccwd[dd])
    return r
   
#loop = loop[::-1] 
D = np.prod(dists.shape)+1
d = add_pos(loop[0][0], loop[-1][0], f=-1)
d2 = add_pos(loop[1][0], loop[0][0], f=-1)
dds = [(1,0),(0,1)]
dds = [(1,0),(0,-1)]

for i in range(len(loop)):
    p  = loop[i]
    print(p)
    pp = loop[i-1]
    ppp = loop[(i+1)%len(loop)]
    d = add_pos(p[0], pp[0], f=-1)
    d2 = add_pos(ppp[0], p[0], f=-1)
    cw = False
    norot=False
    if d == d2:
       norot=True 
    elif d==(0,-1) and d2==(-1,0):
        norot=True
        dds=[(-1,0),(0,1)]
    elif d==(0,1) and d2==(1,0):
        norot=True
        dds=[(1,0),(0,-1)]
    elif d==(-1,0) and d2==(0,1):
        norot=True
        dds=[(1,0),(0,1)]
    elif d==(1,0) and d2==(0,-1):
        norot=True
        dds=[(-1,0),(0,-1)]
    elif d==(1,0) and d2==(0,1):
        norot=True
    elif d==(0,1) and d2==(-1,0):
        cw=False
    elif d==(0,-1) and d2==(1,0):
        cw=False
    elif d==(-1,0) and d2==(0,-1):
        norot=True
        dds=[(-1,0),(0,1)]
    else:
        print('WEIRDD')
        print(d)
        print(d2)
    if not norot:
        dds = rot(dds,cw)
        
    
    for dd in dds:        
        gg = add_pos(p[0], dd)
        I[...,1][add_pos((0,0), p[0],f=2)] = 1.
        if not get_symb(gg) is None:
            if pos_tile[gg] >= 0:# and pos_tile[gg] < D:
                a = np.where(pos_tile==pos_tile[gg])
                pos_tile[a] = D
                for i in range(len(a[0])):
                    I[...,2][2*a[0][i], 2*a[1][i]]=1
            I[...,2][add_pos((0,0), gg,f=2)]=1.
            I[...,1][add_pos((0,0), gg,f=2)]=1.
    show=False
    if show:
        ax.imshow(I)
        plt.pause(2.5)
        ax.clear()
    I[...,1]=0
    I[...,2]=0
    
for i in range(dists.shape[0]):
    for j in range(dists.shape[1]):
        if pos_tile[i,j]==D:
            I[2*i,2*j,1]=1.
    
#%%  
plt.imshow(I)
A = I[...,0]

from skimage.segmentation import flood, flood_fill
A = flood_fill(A, (0, 0), 1)
A = flood_fill(A, (250, 250), 1)

I[...,0][np.where(A>0.)]=1
plt.imshow(I)

b = np.where(np.logical_and(A>0, I[...,1]>0))
#%%
pos_tile[np.where(pos_tile!=D)] = 0.             
#plt.imshow(pos_tile)
  
res = len(np.where(pos_tile==D)[0])
print('number of tiles: ' + str(res))


    
