
from dataclasses import dataclass, field
import itertools
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


class Solution_{year}_{full_day}(SolutionBase):
    """https://adventofcode.com/{year}/day/{day}"""

    def __post_init__(self):
        """Runs Once After `__init__`"""
        
        for line in self.input_str_list(include_empty_lines=False):
            pass

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
