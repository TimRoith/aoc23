import numpy as np
R = []
d = {'#':-1, '.':0, 'O':1}
dd = {d[k]:k for k in d.keys()}
with open('input.txt') as file:
    for line in file:
        line = line.strip()
        if len(line) > 0:
            R.append([d[r] for r in line])
R = np.array(R)

def to_vis(R):
    RR = ''
    for i in range(R.shape[0]):
        a =''
        for r in R[i,:]:
            a+= dd[r]
        RR+= a+ '\n'
    return RR

def tilt(R, direc = 'N'):
    if direc == 'N':
        R_st = np.maximum(R, 0)
        R_tilt = np.zeros_like(R)
        R_tilt[np.where(R==-1)] = -1
        for i in range(R.shape[1]):
            f_idx = np.concatenate([[-1],np.where(R[:,i]==-1)[0], [R.shape[1]]])
            for j in range(len(f_idx)-1):
                num_st = np.sum(R_st[(f_idx[j]+1):f_idx[j+1],i])
                R_tilt[(f_idx[j]+1):(f_idx[j]+1+num_st),i] = 1
    elif direc == 'S':
        R_tilt = np.flipud(tilt(np.flipud(R)))
    elif direc == 'E':
        R_tilt = np.rot90(tilt(np.rot90(R,k=1)),k=-1)
    elif direc == 'W':
        R_tilt = np.rot90(tilt(np.rot90(R,k=-1)),k=1)
    return R_tilt

def calculate_load(R, direc='N'):
    if direc == 'N':
        res = 0
        for i in range(R.shape[0]):
            num_st = np.sum(R[i,:]==1)
            res += num_st *(R.shape[0]-i)
        return res
    
def cycle(R):
    R_tilt=R.copy()
    for direc in ['N', 'W', 'S', 'E']:
        R_tilt=tilt(R_tilt, direc=direc)
    return R_tilt
     
#%% part one  
print('Part one: ' + str(calculate_load(tilt(R))))   
#%% part two
hist = [R.copy()]
idx = 0
term = False
while not term:
    R = cycle(R)
    idx+=1
    print(calculate_load(R))
    for i,h in enumerate(hist):
        if np.allclose(h, R):
            term = True
            c_start = i
    if not term:
        hist.append(R.copy())
    

c_len = len(hist) - c_start
target = 1000000000 - c_start
res = calculate_load(hist[(target%c_len) + c_start])
print('Part two: ' + str(res))
