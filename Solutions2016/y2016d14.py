# from AOC_Lib.name import *

from hashlib import md5
from typing import List

# return the character that appears as a triple
def containsConsecutiveTriple(h : str) -> List[str]:
    toReturn = []
    for i in range(len(h)-2):
        c = h[i]
        if(h[i+1] == c and h[i+2] == c and c not in toReturn):
            toReturn.append(c)
            return toReturn
    return toReturn

# return true iff h contains c 5 consecutive times
def containsConsecutiveQuintuple(h : str, c : str) -> bool:
    for i in range(len(h)-4):
        if(h[i] == c and h[i+1] == c and h[i+2] == c and h[i+3] == c and h[i+4] == c):
            return True
    return False

def getHashAt(i : int, salt : str) -> str:
    return md5(bytes(f"{salt}{i}", "ascii")).hexdigest()

def getHashAtPart2(i : int, salt : str, rounds = 2016) -> str:
    s = md5(bytes(f"{salt}{i}", "ascii")).hexdigest()
    for i in range(rounds):
        s = md5(bytes(s, "ascii")).hexdigest()
    return s

hashCache = {}
def getHashAtPart2Cached(i : int, salt : str, rounds = 2016) -> str:
    t = (i, salt, rounds)
    if t in hashCache:
        return hashCache[t]
    else:
        h = getHashAtPart2(i, salt, rounds)
        hashCache[t] = h
        return h

class BreakAllException(Exception):
    pass

def getFirstNKeys(salt : str, n :int = 64, isPart2 : bool = False) -> List[int]:
    index = 0
    keys = []

    funptr = getHashAtPart2Cached if isPart2 is True else getHashAt

    while(len(keys) < n):
        h = funptr(index, salt)
        chars = containsConsecutiveTriple(h)
        try:
            for c in chars:
                for i in range(index + 1, index + 1001):
                    h2 = funptr(i, salt)
                    if(containsConsecutiveQuintuple(h2, c)):
                        keys.append(index)
                        # print(f"Found new triple at index {index}:{h}")
                        # print(f"\tChar : {c}")
                        # print(f"\tFound matching quintuple at {i}:{h2}")
                        # print(f"\tKey Len: {len(keys)}")

                        if(len(keys) % 8 == 0):
                            print(f"Key len: {len(keys)}, index: {index}, isPart2: {isPart2}")
                        raise BreakAllException()
        except BreakAllException:
            pass
        index += 1

    return keys


def y2016d14(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d14.txt"
    print("2016 day 14:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    salt = lineList[-1]

    # salt = "abc"

    assert(getHashAtPart2(0, "abc") == "a107ff634856bb300138cac6568c0f24")
    
    Part_1_Answer = getFirstNKeys(salt)[-1]
    Part_2_Answer = getFirstNKeys(salt, isPart2=True)[-1]
    
    assert(Part_1_Answer > 14741)
    # part2 != 20863        
    return (Part_1_Answer, Part_2_Answer)