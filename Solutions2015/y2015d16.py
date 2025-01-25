# from AOC_Lib.name import *


def y2015d16(inputPath=None):
    if inputPath == None:
        inputPath = "Input2015/d16.txt"
    print("2015 day 16:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    known_true = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    part_2_true = {
        "children": (lambda x: x == 3),
        "cats": (lambda x: x > 7),
        "samoyeds": (lambda x: x == 2),
        "pomeranians": (lambda x: x < 3),
        "akitas": (lambda x: x == 0),
        "vizslas": (lambda x: x == 0),
        "goldfish": (lambda x: x < 5),
        "trees": (lambda x: x > 3),
        "cars": (lambda x: x == 2),
        "perfumes": (lambda x: x == 1),
    }

    candidates = []
    pt2_candidates = []

    for line in lineList:
        tokens = line.split(" ")
        sue_number = int(tokens[1][:-1])

        assert len(tokens) % 2 == 0

        this_sue = {}
        for i in range(2, len(tokens), 2):
            key = tokens[i][:-1]
            value = int(tokens[i + 1].strip().replace(",", ""))
            this_sue[key] = value

        if all(map((lambda x: known_true[x[0]] == x[1]), this_sue.items())):
            candidates.append(sue_number)

        if all(map((lambda x: part_2_true[x[0]](x[1])), this_sue.items())):
            pt2_candidates.append(sue_number)

    # print(candidates)
    assert len(candidates) == 1
    Part_1_Answer = candidates[0]
    assert len(pt2_candidates) == 1
    Part_2_Answer = pt2_candidates[0]

    return (Part_1_Answer, Part_2_Answer)
