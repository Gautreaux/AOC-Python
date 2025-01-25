# from AOC_Lib.name import *

from copy import copy
import functools
import itertools
from math import lcm
from typing import Any

# TODO - include Cycle and Remainder


def _swap(l: list[Any], i: int, j: int) -> None:
    t = l[i]
    l[i] = l[j]
    l[j] = t


def getNextState(positions: list[str], instructions: list[str]) -> list[str]:
    """Get the next state from the current state"""
    positions = copy(positions)
    for instruction in instructions:
        if instruction[0] == "s":
            i = int(instruction[1:])
            assert i in range(0, 16)
            positions = positions[-i:] + positions[:-i]

        elif instruction[0] == "x":
            a, b = instruction.split("/")
            i = int(a[1:])
            j = int(b)
            _swap(positions, i, j)
        elif instruction[0] == "p":
            a = instruction[1]
            b = instruction[3]
            i = positions.index(a)
            j = positions.index(b)
            _swap(positions, i, j)
        else:
            raise RuntimeError(f"Unrecognized instruction: `{instruction}`")
    return positions


def y2017d16(inputPath=None):
    if inputPath == None:
        inputPath = "Input2017/d16.txt"
    print("2017 day 16:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    assert len(lineList) == 1

    instructions = lineList[0].split(",")

    start_pos = list(map(chr, range(ord("a"), ord("q"))))
    assert len(start_pos) == 16
    one_pos = getNextState(start_pos, instructions)

    Part_1_Answer = "".join(one_pos)

    # Part 2

    # build jump map

    pos_jumps = {}

    for i in range(16):
        c = start_pos[i]
        e = one_pos.index(c)
        pos_jumps[i] = e

    print(pos_jumps)

    # check no duplicates
    assert len(set(pos_jumps.keys())) == 16

    # find the loop sizes
    loops = []

    for i in range(16):
        if i in itertools.chain.from_iterable(loops):
            continue

        this_loop = [i]

        while True:
            n = pos_jumps[this_loop[-1]]
            if n in this_loop:
                break
            else:
                this_loop.append(n)
        loops.append(this_loop)

    # and get the period size
    period = functools.reduce(lambda x, y: lcm(x, y), map(len, loops))

    print(
        "There are {} total loops: {} (len: {}); Period is {}".format(
            len(loops),
            loops,
            list(map(len, loops)),
            period,
        )
    )

    # TODO - this is a general-ish pattern
    #   can we abstract it somehow

    TARGET = 1000000000

    cycles = TARGET // period
    remainder = TARGET % period

    print(f"Completes after {cycles} cycles and {remainder} remainder")

    positions = [start_pos]

    # this is dumb but funny
    while True:
        print(len(positions))
        try:
            Part_2_Answer = "".join(positions[period + 1])
            break
        except IndexError:
            positions.append(getNextState(positions[-1], instructions))

    for p in positions:
        print("\t{}".format("".join(p)))

    return (Part_1_Answer, Part_2_Answer)
