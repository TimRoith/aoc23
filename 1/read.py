import re
with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
    
s = 0
for line in lines:
    r = re.search(r'\d+', line).group()[0]
    rr = re.search(r'\d+', line[::-1]).group()[0]
    
    s += 10*int(r)+ int(rr)
    
print(10*'-')
print('Result: ' + str(s))
    