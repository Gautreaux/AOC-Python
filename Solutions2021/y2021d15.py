# from AOC_Lib.name import *

import heapq as pq
import itertools

from AOC_Lib.NeighborGenerator import neighborGeneratorFactory


def findBestPath(risk_map):
    width = len(risk_map[0])
    height = len(risk_map)

    best_map = [
        x
        for x in map(
            lambda _: list(itertools.repeat(None, width)), itertools.repeat(0, height)
        )
    ]

    assert len(best_map[0]) == len(risk_map[0])
    assert len(best_map) == len(risk_map)

    neighbor_gen = neighborGeneratorFactory(len(risk_map[0]) - 1, len(risk_map) - 1)

    q = []
    pq.heappush(q, (0, (0, 0)))

    while len(q) > 0:
        dist, (x, y) = pq.heappop(q)

        if best_map[y][x] is not None:
            assert dist >= best_map[y][x]
            continue

        best_map[y][x] = dist

        for n_x, n_y in neighbor_gen(x, y):
            r = risk_map[n_y][n_x]
            c = dist + r

            pq.heappush(q, (c, (n_x, n_y)))
    return best_map[-1][-1]


def y2021d15(inputPath=None):
    if inputPath == None:
        inputPath = "Input2021/d15.txt"
    print("2021 day 15:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    risk_map = []

    for line in lineList:
        a = []
        for d in line:
            a.append(int(d))
        risk_map.append(a)

    Part_1_Answer = findBestPath(risk_map)

    risk_map_2 = []

    h = len(risk_map)
    w = len(risk_map[0])

    for _ in range(h * 5):
        risk_map_2.append([None] * (w * 5))

    for y in range(h):
        for x in range(w):
            for a in range(5):
                for b in range(5):
                    c = risk_map[y][x] + a + b
                    while c > 9:
                        c -= 9
                    risk_map_2[y + h * a][x + w * b] = c

    Part_2_Answer = findBestPath(risk_map_2)

    return (Part_1_Answer, Part_2_Answer)
