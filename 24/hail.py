import numpy as np

X = []
V = []
with open('input.txt') as file:
    for line in file:
        line = line.strip()
        x,v = line.split(' @ ')
        X.append([int(xx) for xx in x.split(', ')])
        V.append([int(vv) for vv in v.split(', ')])
        
X = np.array(X)
V = np.array(V)
#%%
def cross_2D(X, V):
    V = V.copy()
    V[1,:]*=-1
    D = X[1,:] - X[0,:]
    try:
        return np.linalg.solve(V.T,D)
    except np.linalg.LinAlgError as err:
        return [np.inf,np.inf]

area = [7.,17.]
area=[200000000000000.,400000000000000.]
f = 0
for i in range(X.shape[0]):
    for j in range(X.shape[0]):
        if j <= i:
            continue
        t = cross_2D(X[[i,j],:2], V[[i,j],:2])
        if np.min(t) < 0:
            pass#print('In the past')
        elif t[0] == np.inf:
            pass#print('Parallel')
        else:
            c = t[0] * V[i,:2] + X[i,:2]
            if np.min(c) >= area[0] and np.max(c) <= area[1]:
                f+=1
            else:
                pass#print('Out at: ' +str(c))
print('Part one: ' + str(f))
#%% Part two
A = np.zeros((6,6))
F = np.zeros(6)
for i in [0,1]:
    A[3*i:3*(i+1),:3] = np.cross(np.eye(3), V[0,:] - V[i+1,:])
    A[3*i:3*(i+1),3:] = np.cross(np.eye(3), X[i+1,:] - X[0,:])
    F[3*i:3*(i+1)]    = np.cross(X[i+1,:], V[i+1,:]) - np.cross(X[0,:], V[0,:])

XV = np.round(np.linalg.solve(A, F))
print('Part two: ' +str(int(np.sum(XV[:3]))))

#%%
import cbx
N = X.shape[0]
d = N + 2*3
def f(tXV,s = 1):
    return 0.5*np.linalg.norm(tXV[:N,None] *\
                (V[:N,:]-np.repeat(tXV[None,N:N+3],N,axis=0))+\
                 X[:N,:]/s - np.repeat(tXV[None,N+3:],N,axis=0), axis=(0,1))+\
            100 * np.sum(np.abs(np.minimum(tXV[:N],0)))

dyn = cbx.dynamics.CBO(f,d=d, noise='anisotropic',
                       M=3,
                       N=100,
                       term_args={'max_it':1e5},sigma=8.1)
dyn.optimize()
#%%
x = dyn.best_particle[0,:]
f(x)
#%%
res = np.round(dyn.best_particle[0,N:]).astype(int)
print('X: ' +str(res[3:]))
print('V: ' +str(res[:3]))
