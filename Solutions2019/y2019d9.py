from typing import Optional

from .IntcodeLib import IntcodeSolutionBase
from AOC_Lib.SolutionBase import Answer_T


class Solution_2019_09(IntcodeSolutionBase):
    """https://adventofcode.com/2019/day/9"""

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        runner = self._runner_factory()

        outputs = runner.run_sync([1])

        if len(outputs) != 1:
            print("Warning, problematic codes found:")
            print("Inst is done: ", runner.terminated())
            print("Out q empty: ", runner.getOutputQ().empty())
            for o in outputs:
                print(o)
            raise RuntimeError

        return outputs[0]

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        runner = self._runner_factory()

        outputs = runner.run_sync([2])
        if len(outputs) != 1:
            print(outputs)
            raise RuntimeError

        return outputs[0]
