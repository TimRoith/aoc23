import numpy as np
colors = {'red':0, 'green':1, 'blue':2}
#%%
class Game:
    def __init__(self, line, max_takes = None):
        if max_takes is None:
            max_takes = [np.inf,np.inf,np.inf]
        self.max_takes = max_takes
        self.mt = np.zeros((3,))
            
        [G, R] = line.split(":")
        self.id = int(G.split(' ')[-1])
        R = R.split(';')
        self.takes = []
        for r in R:
            g = np.zeros((3,), dtype=int)
            for rr in r.split(','):
                rrs = rr.split(' ')
                n = rrs[-2]
                c = rrs[-1]
                g[colors[c]] = int(n)
            self.takes.append(g)
            self.mt = np.maximum(g, self.mt)
           
        self.valid = np.all(self.mt <= self.max_takes)
        self.power = np.prod(self.mt)
        
#%%
with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
   
val_sum = 0
pow_sum = 0
max_takes = np.array([12,13,14])
for line in lines:
    G_val = Game(line, max_takes=max_takes)
    if G_val.valid:
        val_sum+= G_val.id
        
    G_pow = Game(line)
    pow_sum += G_pow.power
    
        
print('The valid result is: ' + str(val_sum))
print('The power result is: ' + str(pow_sum))
        