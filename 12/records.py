import numpy as np

def get_split(a):
    c = np.where(a==0)[0]
    cc = np.zeros((len(c)+2))
    cc[0]=-1
    cc[-1]=len(a)
    cc[1:-1]=c
    d = cc[1:]-cc[:-1]-1
    return d[d!=0]

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
        
def equal(A,B):
    if A.shape != B.shape:
        return False
    else:
        return np.allclose(A, B)

#%% part one
def get_nums(RR,NN):
    nums = 0
    for i in range(len(RR)):
        R = RR[i]
        N = NN[i]
        x = np.where(R==-1)[0]
        num = 0
        for j in range(2**len(x)):
            Rc = R.copy()
            Rc[x]=0
            for k,d in enumerate(str(bin(j))[2:][::-1]):
                Rc[x[-k]] = int(d)
            #print(Rc)
            if equal(get_split(Rc), N):
                num+=1
        nums+=num
        print('At '+str(100*(i/len(RR))) + '%')
        
    print(nums)
get_nums(RR,NN)
#%% part two
for i in range(len(RR)):
    R = RR[i]
    Rs = [R]
    for j in range(4):
        Rs.append(np.array([-1]))
        Rs.append(R)
    RR[i] = np.concatenate(Rs)
            
get_nums(RR,NN)      


        