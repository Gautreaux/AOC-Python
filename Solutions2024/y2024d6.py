# from AOC_Lib.name import *

from .y2024d4 import WordSearch


def turn_right(direction: tuple[int, int]) -> tuple[int, int]:
    if direction == (0, -1):
        return (1, 0)
    elif direction == (1, 0):
        return (0, 1)
    elif direction == (0, 1):
        return (-1, 0)
    elif direction == (-1, 0):
        return (0, -1)
    else:
        raise ValueError(f'Unrecognied Direction: {direction}')
    

def y2024d6(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2024/d6.txt"
    print("2024 day 6:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    ws = WordSearch(lineList)
    current_pos = next(ws.locate_character('^'))

    visited_pos = set()
    visited_pos.add(current_pos)

    direction = (0,-1)

    def next_position() -> tuple[int, int]:
        nonlocal current_pos
        nonlocal direction

        return (current_pos[0] + direction[0], current_pos[1] + direction[1])

    try:
        while True:
            np = next_position()
            n = ws.at(np)
            if n == '#':
                direction = turn_right(direction)
            else:
                current_pos = np
                visited_pos.add(current_pos)
    except IndexError:
        pass

    Part_1_Answer = len(visited_pos)

    

    return (Part_1_Answer, Part_2_Answer)