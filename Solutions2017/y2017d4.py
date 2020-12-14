# from AOC_Lib.name import *


from typing import Counter


class BreakContinue(Exception):
    pass

def y2017d4(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d4.txt"
    print("2017 day 4:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    

    # for multi line inputs
    Part_1_Answer = 0
    Part_2_Answer = 0
    for line in lineList:
        s = line.split(" ")
        wordSet = set()

        try:
            for word in s:
                if word in wordSet:
                    raise BreakContinue()
                wordSet.add(word)
            Part_1_Answer += 1

            # need to run part 2 only on those that pass part 1
            counterSet = []
            for word in s:
                c = Counter(word)
                if c in counterSet:
                    raise BreakContinue()
                counterSet.append(c)
            Part_2_Answer += 1
        except BreakContinue:
            continue
                

    return (Part_1_Answer, Part_2_Answer)