# from AOC_Lib.name import *

from collections import defaultdict
import itertools
from operator import ne
from typing import Generator, Iterable


Component_T = tuple[int, int]


def generatePossibleComponents(
    last_val: int, components: Iterable[Component_T]
) -> Generator[Component_T, None, None]:
    """Generate the possible next_components"""
    for c in components:
        if c[0] == last_val or c[1] == last_val:
            yield c


def generatePossibleBridges(
    start_val: int, components: Iterable[Component_T]
) -> Generator[Component_T, None, None]:
    """Generate possible bridges starting with start_val"""
    l = list(components)


def y2017d24(inputPath=None):
    if inputPath == None:
        inputPath = "Input2017/d24.txt"
    print("2017 day 24:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    components: list[Component_T] = list(
        map(lambda x: tuple(map(int, x.split("/"))), lineList)
    )

    assert len(components) == len(set(components))

    unique_vals = set(itertools.chain.from_iterable(components))

    print(
        f"There are {len(components)} total components and {len(unique_vals)} unique vals:",
        unique_vals,
    )

    # build a graph representation
    adj_lists = defaultdict(list)

    for a, b in components:
        adj_lists[a].append(b)
        adj_lists[b].append(a)

    # check if there are any cycles

    return (Part_1_Answer, Part_2_Answer)
