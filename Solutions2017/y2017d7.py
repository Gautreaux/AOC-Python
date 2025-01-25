# from AOC_Lib.name import *


def y2017d7(inputPath=None):
    if inputPath == None:
        inputPath = "Input2017/d7.txt"
    print("2017 day 7:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    weightsDict = {}
    adjList = {}

    for l in lineList:
        s = l.split(" ")
        name = s[0]
        weight = int(s[1][1:-1])

        adj = []
        for e in s[3:]:
            adj.append(e.replace(",", ""))

        weightsDict[name] = weight
        adjList[name] = adj

    # part 1
    ctr = {}
    for k in adjList:
        ctr[k] = 1
    for k in adjList.values():
        for e in k:
            ctr[e] -= 1
    l = list(filter(lambda x: ctr[x] == 1, ctr))
    # print(l)
    assert len(l) == 1
    Part_1_Answer = l[0]

    weightCache = {}

    def getWeight(name):
        assert name in weightsDict
        if name in weightCache:
            return weightCache[name]

        partialWeight = 0
        try:
            for a in adjList[name]:
                partialWeight += getWeight(a)
            partialWeight += weightsDict[name]
        finally:
            weightCache[name] = partialWeight
            return partialWeight

    def areSubTowersBalanced(name):
        assert name in weightsDict

        target = None
        for a in adjList[name]:
            w = getWeight(a)
            if target is None:
                target = w
            else:
                if w != target:
                    return False

    def findAllUnbalanced():
        """Get a list of all the unbalanced nodes"""
        l = []
        for a in weightsDict:
            if areSubTowersBalanced(a) is False:
                l.append(a)

        if len(l) == 0:
            raise RuntimeError("No unbalanced nodes")
        return l

    class BreakContinue(Exception):
        pass

    def findPrimaryUnbalance():
        """Return the node that is deepest in the hierarchy"""
        unbalanced = set(findAllUnbalanced())
        root = Part_1_Answer
        assert root in unbalanced
        while True:
            try:
                for a in adjList[root]:
                    if a in unbalanced:
                        unbalanced.remove(root)
                        parent = root
                        root = a
                        raise BreakContinue()
                assert len(unbalanced) == 1
                return root
            except BreakContinue:
                continue

    # print(getWeight(l[0]))
    print(findPrimaryUnbalance())

    imbalance = findPrimaryUnbalance()

    targetWeight = list(map(getWeight, adjList[imbalance]))

    # we know there has to be at least 3 children to know which weight is correct
    assert len(targetWeight) >= 3
    targetWeight.sort()
    # the wrong one could be the min or the max, so grab the middle
    incorrectWeight = (
        targetWeight[0] if targetWeight[0] != targetWeight[1] else targetWeight[-1]
    )
    targetWeight = targetWeight[1]

    difference = incorrectWeight - targetWeight

    badNode = list(
        filter(lambda x: getWeight(x) == incorrectWeight, adjList[imbalance])
    )
    assert len(badNode) == 1
    badNode = badNode[0]

    Part_2_Answer = weightsDict[badNode] - difference

    # checking
    weightsDict[badNode] = Part_2_Answer
    weightCache = {}
    try:
        l = findAllUnbalanced()
        print(f"ERROR - found unbalanced when none expected: {l}")
    except RuntimeError:
        print("Find unbalanced passed balance check")

    assert Part_2_Answer != 8434
    return (Part_1_Answer, Part_2_Answer)
