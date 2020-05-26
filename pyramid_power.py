import Cards
import random
import copy
import sys

class Field():
    def __init__(self, **kwargs):
        self.TRANK = 7
        self.MAXPASS = 3
        self.reset()

    def reset( self ):
        self.passcount = 0
        self.seq = []
        self.field = []
        for n in range( self.TRANK ):
            self.field.append( [0]*(n*2+1) )

    def rank(self):
        return self.TRANK

    def get(self):
        return self.field

    def checkX(self, y, x, v ):
        cl = copy.copy(self.field[y])
        if self.TRANK -1 == y:
            if x < (self.TRANK*2-1)-(14 - v)*4:
                return False
            if v * 4 <= x :
                return False
            if v in cl:
                if x ==0:
                    if cl[x+1]!=v:
                        return False
                if x == len(self.field[y])-1:
                    if cl[x-1]!=v:
                        return False
                if cl[x-1]!=v and cl[x+1]!=v:
                    return False
                
        cl[x] = v
        ov = 0
        for c in cl:
            if c !=0:
                if ov > c:
                    return False
                ov = c
        return True

    def checkY(self, y, x, v ):
        if y == self.TRANK -1:
            return True
        if self.field[y+1][x+1]==0:
            return False
        if self.field[y+1][x+1] < v:
            return False
        return True

    def check(self,y, x, v):
        eflg = False
        if y==4 and x==8 and v==12:
            eflg=False
        if self.field[y][x]!=0:
            return False
        if self.checkY(y, x, v):
            if self.checkX( y, x, v ):
                if eflg:
                    print( "check true" )    
                return True
        if eflg:
             print( "check false" )    
        return False

    def setField(self, y, x, v ):
        if self.check( y, x, v ):
            self.put( y, x, v )

    def put(self, y, x, v ):
        if y < 0:
            self.passcount = self.passcount + 1
        else:
            self.field[y][x] = v
        self.seq.append((y,x,v))

    def pop(self):
        lh = self.seq.pop()
        if lh[0] < 0:
            self.passcount = self.passcount - 1
        else:
            self.field[lh[0]][lh[1]] = 0
        return lh

    def dump(self):
        print( "seq ", len(self.seq), self.seq )
        for y in range(0, self.TRANK):
            line = ""
            for n in range(self.TRANK - y):
                line = line + "   "
            for x in self.field[y]:
                line = line + "{:3d}".format(x)
            print( line )
        print( "passcount ", self.passcount )

    def isclear(self):
        for y in range(0, self.TRANK):
            for x in range(len(self.field[y])):
                if self.field[y][x] == 0:
                    return False
        return True

    def getCandidate(self, v ):
        eflg=False
        cdt = []
        for y in range(self.TRANK):
            for x in range( 2*y + 1 ):
                if field.check( y, x, v ):
                    if y==4 and x==8 and v==12:
                        eflg=False
                    cdt.append( (y, x) )
        if len(cdt)==0 and self.MAXPASS > self.passcount:
            cdt.append( (-1, -1) )
        if eflg :
            print( v, cdt, self.field[4] )
        return cdt

    def getSeq(self):
        return self.seq

    def setSeq(self, seq):
        self.seq = seq
        for y in range(self.TRANK):
            for x in range( 2*y + 1 ):
                self.field[y][x] = 0
        for c in seq:
            print(c, c[0], c[1], c[2])
            if c[0] >= 0:
                self.field[c[0]][c[1]] = c[2]
        return len(seq)

        

def backtruck():
    lh = field.pop()
    ch = field.getCandidate(lh[2])
    for h in range( len(ch)):
        if ch[h][0]==lh[0] and ch[h][1]==lh[1]:
            if h+1 < len(ch):
                print( "backtruck", ch, lh, "->", ch[h+1], lh[2] )
                return ch[h+1]
    return [-2, -2, -2]

cards = Cards.create()

#cards.setCard([7, 31, 18, 12, 47, 11, 10, 13, 25, 4, 5, 45, 36, 2, 21, 38, 35, 27, 15, 17, 6, 48, 43,
#               14, 33, 51, 22, 44, 50, 24, 32, 19, 49, 37, 26, 8, 3, 42, 9, 0, 16, 29, 46, 39, 20, 30, 1, 23, 41, 40, 34, 28])

