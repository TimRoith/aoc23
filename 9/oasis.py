import numpy as np
class pascal:
    def __init__(self, x):
        self.x = x
        self.table = self.cl(x)
        self.l = len(self.table)
        
    def cl(self, x):
        r = [x]
        if np.sum(np.abs(x)) == 0:
            return [x]
        else:
            return r + self.cl(x[1:] - x[:-1])
        
    def extra(self,):
        self.table[-1] = np.append(self.table[-1], self.table[-1][-1])
        for i in range(2, self.l + 1):
            s = self.table[-i][-1] + self.table[-i+1][-1]
            self.table[-i] = np.append(self.table[-i], s)
            
    def extra_rev(self,):
        self.table[-1] = np.insert(self.table[-1], 0, self.table[-1][0])
        for i in range(2, self.l + 1):
            s = self.table[-i][0] - self.table[-i+1][0]
            self.table[-i] = np.insert(self.table[-i],0, s)
            
#%%
p1_sum = 0
p2_sum = 0
with open('input.txt') as file:
    for line in file:
        line = line.strip().split(' ')
        x = np.array([int(l) for l in line])
        p = pascal(x)
        p.extra()
        p.extra_rev()
        p1_sum += p.table[0][-1]
        p2_sum += p.table[0][0]
        
print('Part One: ' +str(p1_sum))
print('Part two: ' + str(p2_sum))