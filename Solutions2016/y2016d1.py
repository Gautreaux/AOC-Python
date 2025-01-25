"""https://adventofcode.com/2016/day/1"""

from AOC_Lib.SolutionBase import SolutionBase

from AOC_Lib.point import Point2, Y_2_TRANSLATIONS
from AOC_Lib.point import Y_UP_2_TRANSFORMS as transforms
from AOC_Lib.boundedInt import BoundedInt


class Solution_2016_01(SolutionBase):
    """https://adventofcode.com/2016/day/1"""

    def __post_init__(self):
        """Runs Once After `__init__`"""
        puzzle_input = self.input_str()
        tokens = puzzle_input.replace(" ", "").split(",")

        visited_locations_set: set = set()

        # NORTH = 0
        # EAST = 1
        # SOUTH = 2
        # WEST = 3
        direction = BoundedInt(4, value=0)
        pos = Point2(0, 0)

        visited_locations_set.add(pos)

        for t in tokens:
            if t[0] == "R":
                direction += 1
            elif t[0] == "L":
                direction -= 1
            else:
                raise ValueError(t[0])

            tt = transforms[Y_2_TRANSLATIONS[direction.asInt()]]

            steps = int(t[1:])

            for _ in range(steps):
                pos += tt
                if not self.is_part_2_done():
                    if pos in visited_locations_set:
                        self._part_2_answer = pos.manhattan()
                    else:
                        visited_locations_set.add(pos)

            self._part_1_answer = pos.manhattan()
