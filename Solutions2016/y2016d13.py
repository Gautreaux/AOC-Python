# from AOC_Lib.name import *

from AOC_Lib.queue import CircularQueue


def y2016d13(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d13.txt"
    print("2016 day 13:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    favorite_number = int(lineList[0])

    def isWall(x, y):
        c = x * x + 3 * x + 2 * x * y + y + y * y + favorite_number
        b = "{0:b}".format(c)
        o = sum(map(lambda x: 1 if x == "1" else 0, b))
        return (o % 2) == 1

    target = (31, 39)

    layout = {}
    subFiftySet = set()

    # just do a BFS
    q = CircularQueue(maxSize=100000)

    q.push(((1, 1), 0))

    transforms = [
        lambda x: (x[0] - 1, x[1]),
        lambda x: (x[0] + 1, x[1]),
        lambda x: (x[0], x[1] - 1),
        lambda x: (x[0], x[1] + 1),
    ]

    def isValidPos(p):
        return p[0] >= 0 and p[1] >= 0

    while Part_1_Answer is None:
        if len(q) == 0:
            raise RuntimeError("Queue emptied without finding goal")

        pos, dist = q.pop()

        if pos == target:
            Part_1_Answer = dist
            break

        if pos in layout:
            assert layout[pos] <= dist
            continue

        layout[pos] = dist
        if dist <= 50:
            subFiftySet.add(pos)

        for t in transforms:
            newPos = t(pos)
            if not isValidPos(newPos):
                continue
            if isWall(*newPos):
                continue
            if newPos in layout:
                continue
            q.push((newPos, dist + 1))

    if Part_1_Answer < 50:
        raise RuntimeError("Incorrect part 2 answer cause part 1 ended too soon")

    Part_2_Answer = len(subFiftySet)

    return (Part_1_Answer, Part_2_Answer)
