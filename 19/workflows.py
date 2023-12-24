import re

#%%
class workflow:
    def __init__(self, line):
        self.line = line
        self.vars = []
        self.vals = []
        self.res  = []
        self.conds= []
        G = line.split(',')
        for w in G[:-1]:
            C, R = w.split(':')
            self.vars.append(C[0])
            self.vals.append(int(C[2:]))
            self.res.append(R)
            if C[1] == '<':
                self.conds.append('__lt__')
            else:
                self.conds.append('__gt__')
                
        self.els = G[-1]
        
    def check(self, part):
        for i,var in enumerate(self.vars):
            if getattr(getattr(part, var),self.conds[i])(self.vals[i]):
                if self.res[i] in ['A','R']:
                    return self.res[i]
                else:
                    return wfs[self.res[i]].check(part)
        else:
            if self.els in ['R','A']:
                return self.els
            else:
                return wfs[self.els].check(part)
    def check_range(self,prange, i):
        for k in prange.keys():
            if (prange[k][1] - prange[k][0]) < 0:
                print(5)
                return 0
        if i < len(self.vals):                
            mi = prange[self.vars[i]][0]
            ma = prange[self.vars[i]][1]
            prange_new = prange.copy()
            asum = 0
            if self.conds[i] == '__lt__':
                prange[self.vars[i]] = (mi, min(self.vals[i]-1, ma))
                prange_new[self.vars[i]] = (self.vals[i], ma)
            else:
                prange[self.vars[i]] = (max(self.vals[i]+1, mi), ma)                 
                prange_new[self.vars[i]] = (mi, self.vals[i])
            
            asum += self.check_range(prange_new, i+1)
            if self.res[i] == 'A':
                f = 1
                for k in prange.keys():
                    f *= (prange[k][1] - prange[k][0]+1)
                asum += max(f,0)
            elif self.res[i] != 'R':
                asum += wfs[self.res[i]].check_range(prange, 0)
            return asum
        else:
            if self.els == 'A':
                f = 1
                for k in prange.keys():
                    f *= (prange[k][1] - prange[k][0]+1)
                return f
            elif self.els != 'R':
                return wfs[self.els].check_range(prange, 0)
            else:
                return 0
                
        
    def __repr__(self):
        return self.line
    

class part:
    def __init__(self, line):
        self.line = line
        self.allsum = 0
        for L in line.split(','):
            n,v = L.split('=')
            setattr(self, n, int(v))
            self.allsum += int(v)
            
    def __repr__(self,):
        return 'Part: ' + self.line
#%%
wf = True
wfs = {}
parts = []
with open('input.txt') as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            wf = False
        elif wf:
            line=line.replace('}', '{')
            [N,w,_] = line.split('{')
            wfs[N] = workflow(w)
        else:
            parts.append(part(line[1:-1]))
#%%
res = 0
for p in parts:
    if wfs['in'].check(p) == 'A':
        res += p.allsum
        
print('Part one: ' +str(res))
            
#%% part two
res = wfs['in'].check_range({'x':(1,4000), 'm':(1,4000), 
                             'a':(1,4000),'s':(1,4000)},0)
print('Part two: ' +str(res))           

