# from AOC_Lib.name import *

class DLLNode():
    def __init__(self, value, prev, next) -> None:
        if value is None:
            self.v = 0
            self.p = self
            self.n = self
            return

        self.v = value
        self.p = prev
        prev.n = self
        self.n = next
        next.p = self

def y2017d17(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d17.txt"
    print("2017 day 17:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    stepCount = int(lineList[-1])
    
    myPos = DLLNode(None, None, None) # create the empty list

    i = 1
    while True:
        for _ in range(stepCount):
            myPos = myPos.n
        myPos.n = DLLNode(i, myPos, myPos.n)
        myPos = myPos.n
        if i == 2017:
            Part_1_Answer = myPos.n.v
            break
        i += 1

    # part2
    index = 0
    valueIn1 = None
    for i in range(1, 50000000+1):
        newIndex = (index + stepCount) % i
        # print(newIndex)
        if newIndex == 0:
            valueIn1 = i
            # print(valueIn1)
        index = (newIndex + 1)
    Part_2_Answer = valueIn1

    return (Part_1_Answer, Part_2_Answer)