# from AOC_Lib.name import *

from functools import total_ordering
#TODO - move this into the lib and update 2016d4 with it too
@total_ordering
class Comparable():
    def __init__(self, t) -> None:
        self.a = t[0]
        self.b = t[1]
    
    def __eq__(self, o: object) -> bool:
        return self.a == o.a and self.b == o.b
    
    def __lt__(self, o: object) -> bool:
        if self.b < o.b:
            return True
        if self.b == o.b and self.a < o.a:
            return True
        return False

    def __str__(self) -> str:
        return f"({self.a}, {self.b})"

    def __repr__(self) -> str:
        return str(self)


# sample variant for reading data from an input file, line by line
def y2016d6(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d6.txt"
    print("2016 day 6:")

    Part_1_Answer = None
    Part_2_Answer = None

    colDicts = [None]*8
    for i in range(8):
        colDicts[i] = {}

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            assert(len(line) == 8)
            
            for i in range(8):
                c = line[i]
                if c not in colDicts[i]:
                    colDicts[i][c] = 1
                else:
                    colDicts[i][c] += 1
        
        p1Partial = ""
        p2Partial = ""

        for i in range(8):
            l = list(map(lambda x: Comparable(x), colDicts[i].items()))
            l.sort()
            p1Partial += l[-1].a
            p2Partial += l[0].a

        Part_1_Answer = p1Partial
        Part_2_Answer = p2Partial
        
    return (Part_1_Answer, Part_2_Answer)