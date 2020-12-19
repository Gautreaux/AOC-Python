# from AOC_Lib.name import *

from copy import deepcopy

def y2015d17(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d17.txt"
    print("2015 day 17:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    containerList = list(map(int, lineList))

    containerList.sort()
    print(containerList)

    # works for part 1 but pt2 give us it too
    # waysCache = {}
    # # waysCache[0] = 1

    # for i in containerList:
    #     newDict = deepcopy(waysCache)
    #     if i not in newDict:
    #         newDict[i] = 0
    #     newDict[i] += 1
    #     for total,numWays in waysCache.items():
    #         newTotal = total + i

    #         if newTotal not in newDict:
    #             newDict[newTotal] = 0
    #         newDict[newTotal] += numWays

    #     waysCache = newDict

    # Part_1_Answer = waysCache[150]


    permuDict = {}
    for c in containerList:
        # print(c)
        newPerm = deepcopy(permuDict)
        if c not in newPerm:
            newPerm[c] = []
        newPerm[c].append([c]) 

        for total, permuList in permuDict.items():
            newTotal = total + c
            if newTotal not in newPerm:
                newPerm[newTotal] = []
            for permu in permuList:
                p = deepcopy(permu)
                p.append(c)
                newPerm[newTotal].append(p)

        permuDict = newPerm

    
    # for e in range(6):
    #     if e not in permuDict:
    #         print(f"{e}:None")
    #         continue
    #     for p in permuDict[e]:
    #         print(f"{e}:{p}")

    Part_1_Answer = len(permuDict[150])

    minContainerCount = min(map(len, permuDict[150]))
    print(f"Min container count = {minContainerCount} (not necessarily pt2 answer)")
    Part_2_Answer = sum(1 for _ in filter(lambda x : len(x) == minContainerCount, permuDict[150]))
    

    return (Part_1_Answer, Part_2_Answer)