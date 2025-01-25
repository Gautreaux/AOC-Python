# from AOC_Lib.name import *

from collections import namedtuple
import itertools

Node_T = namedtuple("Node_T", "name size used avail used_pct")


def y2016d22(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d22.txt"
    print("2016 day 22:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    nodes: list[Node_T] = []

    for line in lineList[2:]:
        assert line.startswith("/dev/grid/")
        name, size, used, avail, used_pct = line.rpartition("/")[-1].split()
        assert size.endswith("T")
        assert used.endswith("T")
        assert avail.endswith("T")
        assert used_pct.endswith("%")
        nodes.append(
            Node_T(
                name=name,
                size=int(size[:-1]),
                used=int(used[:-1]),
                avail=int(avail[:-1]),
                used_pct=int(used_pct[:-1]),
            )
        )

    counter = 0

    for node_a, node_b in itertools.permutations(nodes, 2):
        if node_a.used == 0:
            continue
        if node_a == node_b:
            continue
        if node_a.used > node_b.avail:
            continue
        counter += 1

    Part_1_Answer = counter

    return (Part_1_Answer, Part_2_Answer)
