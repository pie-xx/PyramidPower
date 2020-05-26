import random
import copy

def create():
	return Cards()

class Cards():
    def __init__(self, **kwargs):
        self.cards = list(range(52))
        self.reset()

    def pop(self):
        self.picp = self.picp + 1
        v = self.cards[self.picp-1]
        return v % 4, int(v / 4)+1

    def push(self):
        self.picp = self.picp - 1

    def getList(self):
        return self.cards

    def getPos(self):
        return self.picp

    def setCard(self, cards):
        self.cards = copy.copy(cards)
        
    def setPos(self, p ):
        self.pipc=p

    def reset(self):
        self.cards = list(range(52))
        random.shuffle( self.cards )
        self.picp = 0
