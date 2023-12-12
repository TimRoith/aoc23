import numpy as np

NN = []
RR = []
d = {'?':-1, '#':1, '.':0}
with open('input_ex.txt') as file:
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


#%%
def equal(A,B):
    if A.shape != B.shape:
        return False
    else:
        return np.allclose(A, B)
    
def get_split(a):
    c = np.where(a==0)[0]
    cc = np.zeros((len(c)+2))
    cc[0]=-1
    cc[-1]=len(a)
    cc[1:-1]=c
    d = cc[1:]-cc[:-1]-1
    return d[d!=0]
        
        
def fill_line(R,N):
    if len(R)==0:
        return len(N) == 0
    else:
        res = 0
        # 0 in first: Test if no entry in first works
        if R[0] != 1:
            res += fill_line(R[1:], N)
        # 1 in first:
        if len(N) > 0:
            p = split_zero(R)
            a = len(np.where(p[0]==-1)[0])
            n_min = len(p[0])-a
            n_max = len(p[0])
            
            if N[0] <= n_max and N[0] >=n_min:
                idx = N[0]+1
                print(R)
                print(N)
                res += fill_line(R[idx:], N[1:])
                

        return res
  
# for i in range(len(RR)):           
#     r = fill_line(RR[i],NN[i])
#     nums+=r
    
print(fill_line(RR[1],NN[1])  )
    

# #%% part two
# for i in range(len(RR)):
#     R = RR[i]
#     Rs = [R]
#     for j in range(4):
#         Rs.append(np.array([-1]))
#         Rs.append(R)
#     RR[i] = np.concatenate(Rs)
# #%%   
# nums = 0
# for i in range(len(RR)):           
#     r = fill_line(RR[i],NN[i])
#     nums+=r
#     print('At '+str(100*(i/len(RR))) + '%')