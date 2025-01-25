# from AOC_Lib.name import *

from typing import Generator


def pt1GenGeneric(s: str, i: int):
    pieces = s.replace("[", "]").split("]")
    for ii in range(i, len(pieces), 2):
        yield pieces[ii]


def genIPV7Segments(s: str) -> Generator[str, None, None]:
    return pt1GenGeneric(s, 0)


def genHypernetSequences(s: str) -> Generator[str, None, None]:
    return pt1GenGeneric(s, 1)


def containsABBA(s: str) -> bool:
    if len(s) < 4:
        return False
    for i in range(len(s) - 3):
        if s[i] == s[i + 3] and s[i + 1] == s[i + 2] and s[i] != s[i + 1]:
            return True
    return False


def pt2GenGeneric(s: str, gen):
    for k in gen(s):
        if len(k) < 3:
            continue
        for i in range(len(k) - 2):
            if k[i] == k[i + 2] and k[i] != k[i + 1]:
                yield k[i : i + 3]


def genABA(s: str) -> Generator[str, None, None]:
    return pt2GenGeneric(s, genIPV7Segments)


def genBAB(s: str) -> Generator[str, None, None]:
    return pt2GenGeneric(s, genHypernetSequences)


class BreakContinue(Exception):
    pass


def y2016d7(inputPath=None):
    if inputPath == None:
        inputPath = "Input2016/d7.txt"
    print("2016 day 7:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    Part_1_Answer = 0
    for line in lineList:
        try:
            for h in genHypernetSequences(line):
                if containsABBA(h):
                    raise BreakContinue()

            for h in genIPV7Segments(line):
                if containsABBA(h):
                    Part_1_Answer += 1
                    break
        except BreakContinue:
            pass

    # print(list(genIPV7Segments(lineList[0])))
    # print(list(genHypernetSequences(lineList[0])))

    assert Part_1_Answer < 108

    Part_2_Answer = 0
    for line in lineList:
        aba = list(genABA(line))
        bab = list(genBAB(line))

        for a in aba:
            if f"{a[1]}{a[0]}{a[1]}" in bab:
                Part_2_Answer += 1

                # print(line)
                # print(list(genIPV7Segments(line)))
                # print(list(genHypernetSequences(line)))
                # print(aba)
                # print(bab)
                break

    assert Part_2_Answer != 51

    return (Part_1_Answer, Part_2_Answer)
