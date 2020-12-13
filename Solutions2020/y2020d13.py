# from AOC_Lib.name import *

from math import gcd, ceil
from functools import reduce
from typing import List, Tuple

def y2020d13(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d13.txt"
    print("2020 day 13:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    earliest = int(lineList[0])

    s = list(set(lineList[1].split(',')))
    s.remove('x')
    print(s)

    wait = 0
    for i in range(0, 100000):
        n = earliest + i
        if 0 in map(lambda x: n % int(x), s):
            wait = int(i)
            break
    

    busId = 0
    for e in s:
        if (earliest + wait) % int(e) == 0:
            busId = int(e)
            break
    print(wait)
    print(busId)

    Part_1_Answer = busId * wait


    assert(Part_1_Answer != 677677677677677)

    #lineList[1] = "17,x,13,19"

    # part 2

    offsets = {}
    ss = lineList[1].split(',')
    for k in ss:
        if k == 'x':
            continue
        else:
            offsets[int(k)] = ss.index(k)
    
    print(offsets)

    def lcm(a, b):
        return abs(a*b) // gcd(a, b)

    def doReduce(p0, o0, p1, o1) -> Tuple[int, int]:
        # find where the first intersection is
        first = None

        i0 = 1
        i1 = 1
        while True:
            k0 = (p0*i0)+o0
            k1 = (p1*i1)+o1
            
            if k0 == k1:
                print(f"Found {p0} {p1} match at {k0}")
                first = k0
                break
            elif k0 < k1:
                # skip ahead to the next possible candidate
                i0 = ceil((k1 - o0)/p0)
            else: # k1 < k0
                i1 = ceil((k0 - o1)/p1)


        return (lcm(p0,p1), first)

    l = list(offsets.items())
    inP, inO = doReduce(*l[0], *l[1])
    for k,v in l[2:]:
        inP,inO = doReduce(inP, inO, k, v)
    
    Part_2_Answer = (inP - inO)
    
    return (Part_1_Answer, Part_2_Answer)

    myGCD = reduce(gcd, offsets)
    myMult = reduce(lambda x,y: x*y, offsets)
    myLCM = myMult//myGCD
    print(myLCM)

    def infiniteGenerator():
        i = 0
        while True:
            yield i*myLCM
            i += 1

    class BreakContinue(Exception):
        pass

    for i in infiniteGenerator():
        try:
            for k in offsets:
                if (offsets[k]+i)%k != 0:
                    raise BreakContinue()
            Part_2_Answer = i
            break
        except BreakContinue:
            continue




    return (Part_1_Answer, Part_2_Answer)

    def multipleGenerator(n, o):
        i = 0
        while True:
            yield (i * n) - o
            i += 1

    generatorList = []
    valuesList = []
    for key, offset in offsets.items():
        generatorList.append(multipleGenerator(key, offset))
        valuesList.append(next(generatorList[-1]))
    
    maxValue = max(valuesList)
    while True:
        allMatch = True
        for i in range(len(valuesList)):
            while valuesList[i] < maxValue:
                valuesList[i] = next(generatorList[i])
            if valuesList[i] > maxValue:
                maxValue = valuesList[i]
                allMatch = False
        if allMatch:
            Part_2_Answer = valuesList[0]
            break

    return (Part_1_Answer, Part_2_Answer)