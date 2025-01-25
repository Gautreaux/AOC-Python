from AOC_Lib.SolutionBase import SolutionBase


class Solution_2019_01(SolutionBase):
    """https://adventofcode.com/2019/day/01"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        newFuelCounter = 0
        newTotalFuelCounter = 0

        for line in self.input_str_list(include_empty_lines=False):
            newFuelCounter += int(line) // 3 - 2

            temp_counter = int(line)

            while temp_counter > 0:
                next_temp = temp_counter // 3 - 2
                if next_temp > 0:
                    newTotalFuelCounter += next_temp
                    temp_counter = next_temp
                else:
                    temp_counter = 0

        self._part_1_answer = newFuelCounter
        self._part_2_answer = newTotalFuelCounter

        print(newFuelCounter, newTotalFuelCounter)
