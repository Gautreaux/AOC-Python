# from AOC_Lib.name import *

from collections import defaultdict, deque
from typing import Generator

def generatePositions(s) -> Generator[tuple[tuple[int,int], tuple[int,int]], None, None]:
    x = 0
    y = 0

    rollback_pos = []

    for c in s:
        if c == "^":
            continue
        elif c == "$":
            continue
        elif c == "E":
            x += 1
            yield ((x-1,y), (x,y))
        elif c == "W":
            x -= 1
            yield ((x+1,y), (x,y))
        elif c == "N":
            y -= 1
            yield ((x,y+1), (x,y))
        elif c == "S":
            y += 1
            yield ((x,y-1), (x,y))
        elif c == "|":
            x,y = rollback_pos[-1]
        elif c == "(":
            rollback_pos.append((x,y))
        elif c == ")":
            x,y=rollback_pos.pop()
        else:
            raise RuntimeError(f"Did not recognize character: `{c}`")


def y2018d20(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d20.txt"
    print("2018 day 20:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    adj_map = defaultdict(list)

    for a,b in list(generatePositions(lineList[-1])):
        adj_map[a].append(b)
        adj_map[b].append(a)
    
    # now the search

    visited = {}
    frontier = deque()
    frontier.append(((0,0), 0))
    visited[(0,0)] = 0
    furthest_depth = 0

    while frontier:
        this_pos, this_depth = frontier.popleft()

        furthest_depth = max(furthest_depth, this_depth)

        for neighbor in adj_map[this_pos]:
            if neighbor not in visited:
                visited[neighbor] = this_depth + 1
                frontier.append((neighbor, this_depth+1))

    Part_1_Answer = furthest_depth

    # part 2

    Part_2_Answer = sum(1 for x in visited.values() if x >= 1000)

    return (Part_1_Answer, Part_2_Answer)