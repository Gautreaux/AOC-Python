# from AOC_Lib.name import *

from collections import namedtuple
from typing import Generator

Reindeer = namedtuple("Reindeer", "name speed duration rest")

_REST = 0
_MOVE = 1

def ReindeerActionGenerator(reindeer: Reindeer) -> Generator[int, None, None]:
    """Return either rest or move action for this turn
        assumes starts fully rested and moves until exhausted
    """
    while True:
        for _ in range(reindeer.duration):
            yield _MOVE
        
        for _ in range(reindeer.rest):
            yield _REST


def ReindeerPositionGenerator(reindeer: Reindeer, step: int = 1) -> Generator[tuple[int, int], None, None]:
    """Yield the position of the reindeer at multiples of `step` resolution
        yield type is tuples of (time, position)
    """
    position = 0
    next_report = step

    for time, action in enumerate(ReindeerActionGenerator(reindeer), start=1):
        if action == _MOVE:
            position += reindeer.speed

        if time == next_report:
            yield (time, position)
            next_report += step


def getPositionAtTime(reindeer: Reindeer, time:int) -> int:
    """Get the reindeer position at a given time"""
    for t,p in ReindeerPositionGenerator(reindeer, step=time):
        assert(t == time)
        return p


def generateGroupPositions(reindeer_list: Reindeer, step: int = 1) -> Generator[tuple[int, tuple[int]], None, None]:
    """Same a ReindeerPositionGenerator but for a group"""

    generators = list(map(lambda x: ReindeerPositionGenerator(x), reindeer_list))

    for gt in zip(*generators):
        positions = tuple(map(lambda x: x[1], gt))
        yield (gt[0][0], positions)


def y2015d14(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d14.txt"
    print("2015 day 14:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    reindeer_list: list[Reindeer] = []

    for line in lineList:
        s = line.split(" ")

        reindeer_list.append(Reindeer(s[0], int(s[3]), int(s[6]), int(s[-2])))

    Part_1_Answer = max(map(lambda x: getPositionAtTime(x, 2503), reindeer_list))

    points_chart = [0]*len(reindeer_list)

    for t,p in generateGroupPositions(reindeer_list):
        m = max(p)
        for i,pos in enumerate(p):
            if pos == m:
                points_chart[i] += 1

        if t >= 2503:
            break
    
    Part_2_Answer = max(points_chart)

    return (Part_1_Answer, Part_2_Answer)