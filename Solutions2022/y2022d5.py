
from copy import deepcopy
from dataclasses import dataclass, field
import itertools
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@dataclass
class LiftOperation:

    quantity: int
    source: int
    destination: int

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

        columns: list[list[str]] = []

        start_lines = list(itertools.takewhile(
            lambda x: x.strip() != '',
            self.input_str_list(include_empty_lines=True, strip=False)
        ))[:-1]

        for parsed_tokens in map(parser, start_lines):
            for colum_no, token in enumerate(parsed_tokens, start=1):
                if token == ' ':
                    continue

                # Size is dynamic to last specified column
                while len(columns) <= colum_no:
                    columns.append([])
                columns[colum_no].append(token)

        for i in range(len(columns)):
            columns[i] = list(reversed(columns[i]))

        self.start_columns: list[list[str]] = columns

        end_lines = list(itertools.dropwhile(
            lambda x: x.strip() != "",
            self.input_str_list(include_empty_lines=True) 
        ))[1:-1]

        self.operations: list[LiftOperation] = []

        for instr in end_lines:
            _, qty, __, source, ___, dest = instr.split(" ")

            self.operations.append(LiftOperation(
                quantity=int(qty),
                source=int(source),
                destination=int(dest),
            ))

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        columns = deepcopy(self.start_columns)

        for op in self.operations:
            for _ in range(op.quantity):
                columns[op.destination].append(columns[op.source].pop())

        return "".join(map(lambda x: x[-1], columns[1:]))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        columns = deepcopy(self.start_columns)

        for op in self.operations:
            tmp = []

            for _ in range(op.quantity):
                tmp.append(columns[op.source].pop())
            while tmp:
                columns[op.destination].append(tmp.pop())

        return "".join(map(lambda x: x[-1], columns[1:]))