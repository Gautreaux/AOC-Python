# from AOC_Lib.name import *

from collections import namedtuple
import itertools
from typing import Generator

import sys

sys.setrecursionlimit(1200)

NanoBot = namedtuple("NanoBot", "pos radius")


def doNanoBotsIntersect(a: NanoBot, b: NanoBot) -> bool:
    r_sum = a.radius + b.radius
    m_dist = sum(map(lambda x, y: abs(x - y), a.pos, b.pos))
    return r_sum >= m_dist


def y2018d23(inputPath=None):
    if inputPath == None:
        inputPath = "Input2018/d23.txt"
    print("2018 day 23:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    nanobots: list[NanoBot] = []

    for line in lineList:
        p, r = line.split(" ")
        r_value = int(r[2:])
        p_value = tuple(map(int, p[5:-2].split(",")))
        nanobots.append(NanoBot(p_value, r_value))

    strongest_nanobot = max(nanobots, key=lambda x: x.radius)

    bots_in_range = list(
        filter(
            lambda x: sum(map(lambda x, y: abs(x - y), x.pos, strongest_nanobot.pos))
            <= strongest_nanobot.radius,
            nanobots,
        )
    )

    Part_1_Answer = len(bots_in_range)

    # Part_2

    # check that all are unique
    assert len(set(nanobots)) == len(nanobots)

    min_vals = tuple(map(lambda x: min(map(lambda y: y.pos[x], nanobots)), range(3)))
    max_vals = tuple(map(lambda x: max(map(lambda y: y.pos[x], nanobots)), range(3)))
    ranges = tuple(map(lambda x, y: x - y, max_vals, min_vals))
    print(f"{ranges} -> {ranges[0]*ranges[1]*ranges[2]}")

    def generateNIntersectionGroups(
        n: int,
    ) -> Generator[tuple[NanoBot, ...], None, None]:

        assert n >= 2

        if n == 2:
            for c in itertools.combinations(nanobots, 2):
                if doNanoBotsIntersect(c[0], c[1]):
                    yield c
            return

        for c in generateNIntersectionGroups(n - 1):
            for b in nanobots:
                if b in c:
                    continue
                if all(map(lambda x: doNanoBotsIntersect(x, b), c)):
                    yield tuple(itertools.chain([b], c))

    # Not Working
    # print("Checking 999: {}".format(
    #     all(map(
    #         lambda x: doNanoBotsIntersect(x[0], x[1]),
    #         itertools.combinations(nanobots, 2),
    #     )),
    # ))

    # for i in range(2, len(nanobots)):
    #     has_intersection = False
    #     for c in generateNIntersectionGroups(i):
    #         print(f"An intersection exists for n={i}")
    #         assert(len(c) == i)
    #         has_intersection = True
    #         break
    #     if not has_intersection:
    #         print(f"No intersection exists for n={i}")
    #         break

    return (Part_1_Answer, Part_2_Answer)
