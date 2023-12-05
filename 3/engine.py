import regex as re
import numpy as np
with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
  
N = len(lines)
M = len(lines[0])
symbol_idx = np.zeros((M, N))

p = re.compile("[^.\d]")
pp = re.compile("\d+")

for n, line in enumerate(lines):
    for m in p.finditer(line):
        idx = m.span()[0]
        symbol_idx[n, idx] = 1
#%%
s = 0
for n, line in enumerate(lines):
    for m in pp.finditer(line):
        sp = m.span()
        idx0 = max(sp[0]-1, 0)
        idx1 = min(sp[1]+1, M)
        
        nmin = max(n-1, 0)
        nmax = min(n+2, N)
        symb_flag = np.sum(symbol_idx[nmin:nmax, :][:,idx0:idx1])
        if symb_flag > 0:
            s+= int(m[0])
        else:
            print(m[0])
            
#%%
print('the result is: '+str(s))
