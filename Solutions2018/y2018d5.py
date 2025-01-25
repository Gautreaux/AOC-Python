# from AOC_Lib.name import *

from os import pardir
from AOC_Lib.charSets import ALPHABET_LOWER, ALPHABET_UPPER


class ContinueException(Exception):
    pass


def oppCaseEqual(c0, c1) -> bool:
    if ord(c0) + 32 == ord(c1):
        # print(f"{c0} {c1}")
        return True
    if ord(c0) - 32 == ord(c1):
        # print(f"{c0} {c1}")
        return True
    return False


def reactPolymer(s: str) -> str:
    pieces = []
    index = 0
    while index < len(s):
        try:
            if oppCaseEqual(s[index], s[index + 1]):
                raise ContinueException()

            pieces.append(s[index])
            index += 1
        except ContinueException:
            index += 2
            pass
        except IndexError:
            pieces.append(s[index])
            index += 1

    return "".join(pieces)


def reactPolymerFully(s: str) -> str:
    last = ""
    now = s

    while last != now:
        last = now
        now = reactPolymer(last)
        # print(len(now))
    return now


def y2018d5(inputPath=None):
    if inputPath == None:
        inputPath = "Input2018/d5.txt"
    print("2018 day 5:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    startingPolymer = lineList[-1]

    Part_1_Answer = len(reactPolymerFully(startingPolymer))

    units = []

    for i in startingPolymer:
        c = i if (i in ALPHABET_UPPER) else i.upper()
        if c not in units:
            units.append(c)

    Part_2_Answer = len(startingPolymer)
    for c in units:
        print(f"Removing {c}")
        newPolymer = startingPolymer.replace(c, "").replace(c.lower(), "")
        newReact = reactPolymerFully(newPolymer)
        newLen = len(newReact)
        Part_2_Answer = min(Part_2_Answer, newLen)

    return (Part_1_Answer, Part_2_Answer)
