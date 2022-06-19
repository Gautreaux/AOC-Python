# from AOC_Lib.name import *

from collections import defaultdict
import itertools
from typing import Generator


class ElfGenerator:
    """Represents a elf"""

    def __init__(self, i:int, pt2:bool=False) -> None:
        self._i = i
        self._g = itertools.count(start=i, step=i)
        if pt2:
            self._g = itertools.islice(self._g, 50)
        self._n = None
        self.advance()

    def value(self) -> int:
        return self._i

    def next(self) -> int:
        return self._n
    
    def advance(self) -> None:
        self._n = next(self._g)


def generateHousePresents(pt2: bool = False) -> Generator[int, None, None]:
    """Generate the number of presents at each house, starting with house #1"""

    d = defaultdict(list)

    for i in itertools.count(1):
        # print("GEN: ", i)
        elf_list = d[i]
        elf_list.append(ElfGenerator(i, pt2=pt2))

        s = sum(map(lambda x: x.value(), elf_list))

        for elf in elf_list:
            try:
                elf.advance()
                d[elf.next()].append(elf)
            except StopIteration:
                pass
        
        if pt2:
            yield s*11
        else:
            yield s*10


def y2015d20(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d20.txt"
    print("2015 day 20:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    assert(len(lineList) == 1)

    target = int(lineList[0])

    for house_no, num_presents in enumerate(generateHousePresents(), start=1):
        if num_presents > target:
            Part_1_Answer = house_no
            break

    for house_no, num_presents in enumerate(generateHousePresents(pt2=True), start=1):
        if num_presents > target:
            Part_2_Answer = house_no
            break
    

    return (Part_1_Answer, Part_2_Answer)