field = Field()
"""
sn = field.setSeq([(4, 0, 2), (4, 2, 4), (4, 4, 10), (3, 1, 4), (4, 6, 12), (2, 0, 3), (4, 1, 3), (4, 3, 10),
                   (3, 2, 7), (3, 0, 2), (-1, -1, 2), (3, 5, 12), (2, 4, 10), (-1, -1, 1), (2, 1, 6),
                   (4, 5, 11), (3, 3, 9), (2, 2, 7), (1, 0, 4), (1, 1, 5), (0, 0, 2), (4, 7, 13), (3, 4, 11),
                   (-1, -1, 4), (2, 3, 9)
                   ,(4, 8, 12)
                   , (1, 2, 6), (3, 6, 12), (-1, -1, 2)
                   ])
print(sn)
cards.setPos(sn)
"""
findit = 0
for t in range( 100 ):
    print( "try ", t )
    cards.reset()
    field.reset()

    try:
        for p in range(10000000):
            s, cv = cards.pop()
            ch = field.getCandidate(cv)
            cc = len( ch )

            if cc == 0:
                ins = True
                for n in range( 52 ):
                    cards.push()
                    lh = field.pop()
                    ch = field.getCandidate(lh[2])
                    ci = -1
                    for p in ch:
                        ci = ci + 1
                        if p[0]==lh[0] and p[1]==lh[1]:
                            break

                    cc = 0
                    if ci+1 < len(ch):
                        cn = ch[ci+1]
                        cv = lh[2]
                        break
            else:
                cn = ch[0]

            field.put( cn[0], cn[1], cv )
            if field.isclear():
                findit = findit + 1
                print("rank", field.rank(), "clear!! ", p)
                break


        cdl = cards.getList()
        print( cdl )
        for n in range(len(cdl)):
            cdl[n] = int(cdl[n]/4)+1
        print( cdl )
        field.dump()
    except IndexError:
        print( "---------Exception")

print( findit )

