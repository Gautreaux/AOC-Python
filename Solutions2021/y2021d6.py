# from AOC_Lib.name import *

from collections import Counter, defaultdict

def y2021d6(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d6.txt"
    print("2021 day 6:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    lifetime = Counter(map(int, lineList[0].split(",")))
    # lifetime = Counter(map(int, "3,4,3,1,2".split(",")))

    for day in range(10000):
        next_state = defaultdict(int)

        for lf, number in lifetime.items():
            if lf == 0:
                next_state[8] += number
                next_state[6] += number
            else:
                next_state[lf-1] += number

        lifetime = next_state

        if day == 79:
            Part_1_Answer = sum(lifetime.values())
        elif day == 255:
            Part_2_Answer = sum(lifetime.values())
            break

    return (Part_1_Answer, Part_2_Answer)