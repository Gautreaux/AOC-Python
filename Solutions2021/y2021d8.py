# from AOC_Lib.name import *

from typing import List
import itertools
from collections import defaultdict

FIXED_POINT_LENGTHS = [2, 3, 4, 7]


def determineMapping(signal_segments: List[str], out_segments: List[str]):

    possible = defaultdict(lambda: set("abcdefg"))
    known = [None] * 7

    # do the known points
    for s in itertools.chain(signal_segments, out_segments):
        if len(s) in FIXED_POINT_LENGTHS:
            st = set(s)

            if len(s) == 2:
                # 1
                possible[1] = possible[1].intersection(st)
                possible[2] = possible[2].intersection(st)
            elif len(s) == 3:
                # 7
                possible[0] = possible[0].intersection(st)
                possible[1] = possible[1].intersection(st)
                possible[2] = possible[2].intersection(st)
            elif len(s) == 4:
                # 4
                possible[1] = possible[1].intersection(st)
                possible[2] = possible[2].intersection(st)
                possible[5] = possible[5].intersection(st)
                possible[6] = possible[6].intersection(st)
            elif len(s) == 7:
                # this is a no-op
                # for i in range(7):
                #     possible[i] = possible[i].intersection(s)
                pass

    # logic checkpoint
    assert len(possible[6]) == 4
    assert len(possible[5]) == 4
    assert len(possible[0]) == 3
    assert possible[1] == possible[2]
    assert possible[5] == possible[6]
    assert len(possible[1]) == 2
    assert len(possible[2]) == 2

    # now, remove what we can
    p_0 = possible[0] - (possible[5].intersection(possible[1]))
    assert len(p_0) == 1
    n_4_possible = (possible[5] - possible[1]) - p_0
    assert len(n_4_possible) == 2
    n_2_possible = possible[1] - p_0
    assert len(n_2_possible) == 2

    # much much more efficient option
    score = 0

    # print(f"{p_0} {n_2_possible} {n_4_possible}")

    for p in out_segments:
        score *= 10
        if len(p) == 2:
            score += 1
        elif len(p) == 3:
            score += 7
        elif len(p) == 4:
            score += 4
        elif len(p) == 7:
            score += 8
        elif len(p) == 6:
            # this is a 0 6 or 9
            s = set(p)
            a = n_2_possible.issubset(s)
            b = n_4_possible.issubset(s)
            # print(f"6 - {s} {a} {b}")
            if a and b:
                score += 9
            elif a and (not b):
                score += 0
            elif (not a) and b:
                score += 6
            else:
                assert (not a) and (not b)
                raise RuntimeError("Illegal foramt")
        elif len(p) == 5:
            # this is a 3 9 2 or 5
            s = set(p)
            a = n_2_possible.issubset(s)
            b = n_4_possible.issubset(s)
            # print(f"5 - {s} {a} {b}")

            if a and b:
                raise RuntimeError("Illegal format")
                # would be 5 segment based 9
                # score += 9
            elif a and (not b):
                score += 3
            elif (not a) and b:
                score += 5
            else:
                assert (not a) and (not b)
                score += 2
        else:
            raise RuntimeError(f"Illegal number of segments: {len(p)}")

    # print(f"{out_segments} : {score}")
    return score


def y2021d8(inputPath=None):
    if inputPath == None:
        inputPath = "Input2021/d8.txt"
    print("2021 day 8:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    pre = []
    post = []
    for line in lineList:
        a, _, b = line.partition(" | ")
        pre.append(a)
        post.append(b)

    ctr = 0
    for p in post:
        l = p.split(" ")
        for a in l:
            if len(a) in FIXED_POINT_LENGTHS:
                ctr += 1

    Part_1_Answer = ctr

    assert len(pre) == len(post)

    output = 0
    for pr, po in zip(pre, post):
        output += determineMapping(pr.split(" "), po.split(" "))

    Part_2_Answer = output

    return (Part_1_Answer, Part_2_Answer)
