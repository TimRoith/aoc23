#%%
import numpy as np

cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
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
        return self.cards.max() == 5
    def is_four(self,):
        return self.cards.max() == 4
    def is_full(self,):
        return (3 in self.cards) and (2 in self.cards)
    def is_three(self,):
        return self.cards.max() == 3
    def two_pair(self,):
        return len(np.where(self.cards==2)[0]) == 2
    def one_pair(self,):
        return 2 in self.cards
    
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