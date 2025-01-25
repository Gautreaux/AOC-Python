# from AOC_Lib.name import *

import itertools


IP_RANGE_T = tuple[int, int]


def is_in_range(a: int, r: IP_RANGE_T) -> bool:
    """Return True iff `a` is in the range `r`"""
    return (a >= r[0]) and (a <= r[1])


def do_ranges_intersect(a: IP_RANGE_T, b: IP_RANGE_T) -> bool:
    """Return True iff these ranges intersect"""

    if is_in_range(a[0], b):
        return True
    elif is_in_range(a[1], b):
        return True
    elif is_in_range(b[0], a):
        return True
    elif is_in_range(b[1], a):
        return True
    return False


def update_ranges(new_range: IP_RANGE_T, all_range: set[IP_RANGE_T]) -> None:
    """Update all_range to reflect addition of new_range"""

    impacted_ranges = []

    for r in all_range:
        if do_ranges_intersect(r, new_range):
            impacted_ranges.append(r)

    if not impacted_ranges:
        all_range.add(new_range)
        return

    # all the impacted ranges intersect

    m = min(itertools.chain([new_range[0]], map(lambda x: x[0], impacted_ranges)))
    x = max(itertools.chain([new_range[1]], map(lambda x: x[1], impacted_ranges)))

    for r in impacted_ranges:
        all_range.remove(r)

    all_range.add((m, x))


def y2016d20(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d20.txt"
    print("2016 day 20:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    ranges = []

    for l in lineList:
        s, e = l.split("-")
        assert int(s) <= int(e)
        ranges.append((int(s), int(e)))

    print(f"Raw input contains: {len(ranges)} ranges")

    ranges.sort()

    reduced_ranges = set()

    for r in ranges:
        update_ranges(r, reduced_ranges)

    l = list(reduced_ranges)
    l.sort()
    print(f"Reduced input contains {len(reduced_ranges)} ranges: {l[:3]}...")

    # part 1
    for i in range(2**32):

        is_valid = True

        for k in l:
            if is_in_range(i, k):
                is_valid = False
                break

        if is_valid:
            Part_1_Answer = i
            break

    # part 2

    t = 2**32

    for r in reduced_ranges:
        n = r[1] - r[0] + 1
        t -= n
    Part_2_Answer = t

    return (Part_1_Answer, Part_2_Answer)
