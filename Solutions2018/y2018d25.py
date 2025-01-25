import itertools
from AOC_Lib.DisjointSets import DisjointSets


def manhattanDistance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    """Get the manhattan distance between points"""
    assert len(a) == len(b)
    return sum(map(lambda x, y: abs(x - y), a, b))


def y2018d25(inputPath=None):
    if inputPath == None:
        inputPath = "Input2018/d25.txt"
    print("2018 day 25:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    all_points = []

    for line in lineList:
        all_points.append(tuple(map(int, line.split(","))))

    print(f"There are {len(all_points)} points in consideration")
    print(f"  That is {len(all_points)*(len(all_points)-1)} all pairs")

    sets = DisjointSets(initial=all_points, allow_insert=False)

    for a, b in itertools.combinations(all_points, r=2):
        if manhattanDistance(a, b) <= 3:
            sets.union(a, b)

    Part_1_Answer = len(sets)

    return (Part_1_Answer, Part_2_Answer)
