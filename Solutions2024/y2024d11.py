from functools import cache
from typing import  Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@cache
def simulate_stone_count(stone: int, blinks: int) -> int:
    """Simulate the count of number of stones after the given number of blinks"""
    if blinks <= 0:
        return 1

    s_str = str(stone)
    if stone == 0:
        return simulate_stone_count(1, blinks - 1)

    if len(s_str) % 2 == 0:
        midpoint = len(s_str) // 2
        return simulate_stone_count(
            int(s_str[midpoint:]), blinks - 1
        ) + simulate_stone_count(int(s_str[:midpoint]), blinks - 1)

    return simulate_stone_count(stone * 2024, blinks - 1)


class Solution_2024_11(SolutionBase):
    """https://adventofcode.com/2024/day/11"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.input_stones: list[int] = list(map(int, self.input_str().split()))

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return sum(simulate_stone_count(stone, 25) for stone in self.input_stones)

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        return sum(simulate_stone_count(stone, 75) for stone in self.input_stones)
