import regex as re
import numpy as np
with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
  
N = len(lines)
M = len(lines[0])
symbol_idx = np.zeros((M, N))

p = re.compile("[*]")
pp = re.compile("\d+")

#%%
number_idx = -1 * np.ones((N,M), dtype=int)
numbers = []
num_idx = 0
for n, line in enumerate(lines):
    for m in pp.finditer(line):
        idx = m.span()
        number_idx[n, idx[0]:idx[1]] = num_idx
        numbers.append(int(m[0]))
        num_idx+=1
    
numbers = np.array(numbers)
s = 0
for n, line in enumerate(lines):
    for m in p.finditer(line):
        bidx = m.span()[0]
        
        nmin = max(n-1, 0)
        nmax = min(n+2, N)
        
        idx0 = max(bidx-1, 0)
        idx1 = min(bidx+2, M)
        
        loc_array = number_idx[nmin:nmax,:][:,idx0:idx1]
        loc_nums = np.unique(loc_array)
        nmo = np.where(loc_nums!=-1)[0]
        loc_nums = loc_nums[nmo]
        
        if len(loc_nums) == 2:
            s += np.prod(numbers[loc_nums])
            
print('The result is: ' +str(s))
        