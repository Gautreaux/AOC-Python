# from AOC_Lib.name import *
import itertools
from collections import defaultdict

def y2021d5(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d5.txt"
    print("2021 day 5:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    starts = []
    ends = []

    for l in lineList:
        s,_,e = l.partition(" -> ")
        a,b = s.split(",")
        starts.append((int(a), int(b)))
        a,b = e.split(",")
        ends.append((int(a), int(b)))

    # min_x = min(map(lambda x: x[0], itertools.chain(starts, ends)))
    # max_x = max(map(lambda x: x[0], itertools.chain(starts, ends)))
    # min_y = min(map(lambda x: x[1], itertools.chain(starts, ends)))
    # max_y = max(map(lambda x: x[1], itertools.chain(starts, ends)))

    counter = defaultdict(int)

    for start, end in zip(starts, ends):
        if start[0] == end[0]:
            # vertical
            for i in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                counter[(start[0], i)] += 1
        elif start[1] == end[1]:
            # horizontal
            for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                counter[(i, start[1])] += 1
        else:
            pass

    Part_1_Answer = sum(map(lambda x: 1 if x >=2 else 0, counter.values()))

    for start, end in zip(starts, ends):
        if abs(start[0] - end[0]) == abs(start[1] - end[1]):
            # diagonals
            s = start if start[0] < end[0] else end
            e = end if start[0] < end[0] else start

            is_down = s[1] > e[1]

            if is_down:
                itr = range(s[1], e[1] -1, -1)
            else:
                itr = range(s[1], e[1] + 1)

            for a in zip(range(s[0], e[0] + 1), itr):
                counter[a] += 1

            # print(f"{start} -> {end}")
        else:
            pass

    Part_2_Answer = sum(map(lambda x: 1 if x >=2 else 0, counter.values()))

    return (Part_1_Answer, Part_2_Answer)