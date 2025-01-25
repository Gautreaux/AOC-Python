# from AOC_Lib.name import *

import re
from dataclasses import dataclass
from typing import Iterator

@dataclass(frozen=True)
class MulOperation:
    lhs: int
    rhs: int

    @staticmethod
    def try_parse(mulOp: str) -> 'MulOperation | None':
        try:
            return MulOperation.parse(mulOp)
        except:
            return None

    @staticmethod
    def parse(mulOp: str) -> 'MulOperation':
        
        assert mulOp.startswith('mul(')
        assert mulOp.endswith(')')
        lhs_str, rhs_str = mulOp.split(',')
        lhs = int(lhs_str[4:])
        rhs = int(rhs_str[:-1])

        assert lhs < 1000
        assert rhs < 1000

        return MulOperation(lhs, rhs)
    
    def evaluate(self) -> int:
        return self.lhs * self.rhs

@dataclass(frozen=True)
class DoOperation:
    pass

@dataclass(frozen=True)
class DontOperation:
    pass


SUPPORTED_OPERATORS_T = MulOperation | DoOperation | DontOperation



class MulcodeRunner:
    """Run Mulcode"""

    @staticmethod
    def parse_program_operators(program: str) -> Iterator[SUPPORTED_OPERATORS_T]:
        """Parse the program operators"""
        current_index = 0
        
        while current_index < len(program):
            try:
                # Try and parse do
                if program.startswith('do()', current_index):
                    yield DoOperation()
                    continue

                # Try and parse don't
                if program.startswith("don't()", current_index):
                    yield DontOperation()
                    continue
                
                # Try and parse mul:
                if program.startswith('mul(', current_index):
                    end_index = program.find(')', current_index+1)
                    token = program[current_index:end_index+1]
                    mc = MulOperation.try_parse(token)
                    if mc is not None:
                        # current_index = end_index
                        yield mc
                    continue
    
            finally:
                current_index +=1

    @staticmethod
    def load_program(program: str) -> 'MulcodeRunner':
        operators = MulcodeRunner.parse_program_operators(program)
        return MulcodeRunner(operators=operators)

    def __init__(self, operators: Iterator[SUPPORTED_OPERATORS_T]):
        self.program: tuple[SUPPORTED_OPERATORS_T] = tuple(operators)

        self.accumulator: int = 0
        self._mul_enabled: bool = True

    def run(self) -> int:
        """Run the program; return the accumulator value"""
        assert self.accumulator == 0
        for op in self.program:
            if isinstance(op, DontOperation):
                self._mul_enabled = False
            elif isinstance(op, DoOperation):
                self._mul_enabled = True
            elif isinstance(op, MulOperation):
                if self._mul_enabled:
                    self.accumulator += op.evaluate()
            else:
                raise TypeError(f'Unsupported Operator {type(op)}: {op}')

        return self.accumulator

def y2024d3(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2024/d3.txt"
    print("2024 day 3:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    Part_1_Answer = 0
    Part_2_Answer = 0

    for line in lineList:
        part_2_program = MulcodeRunner.load_program(line)
        part_1_program = MulcodeRunner(op for op in part_2_program.program if isinstance(op, MulOperation))

        Part_1_Answer += part_1_program.run()
        Part_2_Answer += part_2_program.run()

        print('-----\n', part_2_program.program)

    assert MulcodeRunner.load_program("""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))""").run() == 48

    assert Part_1_Answer == 185797128, f'current Part_1_Answer: {Part_1_Answer}'
    assert Part_1_Answer > Part_2_Answer
    assert Part_2_Answer < 92974346, f'current Part_2_Answer: {Part_2_Answer}'

    return (Part_1_Answer, Part_2_Answer)