# from AOC_Lib.name import *

from typing import Iterable, Generator

def y2017d9(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d9.txt"
    print("2017 day 9:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    assert(len(lineList) == 1)


    # Total characters trashed
    trash_counter = 0

    def withoutTrash(itr: Iterable[str]) -> Generator[str, None, None]:
        """Generate the line with all trash removed"""
        nonlocal trash_counter
        in_trash = False

        for c in itr:
            if c == '!':
                # trash the next character
                next(itr)
            elif c == '<':
                if in_trash:
                    trash_counter += 1
                else:
                    in_trash = True
            elif c == '>':
                in_trash = False
            elif in_trash:
                trash_counter += 1
            else:
                yield c

    no_trash = withoutTrash(iter(lineList[0]))

    total_score = 0
    depth = 1

    for c in no_trash:
        if c == "{":
            total_score += depth
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == ',':
            pass
        else:
            raise RuntimeError(f"Unexpected character: `{c}`")

    Part_1_Answer = total_score
    Part_2_Answer = trash_counter

    return (Part_1_Answer, Part_2_Answer)