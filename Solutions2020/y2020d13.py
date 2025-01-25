# from AOC_Lib.name import *

from functools import reduce
from math import ceil, lcm
from typing import List, Tuple


def doReduce(period0, offset0, period1, offset1) -> Tuple[int, int]:
    """Reduce two period offset tuples into their derived period offset tuple"""
    # the derived tuple is the one such that anytime it leaves the station,
    #   the two componet tuples are also leaving the station

    # find where the first time both leave is
    first = None

    # basically loop counter
    i0 = 1
    i1 = 1
    while True:
        # get the time that loop i# of bus # leaves the station
        #   accounting for offset
        k0 = (period0 * i0) + offset0
        k1 = (period1 * i1) + offset1

        if k0 == k1:
            # they started at the same time (w/ offsets)
            # print(f"Found {period0} {period1} match at t={k0}")
            first = k0
            break
        elif k0 < k1:
            # skip ahead to the next possible loop candidate
            #   bigly important when the periods become big numbers
            i0 = ceil((k1 - offset0) / period0)
        else:  # k1 < k0
            i1 = ceil((k0 - offset1) / period1)

    # the new period is the lcm of the components
    return (lcm(period0, period1), first)


# wrap doReduce to work with the provided reduce() syntax


def doReduceWrapper(
    periodOffset0: Tuple[int, int], periodOffset1: Tuple[int, int]
) -> Tuple[int, int]:
    return doReduce(*periodOffset0, *periodOffset1)


def y2020d13(inputPath=None):
    if inputPath == None:
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

    s = list(set(lineList[1].split(",")))
    s.remove("x")
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
    # print(wait)
    # print(busId)

    Part_1_Answer = busId * wait

    assert Part_1_Answer != 677677677677677

    # lineList[1] = "17,x,13,19"

    # part 2

    offsets = {}
    ss = lineList[1].split(",")
    for k in ss:
        if k == "x":
            continue
        else:
            offsets[int(k)] = ss.index(k)

    print(offsets)

    offsetsList: List = list(offsets.items())
    # inP, inO = doReduce(*l[0], *l[1])
    # for k,v in l[2:]:
    #     inP,inO = doReduce(inP, inO, k, v)

    finalPeriod, finalOffset = reduce(doReduceWrapper, offsetsList)

    # not sure exactly why, but the answer is this
    Part_2_Answer = finalPeriod - finalOffset

    return (Part_1_Answer, Part_2_Answer)
