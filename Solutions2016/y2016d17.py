# from AOC_Lib.name import *
from hashlib import md5
import queue


def y2016d17(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d17.txt"
    print("2016 day 17:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    baseKey = lineList[0]

    goal = (3, 3)

    q = queue.Queue()

    q.put(((0, 0), baseKey))

    def isDoorOpen(c):
        return c >= "a"

    while q.qsize() > 0:
        pos, path = q.get()

        if pos == goal:
            if Part_1_Answer is None:
                Part_1_Answer = path[len(baseKey) :]
                print(f"Part_1_Answer: {Part_1_Answer}")
                break
                Part_2_Answer = len(Part_1_Answer)

            k = len(path[len(baseKey) :])
            if k > Part_2_Answer:
                Part_2_Answer = k
                print(f"Found new part 2 answer {Part_2_Answer}, remaining {q.qsize()}")
            continue

        states = md5(path.encode("ascii")).hexdigest()

        # print(f"{pos} {path} {states[:4]}")

        if isDoorOpen(states[0]) and pos[1] != 0:
            q.put(((pos[0], pos[1] - 1), path + "U"))
        if isDoorOpen(states[1]) and pos[1] != 3:
            q.put(((pos[0], pos[1] + 1), path + "D"))
        if isDoorOpen(states[2]) and pos[0] != 0:
            q.put(((pos[0] - 1, pos[1]), path + "L"))
        if isDoorOpen(states[3]) and pos[0] != 3:
            q.put(((pos[0] + 1, pos[1]), path + "R"))

    # for multi line inputs

    return (Part_1_Answer, Part_2_Answer)
