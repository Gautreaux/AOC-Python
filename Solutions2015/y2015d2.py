from typing import Iterator, Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


class Solution_2015_02(SolutionBase):
    """https://adventofcode.com/2015/day/2"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.dimensions: list[tuple[int, int, int]] = []

        for line in self.input_str_list(include_empty_lines=False):
            x, y, z = line.split("x")
            self.dimensions.append((int(x), int(y), int(z)))

    def iter_faces(self) -> Iterator[tuple[int, int, int]]:
        """Iterate the dimensions as faces"""
        for d in self.dimensions:
            yield (d[0] * d[1], d[1] * d[2], d[2] * d[0])

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return sum(map(lambda f: 2 * sum(f) + min(f), self.iter_faces()))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        return sum(
            map(
                lambda d: 2 * (sum(d) - max(d)) + (d[0] * d[1] * d[2]),
                self.dimensions,
            )
        )
