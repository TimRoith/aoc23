node_dict = {}

ins_line = True
with open('input.txt') as file:
    inst = file.readline().strip('\n')
    for line in file:
        line = line.rstrip()
        if len(line) > 0:
            N,D = line.split(' = ')
            L = D[1:4]
            R = D[-4:-1]
            node_dict[N] = (L,R)
            
#%% part one
N = 'AAA'
idx = 0
num_steps = 0
while N != 'ZZZ':
    idx = idx%len(inst)
    D = 0 if inst[idx]=='L' else 1
    
    N = node_dict[N][D]
    idx+=1
    num_steps+=1
    
print('Number of steps: ' + str(num_steps))

#%% part two
nodes = [N for N in list(node_dict.keys()) if N[-1]=='A']
cycles = []
cycles_start = []
for N in nodes:
    term = False
    idx = 0
    num_steps = 0
    cycle = {}
    while not term:
        cycle[(idx,N)] = num_steps
        idx = idx%len(inst)
        D = 0 if inst[idx]=='L' else 1
        N = node_dict[N][D]
        idx+=1
        num_steps+=1
        
        if (idx, N) in cycle:
            term = True
            cycles_start.append((idx,N))
            
    cycles.append(cycle)
 
#%%
class CCycle:
    def __init__(self, c, cs):
        self.c = c
        self.z = []
        for k in self.c.keys():
            if k[1][-1] == 'Z':
                self.z.append(c[k])
                
        self.lens = len(self.c) - cs[0]
        
    def nsteps(self, nz):
        return [self.lens * nz + z for z in self.z]
    
    def nz_possible(self, nstep):
        res = False
        z_true = None
        for z in self.z:
            if (nstep - z)%self.lens == 0:
                res = True
                z_true = z
        return res, z_true
        
                
cs = []
c_min = 1e12
for i in range(len(cycles)):
    CC = CCycle(cycles[i], cycles_start[i])
    cs.append(CC)
    if CC.lens < c_min:
        c_min = CC.lens
#%%
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
    
def extended_euclidean(a, b):
  if b == 0:
    gcd, s, t = a, 1, 0
    return (gcd, s, t)
  else:
    s2, t2, s1, t1 = 1, 0, 0, 1
    while b > 0:
      q= a // b
      r, s, t = (a - b * q),(s2 - q * s1),( t2 - q * t1)
      a,b,s2,t2,s1,t1=b,r,s1,t1,s,t
    gcd,s,t=a,s2,t2
    return (gcd,s,t)

class bs:
    def __init__(self,c, cc):
        self.a = c.lens
        self.b = -cc.lens
        c = -c.z[0]

        g, af, bf = extended_euclidean(self.a, -self.b)
        self.g = g
        r = c/g
        self.x = r*af
        self.y = -r*bf
        self.sx = -self.b/self.g
        
    def ret(self, r):
        xx = self.x - r * self.b/self.g
        yy = self.y + r * self.a/self.g
        return xx, yy

bbs = []
s_max = 0
for c in cs:
    bbs.append(bs(cs[0], c))
    if bbs[-1].sx > s_max:
        s_max = bbs[-1].sx
        bmax = bbs[-1]
found = False
#%%
m = int(1e8)
for r in range(m):
    b = bmax
    xx,yy = b.ret(r)
    res = cs[0].nsteps(xx)[0]
    #print(res)
    s = 0
    found_loc = True
    for i,cc in enumerate(cs):
        if not cc.nz_possible(res)[0]:
            found_loc = False
            break
    if found_loc and res >0.:
        print(res)
        found = True
        
    if (10*r)%m==0:
        print(r)
    if found:
        break
        

    
    



