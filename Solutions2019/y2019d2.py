from typing import Optional

from AOC_Lib.SolutionBase import Answer_T
from .IntcodeLib import *


class Solution_2019_02(IntcodeSolutionBase):
    """https://adventofcode.com/2019/day/2"""

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        runner = self._runner_factory()
        runner.setAddr(1, 12)
        runner.setAddr(2, 2)

        runner.run_sync()

        return runner.readAddr(0)

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        target_value = 19690720

        # TODO - multiprocess if slow
        for noun in range(100):
            for verb in range(100):
                runner = self._runner_factory()
                runner.setAddr(1, noun)
                runner.setAddr(2, verb)

                runner.run_sync()

                v = runner.readAddr(0)

                if v == target_value:
                    return 100 * noun + verb
