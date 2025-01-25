# from AOC_Lib.name import *

from collections import Counter
import itertools


EMPTY = "."
RIGHT = ">"
DOWN = "v"

GridCell_T = str

Grid_T = list[list[GridCell_T]]


def stepRight(grid: Grid_T) -> bool:
    """Step right, updating grid in place
    Return `True` iff anything moved
    """

    any_move: bool = False

    for row in grid:
        was_front_empty = row[0] == EMPTY
        was_back_right = row[-1] == RIGHT

        itr = iter(range(len(row) - 1))
        for index in itr:
            pair = (row[index], row[index + 1])

            if pair == (RIGHT, EMPTY):
                row[index] = EMPTY
                row[index + 1] = RIGHT
                any_move = True
                try:
                    next(itr)
                except StopIteration:
                    break

        if was_back_right and was_front_empty:
            row[0] = RIGHT
            row[-1] = EMPTY
            any_move = True

    return any_move


def stepDown(grid: Grid_T) -> bool:
    """Step down, updating the grid in place
    Return `True` iff anything moved
    """

    any_move: bool = False

    for col_id in range(len(grid[0])):
        was_top_empty = grid[0][col_id] == EMPTY
        was_bottom_down = grid[-1][col_id] == DOWN

        itr = iter(range(len(grid) - 1))
        for index in itr:
            pair = (grid[index][col_id], grid[index + 1][col_id])

            if pair == (DOWN, EMPTY):
                grid[index][col_id] = EMPTY
                grid[index + 1][col_id] = DOWN
                any_move = True
                try:
                    next(itr)
                except StopIteration:
                    break

        if was_top_empty and was_bottom_down:
            grid[0][col_id] = DOWN
            grid[-1][col_id] = EMPTY
            any_move = True

    return any_move


def step(grid: Grid_T) -> bool:
    """Step over then down
    Updates in place and returns `True` iff anything moved
    """
    a = stepRight(grid)
    b = stepDown(grid)
    return a or b


def y2021d25(inputPath=None):
    if inputPath == None:
        inputPath = "Input2021/d25.txt"
    print("2021 day 25:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # debug
    #     lineList = (
    # """v...>>.vv>
    # .vv>>.vv..
    # >>.>v>...v
    # >>v>>.>.v.
    # v>v.vv.v..
    # >.>>..v...
    # .vv..>.>v.
    # v.v..>>v.v
    # ....v..v.>"""
    #     ).splitlines()

    grid = []
    for line in lineList:
        row = list(line)
        grid.append(row)

    print("Initial state:")
    for line in grid:
        print("".join(line))
    print("\n")

    original_counts = Counter(itertools.chain.from_iterable(grid))

    for i in itertools.count(1):
        b = step(grid)
        # print(f"After {i} steps:")
        # for line in grid:
        #     print("".join(line))
        # print('\n')

        c = Counter(itertools.chain.from_iterable(grid))
        if c != original_counts:
            raise RuntimeError(
                "Some items were added {} or destroyed {}".format(
                    c - original_counts,
                    original_counts - c,
                )
            )

        if not b:
            break

    Part_1_Answer = i

    return (Part_1_Answer, Part_2_Answer)
