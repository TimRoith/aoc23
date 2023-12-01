import regex as re

nums = {'zero':0, '0':0,
        'one':1, '1':1,
        'two':2, '2':2,
        'three':3, '3':3,
        'four':4, '4':4,
        'five':5, '5':5,
        'six':6, '6':6,
        'seven':7, '7':7,
        'eight':8, '8':8,
        'nine':9, '9':9}

nums_rev = {}
for num in nums.keys():
    nums_rev[num[::-1]] = nums[num]

p = re.compile(r"\L<words>", words=nums.keys())
p_rev = re.compile(r"\L<words>", words=nums_rev.keys())
#%%
with open('input.txt') as file:
    lines = [line.rstrip() for line in file]
    
s=0
for line in lines:
    r = p.search(line)[0]
    r = nums[r] * 10
    rr = p_rev.search(line[::-1])[0]
    rr = nums_rev[rr]
    
    s += r + rr
    
print(10*'-')
print(s)
