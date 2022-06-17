# from AOC_Lib.name import *

from collections import defaultdict
from copy import copy
from typing import Generator

Cave_T = str
Path_T = list[Cave_T]

adj_map: defaultdict[Cave_T, set] = defaultdict(set)


def isSmallCave(c:Cave_T) -> bool:
    """Return True iff this is a small cave
        NOTE: this is not opposite of `isBigCave`
    """
    if len(c) != 2:
        return False
    return (c == c.lower())


def isBigCave(c: Cave_T) -> bool:
    """Return True iff this is a big cave
        NOTE: this is not opposite of `isSmallCave`
    """
    if len(c) != 2:
        return False
    return (c == c.upper())


def generateSubPaths(p: Path_T, nsd_remain: int = 0) -> Generator[Path_T, None, None]:
    """Generate all the sub-paths of `p`
        `nsd_remain` - number of small duplicates that remain
    """
    global adj_map

    assert(p != [])
    k = p[-1]
    v = adj_map[k]

    for a in v:
        if a == 'end':
            l = copy(p)
            l.append('end')
            yield l
        elif a == 'start':
            continue
        elif isBigCave(a):
            l = copy(p)
            l.append(a)
            for s in generateSubPaths(l, nsd_remain=nsd_remain):
                yield s
        elif isSmallCave(a):
            if a not in p:
                l = copy(p)
                l.append(a)
                for s in generateSubPaths(l, nsd_remain=nsd_remain):
                    yield s
            elif nsd_remain:
                l = copy(p)
                l.append(a)
                for s in generateSubPaths(l, nsd_remain=nsd_remain-1):
                    yield s
        else:
            raise RuntimeError(f"Unhandled case: `{a}` from `{k}` {p}")


def generateAllPaths(nsd_remain: int = 0) -> Generator[Path_T, None, None]:
    """Generate all paths starting at `start`"""
    return generateSubPaths(['start'], nsd_remain=nsd_remain)


def y2021d12(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d12.txt"
    print("2021 day 12:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    global adj_map

    for line in lineList:
        a,b = line.split("-")
        adj_map[a].add(b)
        adj_map[b].add(a)

    # need to ensure that there are no cycles of big caves
    #   its a quick test but works for me
    for k,v in adj_map.items():
        if isBigCave(k):
            for a in v:
                if isBigCave(a):
                    raise RuntimeError("Possible cycle in big caves")

    assert("start" in adj_map)
    assert("end" in adj_map)

    # for p in generateAllPaths():
    #     print(p)

    Part_1_Answer = sum(1 for _ in generateAllPaths())
    Part_2_Answer = sum(1 for _ in generateAllPaths(1))

    return (Part_1_Answer, Part_2_Answer)