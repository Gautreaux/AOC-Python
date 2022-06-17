# from AOC_Lib.name import *

import itertools

from AOC_Lib.SlidingWindow import sliding_window

def advance(state: str, offset: int, plant_map: dict[str, str]) -> tuple[str, int]:
    """Advance one generation based on plant_map and return the new state and offset"""
    assert(set(state) == set("#."))
    o = []
    # only need to pad so that 4 empties on either side
    for i in sliding_window(itertools.chain("....", state, "...."), 5):
        i = "".join(i)
        if i not in plant_map:
            print(i)
        assert(i in plant_map)
        o.append(plant_map[i])

    # pop empties off of o
    while o:
        if o[-1] == ".":
            o.pop()
        else:
            break

    # pop off the front
    # s = sum(1 for _ in itertools.takewhile(lambda x: x == '.', o))
    k = "".join(itertools.dropwhile(lambda x: x == '.', o))
    num_dropped = len(o) - len(k)
    return (k, offset-2+num_dropped)


def getScoreForState(state, offset:int = 0) -> int:
    """Return the score for a given state"""
    e = zip(itertools.count(offset), state)
    f = filter(lambda x: x[1] == "#", e)
    return sum(map(lambda x: x[0], f))


def getScoreForDay_explicit(
    initial_state,
    plant_map,
    target_day:int,
    initial_offset:int=0,
) -> int:
    """Simulate each day for some number days and then get the score"""

    state = initial_state
    offset = initial_offset
    assert(target_day > 0)
    for _ in range(target_day):
        state, offset = advance(state, offset, plant_map)
    return getScoreForState(state, offset)


def getScoreForDay_fast(
    initial_state,
    plant_map,
    target_day: int,
    initial_offset: int = 0,
) -> int:
    """Get the score for a day exploiting any looping properties"""

    state = initial_state
    offset = initial_offset

    # cache states with day-offset pairs
    h_cache = {}
    h_cache[state] = (0, offset)

    first_loop_index = None
    first_loop_offset = None

    for i in range(1, 5000):
        state,offset = advance(state, offset, plant_map)
        if i == target_day:
            return getScoreForState(state, offset)
        elif state in h_cache:
            print(f"Found a loop at {i},{offset} back to {h_cache[state]}")
            first_loop_index = i
            first_loop_offset = offset
            break
        else:
            h_cache[state] = (i,offset)

    if first_loop_index is None:
        raise RuntimeError(f"Could not find a looping state in first 5000 states")

    base_loop_index, base_loop_offset = h_cache[state]

    loop_size = first_loop_index - base_loop_index
    offset_size = first_loop_offset - base_loop_offset

    print(f"  Loop occurs in {loop_size} steps, offset changes {offset_size}")

    num_steps = target_day - base_loop_index

    if num_steps % loop_size != 0:
        raise NotImplementedError(f"Loop size ({loop_size}) does not evenly divide days ({num_steps})")

    num_loops = num_steps // loop_size

    print(f"  Total {num_steps} days, {num_loops} loops")
    new_offset = num_loops * offset_size + base_loop_offset
    return getScoreForState(state, new_offset)


def y2018d12(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d12.txt"
    print("2018 day 12:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # for multi line inputs

    plant_map = {}

    itr = iter(lineList)

    start = next(itr)
    start_state = start.partition("initial state: ")[-1]

    for line in itr:
        if not line:
            continue
        a,_,b = line.partition(" => ")
        assert(b in ["#", "."])
        assert(len(a) == 5)
        plant_map[a] = b

    Part_1_Answer = getScoreForDay_explicit(start_state, plant_map, 20)

    # part 2
    # for d in [20, 50, 100, 153, 154, 155, 200, 1000]:
    #     print(f"Testing d = {d}")
    #     a = getScoreForDay_explicit(start_state, plant_map, d)
    #     b = getScoreForDay_fast(start_state, plant_map, d)
    #     if a != b:
    #         print(f"Expected: {a}, got {b}")
    #     assert(a == b)
    
    target = 50000000000
    Part_2_Answer = getScoreForDay_fast(start_state, plant_map, target)

    # assert(Part_2_Answer > 2649999996756)

    return (Part_1_Answer, Part_2_Answer)