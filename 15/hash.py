A = []
with open('input.txt') as file:
    for line in file:
        line = line.strip()
        if len(line)>0:
            A+= line.split(',')


inp = 'HASH'
def value(inp):
    val = 0
    for s in inp:
        val+=ord(s)
        val*=17
        val=val%256
    
    return val

res = 0
for a in A:
    res += value(a)
    
print(res)

#%% part two
from collections import OrderedDict

boxes = {}

class Box:
    def __init__(self, lb, fl):
        self.lenses = OrderedDict()
        self.lenses[lb] = fl
        
    def insert(self, lb, fl):
        self.lenses[lb] = fl
    def delete(self, lb):
        if lb in self.lenses.keys():
            self.lenses.pop(lb)
    def __str__(self,):
        return str(self.lenses)
    def __repr__(self,):
        return str(self.lenses)
        
for a in A:
    s = a[-1]
    if s == '-':
        lb = a[:-1]
    else:
        fl = a[-1]
        s = '='
        lb = a[:-2]
    idx = value(lb)
    if s == '=':
        if idx in boxes.keys():
            boxes[idx].insert(lb, fl)
        else:
            boxes[idx] = Box(lb, fl)
    else:
        if idx in boxes.keys():
            boxes[idx].delete(lb)
            

res = 0    
for b in boxes.keys():
    num = int(b) + 1
    for i,l in enumerate(boxes[b].lenses):
        add = num * (i+1) *  int(boxes[b].lenses[l])
        res += add
        print(add)
    
        
print(res)