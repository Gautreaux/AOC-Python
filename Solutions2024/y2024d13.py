# from AOC_Lib.name import *
from dataclasses import dataclass
from typing import Iterator
import re


@dataclass(frozen=True)
class ClawMachine:
    """A Claw Machine"""

    button_a_x: int
    button_a_y: int
    button_b_x: int
    button_b_y: int
    prize_x: int
    prize_y: int

    @staticmethod
    def parse(lines: tuple[str, str, str]) -> "ClawMachine":
        """Parse the claw machine from the input lines"""
        a_x, a_y = map(int, re.findall(r"(\d+)", lines[0]))
        b_x, b_y = map(int, re.findall(r"(\d+)", lines[1]))
        p_x, p_y = map(int, re.findall(r"(\d+)", lines[2]))

        return ClawMachine(a_x, a_y, b_x, b_y, p_x, p_y)

    def _is_valid_solution(self, a_presses: int, b_presses: int) -> bool:
        """Return true iff the given number of a_presses and b_presses will result over the prize"""
        return (
            ((self.button_a_x * a_presses) + (self.button_b_x * b_presses))
            == self.prize_x
        ) and (
            ((self.button_a_y * a_presses) + (self.button_b_y * b_presses))
            == self.prize_y
        )

    def generate_possible_solutions(self) -> Iterator[tuple[int, int]]:
        """Generate possible solutions for the a and b presses"""

        # Try the a values
        for a in range(0, 101):
            total_x = self.button_a_x * a
            remain_x = self.prize_x - total_x
            if remain_x < 0:
                # Too much A; No point in checking others
                break

            if not (remain_x % self.button_b_x == 0):
                # We cannot get to the prize with an integer number of b
                continue

            b_x = remain_x // self.button_b_x

            total_y = self.button_a_y * a
            remain_y = self.prize_y - total_y
            if remain_y < 0:
                # Too much A; No point in checking others
                break

            if not (remain_y % self.button_b_y == 0):
                # We cannot get to the prize with an integer number of b
                continue

            b_y = remain_y // self.button_b_y

            if b_x == b_y:
                if b_x > 100:
                    # too many presses
                    continue
                else:
                    assert self._is_valid_solution(a, b_x)
                    yield (a, b_x)

    def find_lowest_token_solution(self) -> tuple[tuple[int, int], int] | None:
        """Find the cheapest solution; Return a tuple of (tuple(a_presses, b_presses), token_count)"""
        best_solution = None
        for solution in self.generate_possible_solutions():
            cost = solution[0] + solution[1]
            if best_solution is None:
                best_solution = (solution, cost)
            elif cost < best_solution[1]:
                best_solution = (solution, cost)
        return best_solution

    def find_cheapest_solution(
        self, cost_per_a: int = 3, cost_per_b: int = 1
    ) -> tuple[tuple[int, int], int] | None:
        """Find the cheapest solution; Return a tuple of (tuple(a_presses, b_presses), cost)"""
        best_solution = None
        for solution in self.generate_possible_solutions():
            cost = cost_per_a * solution[0] + cost_per_b * solution[1]
            if best_solution is None:
                best_solution = (solution, cost)
            elif cost < best_solution[1]:
                best_solution = (solution, cost)
        return best_solution


def _group_input_lines(lines: Iterator[str]) -> Iterator[tuple[str, str, str]]:
    """Try and group the input lines"""
    itr = iter(lines)

    while True:
        try:
            ln1 = ""
            while not ln1:
                ln1 = next(itr)
        except StopIteration:
            return

        try:
            ln2 = next(itr)
            ln3 = next(itr)
        except StopIteration:
            raise ValueError("Improper number of lines read") from None

        if not ln2:
            raise ValueError("ln2 is unexpectedly empty")
        if not ln3:
            raise ValueError("ln3 is unexpectedly empty")

        yield (ln1, ln2, ln3)


def _assert_sample_passes():
    s1 = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400
""".splitlines()
    
    t = tuple(s1)
    assert len(t) == 3

    cm = ClawMachine.parse(t)

    # Assert some solution is found
    assert sum(1 for _ in cm.generate_possible_solutions())
    assert cm.find_cheapest_solution()[1] == 280

    s2 = """Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176
""".splitlines()

    cm = ClawMachine.parse(s2)

    # Assert no solution is found
    assert sum(1 for _ in cm.generate_possible_solutions()) == 0


def y2024d13(inputPath=None):
    if inputPath == None:
        inputPath = "Input2024/d13.txt"
    print("2024 day 13:")

    _assert_sample_passes()

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    machines: list[ClawMachine] = []
    for g in _group_input_lines(lineList):
        machines.append(ClawMachine.parse(g))

    Part_1_Answer = 0
    for m in machines:
        solution_and_tokens = m.find_cheapest_solution()
        if solution_and_tokens is not None:
            Part_1_Answer += solution_and_tokens[1]

    assert Part_1_Answer > 16583

    return (Part_1_Answer, Part_2_Answer)
