import numpy as np

NN = []
RR = []
d = {'?':-1, '#':1, '.':0}
with open('input.txt') as file:
    for line in file:
        line = line.strip()
        R,N = line.split(' ')
        N = np.array([int(n) for n in N.split(',')])
        R = np.array([d[r] for r in R])
        RR.append(R)
        NN.append(N)
        
def split_zero(a):
    idx = np.where(a!=0)[0]
    return np.split(a[idx],np.where(np.diff(idx)!=1)[0]+1)

mem = {}
def rec(R,N):
    r = tuple(R)
    n = tuple(N)
    if len(R) == 0:
        return len(N) == 0
    elif (r,n) in mem.keys():
        return mem[(r,n)]
    else:
        res = 0
        # test if 0 in first position works
        if R[0] != 1:
            res += rec(R[1:], N)
        # test if we can process first number
        if len(N) > 0 and R[0] != 0:
            sp = split_zero(R)[0]
            if (len(sp) > N[0] and sp[N[0]] == -1) or (len(sp) == N[0]):
                res += rec(R[(N[0]+1):], N[1:])
            
        mem[(r,n)] = res
        return res

nums = 0
for i in range(len(RR)):
    nums+=rec(RR[i],NN[i])
print(nums)

#%% part two
for i in range(len(RR)):
    R = RR[i]
    Rs = [R]
    N = NN[i]
    NNN = [N]
    for j in range(4):
        Rs.append(np.array([-1]))
        Rs.append(R)
        NNN.append(N)
    RR[i] = np.concatenate(Rs)
    NN[i] = np.concatenate(NNN)
#%%   
nums = 0
for i in range(len(RR)):
    nums+=rec(RR[i],NN[i])
print(nums)