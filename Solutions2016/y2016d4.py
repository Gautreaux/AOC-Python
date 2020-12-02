# from AOC_Lib.name import *

import re
from typing import ItemsView

from AOC_Lib.boundedInt import BoundedInt

REGEX_STR = "([a-z\-]*)-([0-9]*)\[([a-z]{5})\]"

# sample variant for reading data from an input file, line by line
def y2016d4(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d4.txt"
    print("2016 day 4:")

    Part_1_Answer = 0
    Part_2_Answer = None

    with open(inputPath) as f:
        for line in f:
            line = line.strip()

            x = re.search(REGEX_STR, line)

            if x is None:
                raise RuntimeError(f"Regex failed on line '{line}'")
            name = x.group(1)
            sectorID = int(x.group(2))
            csum = x.group(3)

            occurrences = {}

            for c in name:
                if c == '-':
                    continue
                if c not in occurrences:
                    occurrences[c] = 1
                else:
                    occurrences[c] += 1
            
            itemList = list(occurrences.items())
            if(len(itemList) < 5):
                continue

            itemList.sort(key=lambda x:-x[1] + (ord(x[0]) - ord('a'))/26)
            
            isValid = True
            for i in range(5):
                if itemList[i][0] != csum[i]:
                    isValid = False
                    break
            
            if isValid:
                Part_1_Answer += sectorID

            # part 2:
            partialName = ""
            for c in name:
                if c == '-':
                    partialName += "-"
                    continue
                i = BoundedInt(ord('z')-ord('a')+1, value=ord(c) - ord('a'))
                newI = i + sectorID
                partialName += (chr(newI.asInt() + ord('a')))

            if partialName == "northpole-object-storage":
                assert(Part_2_Answer == None)
                Part_2_Answer = sectorID
        
    return (Part_1_Answer, Part_2_Answer)