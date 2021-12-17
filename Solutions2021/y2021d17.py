# from AOC_Lib.name import *

import functools
import re
from multiprocessing import Pool
import itertools

RE_STR = r"\w+ \w+: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)"

def willIntersectRegion(starts_tuple, region_boundary) -> bool:
    x_min, x_max, y_min, y_max = region_boundary
    x_v_start, y_v_start = starts_tuple
    highest_y = 0
    for p_x, p_y in generatePositions(x_velocity_start=x_v_start, y_velocity_start=y_v_start):
        highest_y = max(highest_y, p_y)
        if p_y < y_min:
            return None
        if (p_y <= y_max) and (p_x >= x_min) and (p_x <= x_max):
            return highest_y

# generate all positions
def generatePositions(x_velocity_start, y_velocity_start):
    x_velocity = x_velocity_start
    y_velocity = y_velocity_start

    x_position = 0
    y_position = 0
    while True:
        yield (x_position, y_position)
        x_position += x_velocity
        y_position += y_velocity
        if x_velocity > 0:
            x_velocity -= 1
        elif x_velocity < 0:
            x_velocity += 1
        y_velocity -= 1


def y2021d17(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d17.txt"
    print("2021 day 17:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    m = re.match(RE_STR, lineList[-1])
    if m == None:
        raise RuntimeError

    x_min = int(m.group(1))
    x_max = int(m.group(2))
    y_min = int(m.group(3))
    y_max = int(m.group(4))

    # I think there is a closed form that will tell you the best value possible
    #   want to minimize x and maximize y so that you get as close as possible
    #   to the upper right corner of the region
    #   but, cpu cycles go brrrrrrrrrrrrrrrr....
    # HAHA in part 2 you need all of them anyway
    #   picking bounds could be more intelligent but whatever
    possible_starts = list(itertools.product(range(x_max + 3), range(y_min - 5, 500)))

    with Pool(processes=8) as p:
        f = functools.partial(willIntersectRegion, region_boundary=(x_min, x_max, y_min, y_max))
        r = list(p.map(f, possible_starts))

    Part_1_Answer = max(0 if l == None else l for l in r)
    Part_2_Answer = len([l for l in r if l != None])


    return (Part_1_Answer, Part_2_Answer)