# from AOC_Lib.name import *

from collections import deque


def y2021d9(inputPath=None):
    if inputPath == None:
        inputPath = "Input2021/d9.txt"
    print("2021 day 9:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    lineList = list(map(lambda x: list(map(int, x)), lineList))

    num_rows = len(lineList)
    num_cols = len(lineList[0])

    def generateNeighbors(r_id, c_id):
        if r_id != 0:
            # can go up
            yield (r_id - 1, c_id)
        if r_id + 1 < num_rows:
            # can go down
            yield (r_id + 1, c_id)
        if c_id != 0:
            yield (r_id, c_id - 1)
        if c_id + 1 < num_cols:
            yield (r_id, c_id + 1)

    def getScore(r_id, c_id):
        v = lineList[r_id][c_id]
        for n_r, n_c in generateNeighbors(r_id, c_id):
            if v >= lineList[n_r][n_c]:
                return 0
        return v + 1

    score = 0

    low_points = []

    for r in range(num_rows):
        for c in range(num_cols):
            a = getScore(r, c)
            score += a

            if a != 0:
                low_points.append((r, c))

    Part_1_Answer = score

    basinMap = [None] * num_rows
    for k in range(num_rows):
        basinMap[k] = [None] * num_cols

    def calculateBasinSize(r, c, i):
        q = deque()
        q.append((r, c))
        basinMap[r][c] = i
        size = 0

        while len(q):
            n_r, n_c = q.popleft()
            size += 1

            for nn_r, nn_c in generateNeighbors(n_r, n_c):
                if basinMap[nn_r][nn_c] is None and lineList[nn_r][nn_c] < 9:
                    basinMap[nn_r][nn_c] = i
                    q.append((nn_r, nn_c))

        return size

    basin_sizes = []

    for i, (r, c) in enumerate(low_points):
        basin_sizes.append(calculateBasinSize(r, c, i))

    basin_sizes.sort()

    assert len(basin_sizes) >= 3

    Part_2_Answer = basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]

    return (Part_1_Answer, Part_2_Answer)
