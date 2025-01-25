
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.SlidingWindow import sliding_window

class Solution_2019_04(SolutionBase):
    """https://adventofcode.com/2019/day/4"""

    def __post_init__(self):
        """Runs Once After `__init__`"""
        
        l_str, _ ,u_str = self.input_str().partition('-')

        self.lower_bound = int(l_str)
        self.upper_bound = int(u_str)

    def is_valid_passcode(self, i: int) -> bool:
        """Return `True` iff this is a valid passcode"""
        s = str(i)

        if len(s) != 6:
            return False
        elif i < self.lower_bound:
            return False
        elif i > self.upper_bound:
            return False
        elif not any(map(
            lambda x: x[0] == x[1],
            sliding_window(s, 2),
        )):
            return False
        
        l = list(s)
        l.sort()
        return all(map(
            lambda x,y: x == y,
            l,
            s,
        ))

    def is_valid_passcode_pt2(self, i: int) -> bool:

        if not self.is_valid_passcode(i):
            return False
        
        s = str(i)
        if any(map(
            lambda x: x[0] != x[1] and x[1] == x[2] and x[2] != x[3],
            sliding_window(s, 4),
        )):
            return True

        # Check the edges where the pair is at the end
        if s[0] == s[1] and s[1] != s[2]:
            return True
        if s[-1] == s[-2] and s[-2] != s[-3]:
            return True
        return False

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return sum(1 for _ in filter(
            lambda x: self.is_valid_passcode(x),
            range(self.lower_bound, self.upper_bound+1),
        ))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        return sum(1 for _ in filter(
            lambda x: self.is_valid_passcode_pt2(x),
            range(self.lower_bound, self.upper_bound+1),
        ))
