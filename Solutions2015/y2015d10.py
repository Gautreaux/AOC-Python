# from AOC_Lib.name import *


import itertools
from typing import Iterable, Generator


def doExpand(iterable: Iterable[int]) -> Generator[int, None, None]:
    """do one round of the expansion"""

    v = next(iterable)
    count = 1
    while True: 
        try:
            c = next(iterable)
        except StopIteration:
            yield count
            yield v
            return
        if c == v:
            count += 1
        else:
            yield count
            yield v
            v = c
            count = 1
        

def y2015d10(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d10.txt"
    print("2015 day 10:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    start_str = lineList[0]

    s_value = list(map(int, start_str))

    generators = [iter(s_value)]
        
    for _ in range(40):
        generators.append(doExpand(generators[-1]))
    
    print("Built generators")

    Part_1_Answer = sum(1 for _ in generators[-1])

    #===========
    # Part 2
    #============

    #since part 1 runs very fast, just redo it

    generators = [iter(s_value)]
        
    for _ in range(50):
        generators.append(doExpand(generators[-1]))
    
    print("Built generators")

    Part_2_Answer = sum(1 for _ in generators[-1])

    return (Part_1_Answer, Part_2_Answer)