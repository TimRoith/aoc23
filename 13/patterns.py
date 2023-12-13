import numpy as np

P = []
p = []
d = {'#':1, '.':0}
with open('input.txt') as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            P.append(np.array(p))
            p = []
        else:
            p.append([d[r] for r in line])
    P.append(np.array(p))
    
def check_reflect(A,idx, axis=0):
    r = idx+1
    bxis = (axis+1)%2
    m = min(A.shape[bxis]-r,r)
    s = (idx+1) - m
    
    a = A.take(indices=range(s,r),axis=bxis)
    b = np.flip(A.take(indices=range(r,r+m),axis=bxis),axis=bxis)
    return np.allclose(a, b)
    
    
def get_pos_reflect(A, axis=0):
    res = []
    p = np.sum(A, axis=axis)
    d = np.where(p[1:]-p[:-1]==0)[0]
    for idx in d:
        if check_reflect(p[None,:], idx, axis=0):
            res.append(idx)
    return res
 
def get_reflect(A):
    for axis in [0,1]:
        if axis==1:
            5
        for idx in get_pos_reflect(A,axis=axis):
            if check_reflect(A, idx, axis=axis):
                return (idx,axis)
    else:
        return None
  
res = 0
for p in P:
    (i, ax) = get_reflect(p)
    res += (i+1) * (1+ 99 * ax)
print(res)

#%% part two
def quant_reflect(A,idx, axis=0):
    r = idx+1
    m = min(A.shape[axis]-r,r)
    s = (idx+1) - m
    
    a = A.take(indices=range(s,r),axis=axis)
    b = np.flip(A.take(indices=range(r,r+m),axis=axis),axis=axis)
    return np.sum(np.abs(a-b))

def all_reflect(A):
    for axis in [0,1]:
        for idx in range(0,A.shape[axis]-1):
            if quant_reflect(A,idx, axis=axis)==1:
                return (idx,axis)
    return None
res = 0           
for p in P:
    (idx, ax) = all_reflect(p)
    res += (idx+1) * (1+ 99 * ((ax+1)%2))
print(res)
            
    
    
