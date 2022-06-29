# from AOC_Lib.name import *


class ElfCircle:
    def __init__(self, qty: int) -> None:
        # can use disjoint sets to quickly skip empty parts
        
        l = [-1]*(qty+2)

        for x in range(1, qty + 1):
            l[x] = x+1 
        l[qty] = 1
        self._next_list = l
        self._num_with_presents = qty
        self._start_qty = qty

    @property
    def initial_elves(self) -> int:
        """Return the number of elves we started with"""
        return self._start_qty

    def __len__(self) -> int:
        """Return the number of elves that remain"""
        return self._num_with_presents

    def _getNext(self, elf:int) -> int:
        """Get the next elf for a given elf"""
        to_compress = []
        a = self._next_list[elf]

        while a < 0:
            to_compress.append(-a)
            a = self._next_list[-a]
        for x in to_compress:
            self._next_list[-x] = a
        return a

    def _removeElf(self, elf:int) -> None:
        """Remove the given elf"""
        n = self._next_list[elf]
        if n > 0:
            self._next_list[elf] = -n
        else:
            self._next_list[elf] = -self._getNext(n)
        self._num_with_presents -= 1

    def Play(self, start_elf: int = 1) -> int:
        """Play a game where each steals from the next (Part 1),
            and return the winning elf
        """
        # check the elf index is valid
        assert(start_elf >= 1 and start_elf <= self._start_qty)
        active = start_elf

        while len(self) > 1:
            next_elf = self._getNext(active)
            self._removeElf(next_elf)
            active = self._getNext(active)
        return active

def y2016d19(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d19.txt"
    print("2016 day 19:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    number_elves = int(lineList[-1])

    ec = ElfCircle(number_elves)
    return (None, None)
    Part_1_Answer = ec.Play()

    # this doesnt actually work:
    #   its very easy to end up in a cyclic problem
    #   where you point to yourself, 
    # There is definetly some optimization from disjoint sets
    #   but I just can't make it work ...

    return (Part_1_Answer, Part_2_Answer)