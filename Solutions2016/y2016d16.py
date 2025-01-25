"""https://adventofcode.com/2016/day/16"""

import itertools
from AOC_Lib.SolutionBase import SolutionBase


class Solution_2016_16(SolutionBase):
    """https://adventofcode.com/2016/day/16"""

    # Lengths given in the problem statement
    FIRST_DISK_LENGTH = 272
    SECOND_DISK_LENGTH = 35651584

    @staticmethod
    def do_one_round(begin: str) -> str:
        """Do one round of filling"""
        b = reversed(begin)
        b = map(lambda x: "0" if x == "1" else "1", b)
        return "".join(itertools.chain(begin, "0", b))

    @staticmethod
    def checksum(s: str):
        """Compute the checksum of `s`"""

        if len(s) % 2 == 1:
            return s

        l = []

        try:
            for i in range(len(s)):
                l.append("1" if s[i * 2] == s[i * 2 + 1] else "0")
        except IndexError:
            pass

        c = "".join(l)

        return Solution_2016_16.checksum(c)

    def __post_init__(self):
        """Runs Once After `__init__`"""

        b = self.input_str()

        while len(b) < self.FIRST_DISK_LENGTH:
            b = self.do_one_round(b)

        self._part_1_answer = self.checksum(b[: self.FIRST_DISK_LENGTH])

        while len(b) < self.SECOND_DISK_LENGTH:
            b = self.do_one_round(b)

        self._part_2_answer = self.checksum(b[: self.SECOND_DISK_LENGTH])
