import numpy as np

#%%
class boat_race:
    def __init__(self, T, record):
        self.T = T
        self.record = record

    def distance(self, t):
        return (self.T - t) * t
    
    def break_record(self):
        br = []
        for t in range(0, self.T + 1):
            if self.distance(t) > self.record:
                br.append(t)
        return br
    
    def error_margin(self):
        return len(self.break_record())
#%%
Times = []
Records = []
with open('input_ex.txt') as f:
    for i, line in enumerate(f):
        line = line.strip()
        I = line.split(' ')
        if I[0][:-1] == 'Time':
            for t in I[1:]:
                if len(t) > 0:
                    Times.append(int(t))
        else:
            for r in I[1:]:
                if len(r) > 0:
                    Records.append(int(r))

#%%
res = 1
for t, r in zip(Times, Records):
    e = boat_race(t, r).error_margin()
    print(e)
    res *= e

print('The result is: ' + str(res))

#%% part 2
T = ''
for t in Times:
    T += str(t)
T = int(T)
R = ''
for r in Records:
    R += str(r)
R = int(R)
#%%
br = boat_race(T, R)
e = br.error_margin()
print('The result is: ' + str(e))