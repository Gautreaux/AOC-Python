# from AOC_Lib.name import *


def y2017d12(inputPath=None):
    if inputPath == None:
        inputPath = "Input2017/d12.txt"
    print("2017 day 12:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    adjList = {}

    for line in lineList:
        label, adj = line.split(" <-> ")
        label = int(label)
        if label not in adjList:
            adjList[label] = set()
        ls = adjList[label]

        for k in adj.split(", "):
            k = int(k)
            if k not in adjList:
                adjList[k] = set()
            ks = adjList[k]
            ls.add(k)
            ks.add(label)

    visitSet = set()

    def visitAll(startingNode):
        pendingQueue = [startingNode]
        while len(pendingQueue) > 0:
            this = pendingQueue[-1]
            pendingQueue = pendingQueue[:-1]

            if this in visitSet:
                continue

            visitSet.add(this)

            for k in adjList[this]:
                if k not in visitSet:
                    pendingQueue.append(k)

    visitAll(0)
    Part_1_Answer = len(visitSet)

    totalGroups = 1

    for i in adjList:
        if i in visitSet:
            continue
        visitAll(i)
        totalGroups += 1

    Part_2_Answer = totalGroups

    return (Part_1_Answer, Part_2_Answer)
