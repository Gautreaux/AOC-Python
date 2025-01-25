# from AOC_Lib.name import *


def y2021d7(inputPath=None):
    if inputPath == None:
        inputPath = "Input2021/d7.txt"
    print("2021 day 7:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    positions = list(map(int, lineList[0].split(",")))

    mi = min(positions)
    ma = max(positions)

    print((mi, ma))

    best_cost = None
    best_cost_2 = None

    steps_lookup = [0]
    while len(steps_lookup) < (ma + 2):
        steps_lookup.append(steps_lookup[-1] + len(steps_lookup))

    print(steps_lookup[:6])

    for i in range(mi, ma):
        total = 0
        total_2 = 0
        for p in positions:
            a = abs(i - p)
            total += a
            total_2 += steps_lookup[a]

        if i == 0:
            best_cost = total
            best_cost_2 = total_2
        else:
            if best_cost > total:
                best_cost = total
            if best_cost_2 > total_2:
                best_cost_2 = total_2

    Part_1_Answer = best_cost
    Part_2_Answer = best_cost_2

    return (Part_1_Answer, Part_2_Answer)
