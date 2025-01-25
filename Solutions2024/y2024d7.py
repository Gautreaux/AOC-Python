# from AOC_Lib.name import *
from typing import Iterator
from enum import Enum, auto

class CalibrationEquationOperands(Enum):
    ADD = auto()
    MUL = auto()
    CCAT = auto()

class CalibrationEquation:
    def __init__(self, target: int, operands: Iterator[int]):
        self.target: int = target
        self.operands: tuple[int] = tuple(operands)

    def generate_valid_solutions(self, supported_operands: list[CalibrationEquationOperands]) -> Iterator[str]:
        """Generate the valid solutions"""
        if not self.operands:
            return
        
        if len(self.operands) == 1:
            if self.target == self.operands[0]:
                yield f'{self.target}'
            else:
                return
            
        if CalibrationEquationOperands.ADD in supported_operands:    
            new_t = self.target - self.operands[-1]
            new_eq = CalibrationEquation(new_t, self.operands[:-1])
            for solution in new_eq.generate_valid_solutions(supported_operands):
                yield f'{solution} + {self.operands[-1]}'
        
        if CalibrationEquationOperands.MUL in supported_operands:
            if self.target % self.operands[-1] == 0:
                new_t = self.target // self.operands[-1]
                new_eq = CalibrationEquation(new_t, self.operands[:-1])
                for solution in new_eq.generate_valid_solutions(supported_operands):
                    yield f'{solution} * {self.operands[-1]}'
        
        if (CalibrationEquationOperands.CCAT in supported_operands):
            str_target = str(self.target)
            str_last_op = str(self.operands[-1])
            if ((str_target != str_last_op) and (str_target.endswith(str_last_op))):
                new_target = int(str_target[:-len(str_last_op)])
                new_eq = CalibrationEquation(new_target, self.operands[:-1])
                for solution in new_eq.generate_valid_solutions(supported_operands):
                    yield f'{solution} || {self.operands[-1]}'

    def has_any_solution(self, supported_operands: list[CalibrationEquationOperands]) -> bool:
        """Return true iff there is at least one valid solution"""

        try:
            next(self.generate_valid_solutions(supported_operands))
        except StopIteration:
            return False
        else:
            return True

def y2024d7(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2024/d7.txt"
    print("2024 day 7:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    equations: list[CalibrationEquation] = []

    for line in lineList:
        target_str, _, tkns = line.partition(':')
        equations.append(CalibrationEquation(int(target_str), map(int, tkns.split())))

    part_1_operands = [CalibrationEquationOperands.ADD, CalibrationEquationOperands.MUL]
    part_2_operands = [CalibrationEquationOperands.ADD, CalibrationEquationOperands.MUL, CalibrationEquationOperands.CCAT]

    Part_1_Answer = sum(eq.target for eq in equations if eq.has_any_solution(part_1_operands))
    Part_2_Answer = sum(eq.target for eq in equations if eq.has_any_solution(part_2_operands))

    assert Part_2_Answer > Part_1_Answer

    return (Part_1_Answer, Part_2_Answer)