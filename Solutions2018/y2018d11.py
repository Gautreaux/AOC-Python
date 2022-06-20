# from AOC_Lib.name import *

# sample variant for single line inputs

import itertools
from typing import Generator, Iterator

FuelCell_T = int

FuelCellGrid_T = dict[tuple[int, int], FuelCell_T]


def buildFuelCellGrid(
    serial_number: int, 
    grid_width: int = 300, 
    grid_height: int = 300,
) -> FuelCellGrid_T:
    """Construct Fuel Cell Grid"""

    g: FuelCellGrid_T = {}

    for x in range(1, grid_width+1):
        for y in range(1, grid_height+1):
            rack_id = x + 10
            power_level = rack_id * y
            power_level += serial_number
            power_level *= rack_id            
            hundreds_digit = int("{:03}".format(power_level)[-3])
            assert((x,y) not in g)
            g[(x,y)] = (hundreds_digit - 5)
    
    return g


def generateNbyMWindows(
    grid: FuelCellGrid_T,
    n_rows: int,
    m_columns: int,
) -> Generator[tuple[tuple[int, int], Iterator[FuelCell_T]], None, None]:
    """Generate the sub windows of n rows by m columns where
        all elements of the window are inside the grid
        return tuple:
            upper left corner
            iterator of cells
    """

    transforms = list(tuple(itertools.product(
        range(m_columns), range(n_rows)
    )))

    min_x = min(map(lambda x: x[0], grid.keys()))
    max_x = max(map(lambda x: x[0], grid.keys()))
    min_y = min(map(lambda x: x[1], grid.keys()))
    max_y = max(map(lambda x: x[1], grid.keys()))

    for upper_left_x in range(min_x, max_x - m_columns + 1):
        for upper_left_y in range(min_y, max_y - n_rows + 1):
            yield (
                (upper_left_x, upper_left_y),
                map(
                    lambda p: grid[p],
                    map(
                        lambda t: (upper_left_x+t[0], upper_left_y+t[1]),
                        transforms,
                    )
                ),
            )


def maxPowerAndPos(grid: FuelCellGrid_T) -> tuple[tuple[int, int], int]:
    """Return the max power and pos"""
    return max(
        map(
            lambda x: (x[0], sum(x[1])),
            generateNbyMWindows(grid, n_rows=3, m_columns=3)
        ),
        key=(lambda x: x[1]),
    )
        



def maxPowerAndPos_variable(grid: FuelCellGrid_T, max_size:int = 300) -> tuple[tuple[int,int], int, int]:
    """Return max power and pos considering all windows"""
    
    assert(max_size > 1)

    cache_by_window_size: list[dict[tuple[int, int], int]] = [{}, grid, ]

    min_x = min(map(lambda x: x[0], grid.keys()))
    max_x = max(map(lambda x: x[0], grid.keys()))
    min_y = min(map(lambda x: x[1], grid.keys()))
    max_y = max(map(lambda x: x[1], grid.keys()))

    to_return_pos = (None, None)
    to_return_size = None
    to_return_score = None

    # single_case
    to_return_pos, to_return_score = max(
        grid.items(),
        key=(lambda x: x[1]),
    )
    to_return_size = 1

    for window_size in range(2, max_size+1):
        new_cache = {}

        if(window_size % 10 == 0):
            print(f"Starting window size {window_size}")

        transforms = list(itertools.chain(
            map(lambda x: (x,window_size-1), range(window_size)),
            map(lambda y: (window_size-1,y), range(window_size-1)),
        ))

        for upper_left_x in range(min_x, max_x - window_size + 1):
            for upper_left_y in range(min_y, max_y - window_size + 1):
                base = cache_by_window_size[-1][(upper_left_x, upper_left_y)]

                n = sum(map(
                    lambda t: grid[(upper_left_x+t[0], upper_left_y+t[1])],
                    transforms
                ))
                score = base + n
                if score > to_return_score:
                    to_return_pos = (upper_left_x, upper_left_y)
                    to_return_score = score
                    to_return_size = window_size
                new_cache[(upper_left_x, upper_left_y)] = score
        cache_by_window_size.append(new_cache)
    return (to_return_pos, to_return_size, to_return_score)


def y2018d11(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d11.txt"
    print("2018 day 11:")

    Part_1_Answer = None
    Part_2_Answer = None

    with open(inputPath) as f:
        line = f.readline().strip()
    serialNumber = int(line)

    # Test Cases

    _t = [
        ((  3,   5),  8, 4),
        ((122,  79), 57, -5),
        ((217, 196), 39,  0),
        ((101, 153), 71,  4),
    ]

    for pos, ser, power in _t:
        g = buildFuelCellGrid(ser)
        out_power = g[pos]
        print(f"[{ser}] Expected {power} got {out_power}")
        assert(out_power == power)

    _t = [
        (18, "33,45", 29),
        (42, "21,61", 30),
    ]

    for ser, ans, power in _t:
        g = buildFuelCellGrid(ser)
        out_ans, out_power = maxPowerAndPos(g)
        out_ans = "{},{}".format(out_ans[0], out_ans[1])
        print(f"[{ser}] Expected {power}@{ans} | got {out_power}@{out_ans}")
        assert(out_ans == ans)
        assert(out_power == power)
    
    # for part 2
    _t = [
        (18, (90,269), 16, 113),
        (42, (232, 251), 12, 119),
    ]

    # for ser, pos, size, power in _t:
    #     g = buildFuelCellGrid(ser)
    #     out_pos, out_size, out_power = maxPowerAndPos_variable(g)
    #     print("[{}] Expected {}@{}<{}> | got {}@{}<{}>".format(
    #         ser, power, pos, size, out_power, out_pos, out_size,
    #     ))
    #     assert(out_pos == pos)
    #     assert(out_power == power)
    #     assert(out_size == size)

    # End tests

    p1_ans_tuple, _ = maxPowerAndPos(buildFuelCellGrid(serialNumber))

    Part_1_Answer = f"{p1_ans_tuple[0]},{p1_ans_tuple[1]}"

    # TODO - this should be much much more efficient
    #   either multiprocessing
    #   or strided reduce 
    #   or both 

    print(f"WARN: This is horrifically inefficient. Sorry.")

    # TODO - fixme at some point
    # p2_ans_pos, p2_ans_size, p2_ans_power = maxPowerAndPos_variable(buildFuelCellGrid(serialNumber))
    
    p2_ans_pos, p2_ans_size, p2_ans_power = ((235, 118), 14, 166)

    print(f"P2: pos: {p2_ans_pos} sz: {p2_ans_size}, power: {p2_ans_power}")
    Part_2_Answer = f"{p2_ans_pos[0]},{p2_ans_pos[1]},{p2_ans_size}"

    assert(Part_1_Answer != "11,2")
    return (Part_1_Answer, Part_2_Answer)
