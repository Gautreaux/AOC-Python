from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.SlidingWindow import sliding_window


class Solution_2022_06(SolutionBase):
    """https://adventofcode.com/2022/day/6"""

    def _find_first_n_unique_sequence(self, size: int) -> int:
        """Find and return the start index of the first sequence of `size` characters in input"""

        for start_index, window in enumerate(
            sliding_window(self.input_str().strip(), size)
        ):
            if len(set(window)) == size:
                return start_index
        raise RuntimeError()

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        # + 3 to get the last character
        # + 1 to adjust to ones-based indexing
        return self._find_first_n_unique_sequence(4) + 3 + 1

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        # + 13 to get the last character
        # +  1 to adjust to ones-based indexing
        return self._find_first_n_unique_sequence(14) + 13 + 1
