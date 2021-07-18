# from AOC_Lib.name import *

import itertools

def checksum(s, lenGoal=None):
    if lenGoal is not None:
        s = s[:lenGoal]
    
    if len(s) % 2 == 1:
        return s
    
    l = []

    try:
        for i in range(len(s)):
            l.append(
                "1" if s[i*2] == s[i*2+1] else "0"
            )
    except IndexError:
        pass

    c = "".join(l)

    return checksum(c)

def doOneRound(input):
    b = reversed(input)
    b = map(lambda x: '0' if x == '1' else '1', b)
    return "".join(itertools.chain(input, '0', b))

def y2016d16(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d16.txt"
    print("2016 day 16:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # test cases
    assert(doOneRound("1") == "100")
    assert(doOneRound("0") == "001")
    assert(doOneRound("11111") == "11111000000")
    assert(doOneRound("111100001010") == "1111000010100101011110000")
    
    b = lineList[0]

    while len(b) < 272:
        b = doOneRound(b)

    Part_1_Answer = checksum(b, 272)

    print("part 1 done")
    print(len(b))
    print(len(Part_1_Answer))

    while len(b) < 35651584:
        b = doOneRound(b)
    print("part 2 gen done")
    
    Part_2_Answer = checksum(b, 35651584)
    print("part 2 done")
    print(len(b))
    print(len(Part_2_Answer))


    return (Part_1_Answer, Part_2_Answer)