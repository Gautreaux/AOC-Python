# from AOC_Lib.name import *

import itertools
from typing import Tuple


def y2015d9(inputPath=None):
    if inputPath == None:
        inputPath = "Input2015/d9.txt"
    print("2015 day 9:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    adjList = {}

    # for multi line inputs
    for line in lineList:
        s = line.split(" ")
        source = s[0]
        sink = s[2]
        dist = int(s[4])

        for p in [(source, sink), (sink, source)]:
            if p[0] not in adjList:
                adjList[p[0]] = []
            adjList[p[0]].append((p[1], dist))

    nodeNames = list(adjList.keys())
    nodeNames.sort()
    print(nodeNames)

    def getAllNodePermutations():
        """raw all permutations"""
        for i in itertools.permutations(nodeNames):
            yield i

    def getLen(source, sink) -> int:
        a = adjList[source]
        for k in a:
            if k[0] == sink:
                return k[1]
        return None

    def isAdj(source, sink) -> bool:
        return getLen(source, sink) is not None

    def getValidPermutation():
        """ "all valid permutations"""
        for permu in getAllNodePermutations():
            allValid = True
            for i in range(len(permu) - 1):
                source = permu[i]
                sink = permu[i + 1]
                if isAdj(source, sink) is False:
                    allValid = False
                    break
            if allValid is True:
                yield permu

    def getPermutationLen(permu) -> int:
        l = 0
        for i in range(len(permu) - 1):
            source = permu[i]
            sink = permu[i + 1]
            l += getLen(source, sink)
        return l

    # get shortest permu
    minLen = float("inf")
    maxLen = 0
    for permu in getValidPermutation():
        l = getPermutationLen(permu)
        if l < minLen:
            minLen = l
        if l > maxLen:
            maxLen = l
    Part_1_Answer = minLen
    Part_2_Answer = maxLen

    # i = 0
    # for _ in getAllNodePermutations():
    #     i += 1
    # print(i)

    # i = 0
    # for _ in getValidPermutation():
    #     i += 1
    # print(i)
    # turns out its fully connected
    #   this is probably important for part 2

    return (Part_1_Answer, Part_2_Answer)
