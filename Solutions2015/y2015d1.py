

from AOC_Lib.SolutionBase import SolutionBase


class Solution_2015_01(SolutionBase):
    """https://adventofcode.com/2015/day/1"""

    def __post_init__(self):
        """Runs Once After `__init__`"""
        
        depth = 0
        
        for i,c in enumerate(self.input_str().strip()):
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            else:
                raise ValueError(f"Unrecognized character: '{c}'")
            if depth < 0 and self._part_2_answer is None:
                self._part_2_answer = i+1
        self._part_1_answer = depth
