# from AOC_Lib.name import *

from collections import Counter
from typing import Generator


def GenerateAsleepStates(lineList: list[str]) -> Generator[tuple[int, int], None, None]:
    """Generate tuples of guard_id, minute which specifies the behavior of the guards
    where minute is the number of minutes since midnight
    """
    # id of the last guard to come on duity
    last_guard_id = None
    last_asleep_time = None

    for line in lineList:
        date_time, _, action = line[1:].partition("] ")

        date, _, time = date_time.partition(" ")

        # convert time to minutes
        hours, _, minutes = time.partition(":")
        minutes = int(minutes) + (60 * int(hours))

        if action.startswith("Guard"):
            last_guard_id = int(action.split(" ")[1][1:])
        elif action.startswith("falls"):
            assert last_guard_id is not None
            assert last_asleep_time is None
            last_asleep_time = minutes
        elif action.startswith("wakes"):
            assert last_guard_id is not None
            assert last_asleep_time is not None
            for i in range(last_asleep_time, minutes):
                yield (last_guard_id, i)
            last_asleep_time = None
        else:
            raise RuntimeError(f"Unrecognized line: `{line}`")


def y2018d4(inputPath=None):
    if inputPath == None:
        inputPath = "Input2018/d4.txt"
    print("2018 day 4:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    lineList.sort()

    mins_generator = GenerateAsleepStates(lineList)

    # since we need to iterate multiple times this should be faster
    all_mins = list(mins_generator)

    # this could be more efficient but whatever
    mins_asleep_by_guard_id = Counter(map(lambda x: x[0], all_mins))

    # print(mins_asleep_by_guard_id)

    most_asleep_guard_id, mins_asleep_qty = max(
        mins_asleep_by_guard_id.items(), key=lambda x: x[1]
    )

    asleep_by_max_guard = Counter(
        map(lambda x: x[1], filter(lambda x: x[0] == most_asleep_guard_id, all_mins))
    )

    most_asleep_min, most_asleep_min_qty = max(
        asleep_by_max_guard.items(), key=lambda x: x[1]
    )

    Part_1_Answer = most_asleep_guard_id * most_asleep_min

    # Part 2

    most_asleep_per_min = Counter(all_mins)

    p2_guard, p2_min = max(most_asleep_per_min.items(), key=lambda x: x[1])

    Part_2_Answer = p2_guard[0] * p2_guard[1]

    return (Part_1_Answer, Part_2_Answer)
