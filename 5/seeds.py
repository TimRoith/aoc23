import bisect
 
#%%
class cat_map:
    def __init__(self, source_cat=None, dest_cat=None):
        self.lens = []
        self.source_idx  = []
        self.dest_idx = []
        self.source_cat = source_cat
        self.dest_cat = dest_cat
        
    def __getitem__(self, idx):
        if idx < min(self.source_idx):
            return idx
        else:
            ins_idx = self.get_ins_idx(idx)
            source_idx = self.source_idx[ins_idx-1]
            off = idx - source_idx
            if off < self.lens[ins_idx-1]:
                return self.dest_idx[ins_idx-1] + off
            else:
                return idx
    
    def add_line(self, line):
        [d, s, l] = line.split(' ')
        ins_idx = self.get_ins_idx(int(s))
        
        self.lens.insert(ins_idx, int(l))
        self.source_idx.insert(ins_idx, int(s))
        self.dest_idx.insert(ins_idx, int(d))
        
    def get_ins_idx(self, idx):
        return bisect.bisect(self.source_idx, idx) 
        
    def map_range(self, a, b):
        rs = []
        low_source = a

        if a == b:
            return [(self[a], self[a])]
        elif a > b:
            return []
        elif a >= self.source_idx[-1] + self.lens[-1]:
            return [(a,b)]
        elif a < min(self.source_idx):
            low_source = min(min(self.source_idx)-1, b)
            rs.append((a, low_source))
            return rs + self.map_range(low_source+1, b)
            
        
        ins_idx = self.get_ins_idx(low_source)-1
        source = self.source_idx[ins_idx]
        idx = ins_idx
        i = 0
        if low_source >= source + self.lens[idx]:
            if ins_idx >= len(self.lens) - 1:
                rs.append((low_source, b))
                low_source = b
            else:
                idx+=1
                source = self.source_idx[idx]
                d_high = min(b, source - 1)
                rs.append((low_source, d_high))
                low_source = d_high + 1
        else:
            len_want = b - low_source
            low_off = low_source - source
            len_allow = min(len_want, self.lens[idx]-low_off-1)
            d_low = self[low_source]
            d_high = self[low_source + len_allow]
            rs.append((d_low, d_high))
            #update
            low_source += len_allow + 1
            rs += self.map_range(low_source, b)
            
        return rs
    
    def map_ranges(self, rs):
        rs_out = []
        for r in rs:
            rr = self.map_range(r[0], r[1])
            rs_out += rr
        return rs_out
        
#%%
cat_maps = {}
source = ''
seed_line = True

with open('input.txt') as file:
    next_start = False
    add_lines = False
    for line in file:
        if seed_line:
            seed_line = False
            seeds = line.rstrip().split(' ')
            seeds = [int(seed) for seed in seeds[1:]]
        if line in ['\n', '\r\n']:   
            next_start = True
            add_lines = False
            continue
            
        elif add_lines:
            L = line.rstrip()
            cat_maps[source].add_line(line)
            
        elif next_start:
            next_start = False
            add_lines = True
            L = line.rstrip()
            [m, _] = L.split(' ')
            [source, _, dest] = m.split('-')
            cat_maps[source] = cat_map(source_cat=source, dest_cat=dest)
            
#%%
seed_loc = []

for seed in seeds:
    cat = 'seed'
    idx = seed
    while cat != 'location':
        idx = cat_maps[cat][idx]
        cat = cat_maps[cat].dest_cat
    seed_loc.append(idx)
    print('Seed: ' +str(seed) + ', Loc: ' +str(idx))
    
print('Min Loc is: ' + str(min(seed_loc)))
            
#%% part 2
i = 0
all_min = int(1e12)
while i < len(seeds)-1:
    cat = 'seed'
    idx = seeds[i]
    off = seeds[i+1]
    rs = [(idx, idx+off)]
    while cat != 'location':
        rs = cat_maps[cat].map_ranges(rs)
        cat = cat_maps[cat].dest_cat
    
    print('Seed ' + str(seeds[i]) + ' rs:')
    print(rs)
    i+=2  
    loc_min = int(1e12)
    for r in rs:
        loc_min = min(loc_min, r[0])
    all_min = min(all_min, loc_min)
    
print('All min: ' +str(all_min))

        