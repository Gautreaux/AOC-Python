

from dataclasses import dataclass, field
import itertools
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


class Solution_2022_05(SolutionBase):
    """https://adventofcode.com/2022/day/5"""

    def __post_init__(self):
        """Runs Once After `__init__`"""
        
        def parser(l: str):
            i = iter(l)
            try:
                while True:    
                    next(i)
                    yield next(i)
                    next(i)
                    next(i)
            except StopIteration:
                return

        columns = list(map(lambda _: list(), range(12)))

        print(columns)

        start_lines = list(itertools.takewhile(
            lambda x: x.strip() != '',
            self.input_str_list(include_empty_lines=True)
        ))[:-1]

        self.end_lines = list(itertools.dropwhile(
            lambda x: x.strip() != "",
            self.input_str_list(include_empty_lines=True) 
        ))[1:-1]

        print(self.end_lines[0])
        print(self.end_lines[-1])

        self.columns: list[list[str]] = [
            [],
            ['S', 'L', 'W'],
            ['J', 'T', 'N', 'Q'],
            ['S', 'C', 'H', 'F', 'J'],
            list(iter('TRMWNGB')),
            list(iter('TRLSDHQB')),
            list(iter('MJBVFHRL')),
            list(iter('DWRNJM')),
            list(iter('BZTFHNDJ')),
            list(iter('HLQNBFT')),
        ]
        self.columns2: list[list[str]] = [
            [],
            ['S', 'L', 'W'],
            ['J', 'T', 'N', 'Q'],
            ['S', 'C', 'H', 'F', 'J'],
            list(iter('TRMWNGB')),
            list(iter('TRLSDHQB')),
            list(iter('MJBVFHRL')),
            list(iter('DWRNJM')),
            list(iter('BZTFHNDJ')),
            list(iter('HLQNBFT')),
        ]



    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        for instr in self.end_lines:
            _, qty, __, source, ___, dest = instr.split(" ")

            qty = int(qty)
            source = int(source)
            dest = int(dest)

            for _ in range(qty):
                self.columns[dest].append(self.columns[source].pop())

        return "".join(map(lambda x: x[-1], self.columns[1:]))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        for instr in self.end_lines:
            _, qty, __, source, ___, dest = instr.split(" ")

            qty = int(qty)
            source = int(source)
            dest = int(dest)

            tmp = []

            for _ in range(qty):
                tmp.append(self.columns2[source].pop())
            while tmp:
                self.columns2[dest].append(tmp.pop())

        return "".join(map(lambda x: x[-1], self.columns2[1:]))