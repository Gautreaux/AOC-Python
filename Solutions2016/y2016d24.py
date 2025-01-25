# from AOC_Lib.name import *

from AOC_Lib.queue import CircularQueue

import itertools

# calculate the maze distance from the square to all other poi


def calcMazeDist(pos, maze):
    maxSize = len(maze[0]) * len(maze)

    q = CircularQueue(maxSize=maxSize)

    visited = set()
    visited.add(pos)
    q.push((pos, 0))

    transforms = [
        lambda x: (x[0] - 1, x[1]),
        lambda x: (x[0] + 1, x[1]),
        lambda x: (x[0], x[1] - 1),
        lambda x: (x[0], x[1] + 1),
    ]

    poi = {}

    while len(q) > 0:
        nowPos, dist = q.pop()

        if maze[nowPos[1]][nowPos[0]] not in [".", "#"]:
            poi[maze[nowPos[1]][nowPos[0]]] = dist

        for t in transforms:
            newPos = t(nowPos)

            if maze[newPos[1]][newPos[0]] == "#":
                continue
            if newPos in visited:
                continue
            visited.add(newPos)
            q.push((newPos, dist + 1))
    return poi


def y2016d24(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d24.txt"
    print("2016 day 24:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    poi = {}

    for y in range(len(lineList)):
        for x in range(len(lineList[y])):
            if lineList[y][x] not in [".", "#"]:
                poi[lineList[y][x]] = (x, y)

    print(poi)
    keys = set(poi.keys())

    myGraph = {}
    for k, p in poi.items():
        myGraph[k] = calcMazeDist(p, lineList)
        assert keys == set(myGraph[k].keys())

    keys.remove("0")

    shortestLen = 100000000000000000

    for permu in itertools.permutations(keys, len(keys)):
        total = 0
        # print(permu)
        for i, v in enumerate(permu):
            last = "0" if i == 0 else permu[i - 1]
            # print(f"{last}->{v}")

            total += myGraph[last][v]

        shortestLen = min(shortestLen, total)

    Part_1_Answer = shortestLen

    shortestLen = 100000000000000000

    for permu in itertools.permutations(keys, len(keys)):
        total = 0
        # print(permu)
        for i, v in enumerate(permu):
            last = "0" if i == 0 else permu[i - 1]
            # print(f"{last}->{v}")

            total += myGraph[last][v]

        total += myGraph[permu[-1]]["0"]

        shortestLen = min(shortestLen, total)

    Part_2_Answer = shortestLen

    assert Part_2_Answer <= 1286
    assert Part_2_Answer <= 1268
    assert Part_2_Answer > Part_1_Answer

    return (Part_1_Answer, Part_2_Answer)
