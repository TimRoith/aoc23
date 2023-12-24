Jobs = []

class module:
    def __init__(self, dest, name):
        self.dest = dest
        self.name = name
    def base_state(self):
        return True
    def reset(self,):
        pass

class broadcaster(module):
    def __init__(self, dest, name):
        super().__init__(dest,name)
        
    def receive(self, s, name):
        for d in self.dest:
            Jobs.append((s, self.name, d))
    
class flipflop(module):
    def __init__(self, dest, name):
        super().__init__(dest,name)
        self.state = 0
    
    def receive(self, s, name):
        if s=='low':
            if self.state == 0:
                self.state = 1
                p = 'high'
            else:
                self.state = 0
                p = 'low'
            for d in self.dest:
                Jobs.append((p, self.name, d))
    def reset(self,):
        self.state = 0
    def base_state(self):
        return self.state == 0
                
    def __repr__(self,):
        return 'FlipFlop, Dest: ' + str(self.dest)
    
class conjunction(module):
    def __init__(self, dest, name):
        super().__init__(dest, name)
        self.mem = {}
        
    def receive(self, s, name):
        v = {'low':False, 'high':True}[s]
        self.mem[name] = v
        r = 'high'
        if all(self.mem.values()):
            r = 'low'
        for d in self.dest:
            Jobs.append((r, self.name, d))
    def base_state(self):
        return ~any(self.mem.values()) 
    def reset(self,):
        for n in self.mem.keys():
            self.mem[n] = False
            
    def __repr__(self,):
        return 'Conjunction, Dest: ' +\
                str(self.dest) + ' Input: ' + str(self.mem)
            
        
#%% 
M = {}
with open('input.txt') as file:
    for line in file:
        line = line.strip()
        [T,F] = line.split(' -> ')
        if T == 'broadcaster':
            M['broadcaster'] = broadcaster(F.split(', '), 'Central')
        elif T[0] == '%':
            M[T[1:]] = flipflop(F.split(', '), T[1:])
        elif T[0] == '&':
            M[T[1:]] = conjunction(F.split(', '), T[1:])
            
for m in M.keys():
    for d in M[m].dest:
        if d in M.keys() and hasattr(M[d], 'mem'):
            M[d].mem[m] = False
            
#%%
term = False
ctrs = []
l = 0
h = 0
while (not term) and len(ctrs) < 1000:
    M['broadcaster'].receive('low', 'Center')
    ctr = {'low':1, 'high':0}
    #print(8*'-')
    while len(Jobs) > 0:
        J = Jobs.pop(0)
        #print(J)
        if J[2] in M.keys():
            M[J[2]].receive(J[0], J[1])
        ctr[J[0]] += 1
    term = True
    for m in M.keys():
        if not M[m].base_state():
            term = False
    ctrs.append(ctr)
    l+=ctr['low']
    h+=ctr['high']
  
pushes = 1000
reps = pushes//len(ctrs)
rest = pushes%len(ctrs)
l*=reps
h*=reps
for i in range(rest):
    l += ctrs[i]['low']
    h += ctrs[i]['high']

print('Part one: ' + str(l*h))
#%% part two
from math import lcm
C = {}
for m in M.keys():
    M[m].reset()
    if hasattr(M[m], 'mem'):
        C[m] = -1

num = 1
while num < 5000:
    M['broadcaster'].receive('low', 'Center')
    while len(Jobs) > 0:
        J = Jobs.pop(0)
        if J[2] in M.keys():
            M[J[2]].receive(J[0], J[1])
            if J[1] in C.keys() and J[0] == 'low':
                if C[J[1]] == -1:
                    C[J[1]] = num
    num += 1
            
cc = [C[c] for c in C.keys() if C[c] >2]
print('Part two: ' + str(lcm(*cc)))
    
