# from AOC_Lib.name import *

from copy import deepcopy
from collections import deque
import itertools


def generatePossibleNeighbors(row_id, col_id):
    for o1 in [-1, 0, 1]:
        for o2 in [-1, 0, 1]:
            a = (row_id + o1, col_id + o2)
            if a == (row_id, col_id):
                continue
            if a[0] < 0 or a[0] >= 10:
                continue
            if a[1] < 0 or a[1] >= 10:
                continue
            yield a


def y2021d11(inputPath=None):
    if inputPath == None:
        inputPath = "Input2021/d11.txt"
    print("2021 day 11:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    octopus_map = []
    flash_map_false = []
    for line in lineList:
        octopus_map.append(list(map(int, line)))
        flash_map_false.append([False for f in line])

    total_flashes = 0

    for round in range(1, 10000000000):
        new_map = deepcopy(octopus_map)
        flash_q = deque()

        this_flash_map = deepcopy(flash_map_false)

        for row_id, row in enumerate(octopus_map):
            for col_id, cell in enumerate(row):
                new_map[row_id][col_id] += 1

                if new_map[row_id][col_id] > 9:
                    flash_q.append((row_id, col_id))

        flash_set = []

        while len(flash_q) > 0:
            this_r, this_c = flash_q.popleft()

            if this_flash_map[this_r][this_c]:
                continue

            this_flash_map[this_r][this_c] = True
            flash_set.append((this_r, this_c))

            for n_r, n_c in generatePossibleNeighbors(this_r, this_c):
                new_map[n_r][n_c] += 1
                if new_map[n_r][n_c] > 9:
                    flash_q.append((n_r, n_c))

        # set items that flashed to zero
        for row_id, row in enumerate(this_flash_map):
            for col_id, cell in enumerate(row):
                if cell:
                    total_flashes += 1
                    new_map[row_id][col_id] = 0

        octopus_map = new_map

        if round == 100:
            Part_1_Answer = total_flashes
            if Part_2_Answer is not None:
                break

        if False in itertools.chain.from_iterable(this_flash_map):
            pass
        else:
            Part_2_Answer = round
            if Part_1_Answer is not None:
                break

    return (Part_1_Answer, Part_2_Answer)
