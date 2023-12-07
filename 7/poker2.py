#%%
import numpy as np

cards = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
card_dict = {c:i for i, c in enumerate(cards)}
#%%
class hand:
    def __init__(self, line):
        [H, B] = line.split(' ')
        self.hand = H
        self.bid = int(B)
        
        self.cards = np.zeros(len(cards), dtype=int)
        self.score = 0
        for i,h in enumerate(self.hand):
            self.cards[card_dict[h]] +=1
            self.score += (card_dict[h]+1) * (10**-(2*i))
        self.eval_score()
        
    def is_five(self,):
        s = self.cards[1:].max() + self.cards[0]
        if s == 5:
            return True
    def is_four(self,):
        s = self.cards[1:].max() + self.cards[0]
        if s == 4:
            return True
    def is_full(self,):
        res = False
        if (3 in self.cards):
            if (2 in self.cards) or (self.cards[0] == 1):
                res = True
        elif len(np.where(self.cards[1:]==2)[0]) == 2:
            if self.cards[0] == 1:
                res = True
        elif len(np.where(self.cards[1:]==2)[0]) == 1:
            if self.cards[0] == 2:
                res = True

        return res
        
    def is_three(self,):
        s = self.cards[1:].max() + self.cards[0]
        if s == 3:
            return True
    def two_pair(self,):
        res = False
        if len(np.where(self.cards==2)[0]) == 2:
            res = True
        
        return res
    def one_pair(self,):
        return 2 in self.cards or self.cards[0] == 1
    
    def eval_score(self,):
        if self.is_five():
            self.score += 700
        elif self.is_four():
            self.score += 600
        elif self.is_full():
            self.score += 500
        elif self.is_three():
            self.score += 400
        elif self.two_pair():
            self.score += 300
        elif self.one_pair():
            self.score += 200
        else:
            self.score += 100
        
#%%
hands = []
with open('input.txt') as file:
    for line in file:
        h = hand(line)
        hands.append(h)

hands.sort(key=lambda x: x.score)
bid_score = 0
for i, h in enumerate(hands):
    bid_score += (i+1) * h.bid

print('The result is ' + str(bid_score))