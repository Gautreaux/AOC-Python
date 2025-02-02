from dataclasses import dataclass
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.Point import DiscretePoint2
from AOC_Lib.boundedInt import BoundedInt


@dataclass
class Robot:
    """A robot with position and velocity"""

    position_x: BoundedInt
    position_y: BoundedInt
    velocity: DiscretePoint2

    def move(self):
        """Move one second"""
        self.position_x += self.velocity.x
        self.position_y += self.velocity.y


class Solution_2024_14(SolutionBase):
    """https://adventofcode.com/2024/day/14"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.width = 101
        self.height = 103

        robots: list[Robot] = []
        for line in self.input_str_list(include_empty_lines=False):
            p, v = line.split(" ")
            pos = DiscretePoint2(*map(int, p.partition("=")[-1].split(",")))
            vel = DiscretePoint2(*map(int, v.partition("=")[-1].split(",")))
            robots.append(
                Robot(
                    BoundedInt(upper_bound=self.width, value=pos.x),
                    BoundedInt(upper_bound=self.height, value=pos.y),
                    vel,
                )
            )
        self.starting_positions: tuple[Robot, ...] = tuple(robots)
        self.robots: list[Robot] = robots

    def simulate_one_second(self) -> None:
        """Simulate one second"""
        for r in self.robots:
            r.move()

    def get_count_by_quadrant(self) -> tuple[int, int, int, int]:
        """Get the count by quadrant"""
        mid_x = self.width // 2
        mix_y = self.height // 2

        # count number of robots in the quadrant
        count_by_quadrant = [0, 0, 0, 0]

        for r in self.robots:
            if r.position_x.asInt() < mid_x and r.position_y.asInt() < mix_y:
                count_by_quadrant[0] += 1
            elif r.position_x.asInt() > mid_x and r.position_y.asInt() < mix_y:
                count_by_quadrant[1] += 1
            elif r.position_x.asInt() < mid_x and r.position_y.asInt() > mix_y:
                count_by_quadrant[2] += 1
            elif r.position_x.asInt() > mid_x and r.position_y.asInt() > mix_y:
                count_by_quadrant[3] += 1

        return tuple(count_by_quadrant)  # type: ignore

    def calculate_safety_factor(self) -> int:
        """Calculate the safety factor"""
        count_by_quadrant = self.get_count_by_quadrant()
        return (
            count_by_quadrant[0]
            * count_by_quadrant[1]
            * count_by_quadrant[2]
            * count_by_quadrant[3]
        )

    def is_vertically_symmetrical_ish(self) -> bool:
        """Return true if this is kinda vertically symmetrical"""
        count_by_quadrant = self.get_count_by_quadrant()
        lhs = count_by_quadrant[0] + count_by_quadrant[2]
        rhs = count_by_quadrant[1] + count_by_quadrant[3]
        return abs(lhs - rhs) < (len(self.robots) // 2)

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        for _ in range(100):
            self.simulate_one_second()
        return self.calculate_safety_factor()

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        self.robots = list(self.starting_positions)

        raise NotImplementedError()

        for i in range(100000):
            self.simulate_one_second()

            if self.is_vertically_symmetrical_ish():
                taken_positions = {
                    (r.position_x.asInt(), r.position_y.asInt()) for r in self.robots
                }

                print(f"After {i} seconds")

                for y in range(self.height):
                    print(
                        "".join(
                            "#" if (x, y) in taken_positions else " "
                            for x in range(self.width)
                        )
                    )
                print("----")
                # from time import sleep
                # sleep(0.25)
