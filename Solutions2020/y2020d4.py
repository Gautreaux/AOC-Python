# from AOC_Lib.name import *


from typing import List, Tuple
from AOC_Lib.charSets import CHARSET_DIGITS, CHARSET_HEXADECIMAL_LOWER


def groupByEmptyLines(lineList: List[str]) -> Tuple[List[str], List[int]]:
    """concats lines (without newlines) into returnLine"""
    returnLine = []
    returnCount = []
    tempLine = ""
    tempCount = 0
    for line in lineList:
        if line == "":
            returnLine.append(tempLine.strip())
            returnCount.append(tempCount)
            tempLine = ""
            tempCount = 0
        else:
            tempLine += line + " "
            tempCount += 1
    return (returnLine, returnCount)


# moved out b/c I think this one is coming back
eclList = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def isIntInRange(v: str, lowerBound: int, upperBound: int) -> bool:
    try:
        i = int(v)
    except ValueError:
        return False

    return i >= lowerBound and i <= upperBound


def hgtValid(v):
    try:
        i = int(v[:-2])
    except ValueError:
        return False
    u = v[-2:]

    if u == "cm":
        return i >= 150 and i <= 193
    elif u == "in":
        return i >= 59 and i <= 76
    else:
        return False


def hclValid(v):
    if len(v) != 7:
        return False

    if v[0] != "#":
        return False

    for c in v[1:]:
        if c not in CHARSET_HEXADECIMAL_LOWER:
            return False
    return True


def eclValid(v):
    if len(v) != 3:
        return False

    return v in eclList


def pidValid(v):
    if len(v) != 9:
        return False
    for c in v:
        if c not in CHARSET_DIGITS:
            return False
    return True


def checkValid(passport: str) -> int:
    # returns 0 if invalid
    #   1 if part 1 valid and not part 2 valid
    #   2 if part 2 valid

    expected = {
        "byr": 1,
        "iyr": 1,
        "eyr": 1,
        "hgt": 1,
        "hcl": 1,
        "ecl": 1,
        "pid": 1,
        "cid": 0,
    }

    # function pointers to the checker functions
    checkers = {
        "byr": lambda x: isIntInRange(x, 1920, 2002),
        "iyr": lambda x: isIntInRange(x, 2010, 2020),
        "eyr": lambda x: isIntInRange(x, 2020, 2030),
        "hgt": hgtValid,
        "hcl": hclValid,
        "ecl": eclValid,
        "pid": pidValid,
    }

    allFieldsValid = True

    while passport.find("  ") != -1:
        passport.replace("  ", " ")
    fields = passport.strip().split(" ")
    for f in fields:
        e = f.split(":")

        k = e[0]
        v = e[1]

        if k == "cid":
            continue
        else:
            if k in expected:
                if checkers[k](v) is False:
                    allFieldsValid = False
                expected[k] -= 1
            else:
                return False

    t = sum(map(lambda x: x[1], expected.items())) == 0

    return 0 if t is False else (2 if allFieldsValid is True else 1)


def y2020d4(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d4.txt"
    print("2020 day 4:")

    Part_1_Answer = 0
    Part_2_Answer = 0
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    lineList.append("")

    groupedLines, _ = groupByEmptyLines(lineList)
    numGroups = len(groupedLines)

    for passport in groupedLines:
        # print(passport)
        k = checkValid(passport)
        if k == 1:
            Part_1_Answer += 1
        elif k == 2:
            Part_1_Answer += 1
            Part_2_Answer += 1

    return (Part_1_Answer, Part_2_Answer)
