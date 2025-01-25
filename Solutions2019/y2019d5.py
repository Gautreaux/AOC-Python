from typing import Optional


from .IntcodeLib import IntcodeSolutionBase
from AOC_Lib.SolutionBase import Answer_T


class Solution_2019_05(IntcodeSolutionBase):
    """https://adventofcode.com/2019/day/5"""

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        runner = self._runner_factory()
        return runner.run_sync([1]).pop()

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        runner = self._runner_factory()
        return runner.run_sync([5]).pop()