"""
rank 5 clear!!  25106
[30, 44, 37, 47, 36, 29, 5, 32, 49, 28, 3, 34, 7, 21, 17, 51, 9, 45, 8, 42, 10, 40, 15, 35, 2, 24, 12, 23, 25, 18, 39, 41, 31, 13, 48, 19, 27, 22, 33, 11, 0, 46, 26, 50, 4, 16, 6, 1, 43, 14, 20, 38]
seq  27 [(4, 8, 13), (4, 2, 9), (4, 3, 10), (4, 4, 12), (4, 0, 2), (3, 2, 3), (2, 1, 2),
(4, 1, 3), (4, 6, 12), (3, 5, 11), (1, 0, 1), (2, 4, 9), (3, 0, 2), (3, 3, 6), (2, 2, 5),
(4, 7, 13), (1, 1, 3),
(4, 5, 9), (0, 0, 3), (3, 6, 11), (3, 1, 3), (-1, -1, 11), (-1, -1, 4), (3, 4, 9), (2, 0, 1), (2, 3, 7), (1, 2, 4)]
                 3
              1  3  4
           1  2  5  7  9
        2  3  3  6  9 11 11
     2  3  9 10 12  9 12 13 13
passcount  2

================ RESTART: C:/src/Kivy/Cards/pyramid_power.py ================
[9, 45, 12, 28, 17, 39, 34, 31, 51, 43, 13, 47, 15, 23, 10, 27, 41, 14, 7, 6, 5, 2, 3, 26, 36, 32, 35, 40, 4, 16, 19, 50, 49, 42, 33, 11, 46, 38, 25, 48, 21, 8, 30, 22, 0, 1, 29, 24, 44, 37, 20, 18]
[3, 12, 4, 8, 5, 10, 9, 8, 13, 11, 4, 12, 4, 6, 3, 7, 11, 4, 2, 2, 2, 1, 1, 7, 10, 9, 9, 11, 2, 5, 5, 13, 13, 11, 9, 3, 12, 10, 7, 13, 6, 3, 8, 6, 1, 1, 8, 7, 12, 10, 6, 5]
seq  23 [(4, 0, 3), (4, 6, 12), (4, 1, 4), (3, 5, 8), (2, 4, 5), (4, 4, 10), (4, 3, 9), (4, 2, 8), (4, 8, 13), (4, 5, 11), (3, 2, 4), (4, 7, 12), (3, 3, 4), (3, 4, 6), (2, 1, 3), (-1, -1, 7), (3, 6, 11), (2, 2, 4), (1, 1, 2), (1, 0, 2), (3, 1, 2), (0, 0, 1), (2, 0, 1)]
                 1
              2  2  0
           1  3  4  0  5
        0  2  4  4  6  8 11
     3  4  8  9 10 11 12 12 13
passcount  1
>>> 
================ RESTART: C:/src/Kivy/Cards/pyramid_power.py ================
[(2, 4)]
rank 6 clear!!  166194
[29, 16, 44, 0, 41, 26, 51, 46, 20, 12, 39, 25, 43, 5, 14, 30, 36, 8, 23, 45, 27, 22, 34, 28, 38, 48, 49, 47, 35, 17, 15, 11, 13, 1, 32, 3, 37, 19, 24, 9, 33, 6, 2, 10, 4, 42, 7, 18, 40, 31, 50, 21]
[8, 5, 12, 1, 11, 7, 13, 12, 6, 4, 10, 7, 11, 2, 4, 8, 10, 3, 6, 12, 7, 6, 9, 8, 10, 13, 13, 12, 9, 5, 4, 3, 4, 1, 9, 1, 10, 5, 7, 3, 9, 2, 1, 3, 2, 11, 2, 5, 11, 8, 13, 6]
seq  38 [(5, 1, 8), (4, 0, 5), (5, 4, 12), (5, 0, 1), (5, 2, 11), (4, 3, 7), (5, 8, 13), (5, 5, 12), (3, 2, 6), (2, 1, 4), (4, 7, 10), (4, 1, 7), (5, 3, 11), (1, 0, 2), (3, 0, 4), (4, 4, 8), (3, 6, 10), (-1, -1, 3), (3, 3, 6), (5, 6, 12), (4, 2, 7), (3, 1, 6), (4, 5, 9), (3, 4, 8), (-1, -1, 10), (5, 9, 13), (5, 10, 13), (5, 7, 12), (4, 6, 9), (2, 3, 5), (2, 2, 4), (1, 1, 3), (1, 2, 4), (0, 0, 1), (3, 5, 9), (2, 0, 1), (4, 8, 10), (2, 4, 5)]
                    1
                 2  3  4
              1  4  4  5  5
           4  6  6  6  8  9 10
        5  7  7  7  8  9  9 10 10
     1  8 11 11 12 12 12 12 13 13 13
passcount  2
>>> 
================ RESTART: C:/src/Kivy/Cards/pyramid_power.py ================
[34, 21, 13, 33, 40, 12, 32, 45, 4, 2, 47, 51, 41, 5, 31, 26, 23, 14, 19, 28, 25, 20, 38, 7, 6, 17, 22, 3, 10, 15, 9, 1, 18, 29, 8, 43, 37, 36, 27, 48, 49, 50, 39, 44, 42, 16, 0, 11, 35, 24, 46, 30]
[9, 6, 4, 9, 11, 4, 9, 12, 2, 1, 12, 13, 11, 2, 8, 7, 6, 4, 5, 8, 7, 6, 10, 2, 2, 5, 6, 1, 3, 4, 3, 1, 5, 8, 3, 11, 10, 10, 7, 13, 13, 13, 10, 12, 11, 5, 1, 3, 9, 7, 12, 8]
seq  26 [(5, 0, 9), (-1, -1, 6), (-1, -1, 4), (5, 2, 9), (5, 5, 11), (4, 4, 4), (5, 1, 9), (5, 6, 12), (3, 3, 2), (4, 0, 1), (5, 7, 12), (5, 9, 13), (5, 4, 11), (4, 1, 2), (4, 6, 8), (3, 5, 7), (4, 5, 6), (4, 3, 4), (2, 4, 5), (4, 8, 8), (-1, -1, 7), (3, 4, 6), (5, 3, 10), (4, 2, 2), (3, 0, 2), (2, 3, 5)]
                    0
                 0  0  0
              0  0  0  5  5
           2  0  0  2  6  7  0
        1  2  2  4  4  6  8  0  8
     9  9  9 10 11 11 12 12  0 13  0
passcount  3
>>>
================ RESTART: C:/src/Kivy/Cards/pyramid_power.py ================
try  0
[27, 50, 11, 48, 40, 19, 14, 3, 34, 21, 10, 24, 2, 22, 13, 9, 32, 1, 16, 5, 35, 33, 28, 45, 31, 4, 15, 0, 29, 17, 49, 30, 26, 20, 44, 6, 7, 42, 43, 23, 18, 37, 47, 38, 46, 39, 41, 8, 25, 36, 12, 51]
[7, 13, 3, 13, 11, 5, 4, 1, 9, 6, 3, 7, 1, 6, 4, 3, 9, 1, 5, 2, 9, 9, 8, 12, 8, 2, 4, 1, 8, 5, 13, 8, 7, 6, 12, 2, 2, 11, 11, 6, 5, 10, 12, 10, 12, 10, 11, 3, 7, 10, 4, 13]
seq  40 [(6, 1, 7), (6, 10, 13), (6, 0, 3), (6, 9, 13), (6, 7, 11), (5, 0, 5), (-1, -1, 4), (-1, -1, 1), (6, 5, 9), (5, 4, 6), (4, 3, 3), (6, 2, 7), (3, 2, 1), (5, 6, 6), (4, 5, 4), (3, 4, 3), (6, 3, 9), (2, 1, 1), (5, 2, 5), (2, 3, 2), (5, 8, 9), (6, 4, 9), (4, 7, 8), (6, 8, 12), (3, 6, 8), (1, 2, 2), (-1, -1, 4), (1, 0, 1), (5, 7, 8), (5, 1, 5), (6, 11, 13), (4, 6, 8), (3, 5, 7), (5, 3, 6), (5, 9, 12), (4, 0, 2), (2, 4, 2), (4, 8, 11), (6, 6, 11), (5, 5, 6)]
                       0
                    1  0  2
                 0  1  0  2  2
              0  0  1  0  3  7  8
           2  0  0  3  0  4  8  8 11
        5  5  5  6  6  6  6  8  9 12  0
     3  7  7  9  9  9 11 11 12 13 13 13  0
passcount  3
"""
