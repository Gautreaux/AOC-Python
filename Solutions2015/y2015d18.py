# from AOC_Lib.name import *

import itertools
from typing import Any

from AOC_Lib.NeighborGenerator import neighborGeneratorFactory


_GRID_SIZE_X = 100
_GRID_SIZE_Y = _GRID_SIZE_X

_ON = 1
_OFF = 0

Grid_T = list[list[int]]


def generateBlankGrid(default_value: Any = _OFF) -> Grid_T:
    return list(map((lambda x: [default_value] * _GRID_SIZE_X), range(_GRID_SIZE_Y)))


def buildNextState(grid: Grid_T, pos_x: int, pos_y: int) -> int:
    """Return _ON if on, _OFF if off in the next state"""

    neighbor_gen = neighborGeneratorFactory(
        len(grid[pos_y]) - 1, len(grid) - 1, allow_diagonal=True
    )

    qtyOnNeighbors = 0
    for n_x, n_y in neighbor_gen(pos_x, pos_y):
        if grid[n_y][n_x] != _OFF:
            qtyOnNeighbors += 1
    in_state = grid[pos_y][pos_x]

    if in_state == _ON:
        return _ON if qtyOnNeighbors in [2, 3] else _OFF
    else:
        assert in_state == _OFF
        return _ON if qtyOnNeighbors == 3 else _OFF


def buildNextGrid(grid, is_part_2: bool = False) -> Grid_T:
    new_grid = generateBlankGrid(0)

    for y_val in range(len(grid)):
        for x_val in range(len(grid[y_val])):
            new_grid[y_val][x_val] = buildNextState(grid, x_val, y_val)

    if is_part_2:
        new_grid[0][0] = _ON
        new_grid[0][-1] = _ON
        new_grid[-1][0] = _ON
        new_grid[-1][-1] = _ON
    return new_grid


def countOnLights(grid: Grid_T) -> int:
    return sum(itertools.chain.from_iterable(grid))


def y2015d18(inputPath=None):
    if inputPath == None:
        inputPath = "Input2015/d18.txt"
    print("2015 day 18:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    start_grid = generateBlankGrid()
    for y_val, line in enumerate(lineList):
        for x_val, char in enumerate(line):
            start_grid[y_val][x_val] = _ON if char == "#" else _OFF

    this_grid = start_grid
    pt_2_grid = start_grid
    for i in range(100):
        if i % 10 == 0:
            print(f"{i}% complete")
        this_grid = buildNextGrid(this_grid)
        pt_2_grid = buildNextGrid(pt_2_grid, is_part_2=True)

    Part_1_Answer = countOnLights(this_grid)
    Part_2_Answer = countOnLights(pt_2_grid)

    return (Part_1_Answer, Part_2_Answer)
