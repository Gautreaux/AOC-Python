# from AOC_Lib.name import *

import re

SEARCH_STR = "([0-9]*)-([0-9]*) ([a-z]): ([a-z]*)"

# sample variant for reading data from an input file, line by line


def y2020d2(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d2.txt"
    print("2020 day 2:")

    Part_1_Answer = 0
    Part_2_Answer = 0

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            x = re.search(SEARCH_STR, line)

            assert x != None

            minC = int(x.group(1))
            maxC = int(x.group(2))
            char = x.group(3)
            word = x.group(4)

            c = sum(map(lambda x: 1 if x == char else 0, word))
            # c = len(list(filter(lambda x: x == char, word)))

            if c >= minC and c <= maxC:
                Part_1_Answer += 1

            if (word[minC - 1] == char) ^ (word[maxC - 1] == char):
                Part_2_Answer += 1

                # NOT - 149

    return (Part_1_Answer, Part_2_Answer)
