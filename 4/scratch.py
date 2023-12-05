import numpy as np
#%%
with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
#%%
class Card:
    def __init__(self, line,):
        [G, R] = line.split(":")
        self.id = int(G.split(' ')[-1])
        [W, H] = R.split('|')
        W_idx = np.zeros((100,), dtype=bool)
        H_idx = np.zeros((100,), dtype=bool)
        W = [int(w) for w in W.split(' ') if w!='']
        W_idx[W] = True
        H = [int(h) for h in H.split(' ') if h!='']
        H_idx[H] = True
        
        wh = np.logical_and(W_idx, H_idx)
        self.wh_num = np.sum(wh)

        self.pow = int(2.**(self.wh_num-1))
        
#%% part 1
s = 0
for line in lines:
    s+= Card(line).pow
    
print('The result is: ' +str(s))

#%% part 2
num_cards = np.ones((len(lines),), dtype=int)
num_cards[0] = 1
for i, line in enumerate(lines):
    num = num_cards[i]
    c = Card(line)
    if c.wh_num > 0:
        num_cards[i+1:i+1+c.wh_num] += num
        
print('The result for part two is: ' + str(np.sum(num_cards)))