from .IntcodeLib import *

def y2019d9(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d9.txt"
    print("2019 day 9:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # prog = IntcodeProgram([109, 2000, 109, 19, 204, -34, 99])
    # inst = IntcodeRunner(prog)
    # inst.setAddr(1985, 324)
    # out = inst.run_sync()
    # print(inst._relBase)
    # print(out)
    # return (-1, -1)


    prog = IntcodeProgram(map(int, lineList[0].split(",")))


    inst = IntcodeRunner(prog)

    outputs = inst.run_sync([1])
    
    Part_1_Answer = outputs[0]

    inst = IntcodeRunner(prog)
    outputs = inst.run_sync([2])
    if len(outputs) != 1:
        print(o)
        raise RuntimeError

    Part_2_Answer = outputs[0]
    return (Part_1_Answer, Part_2_Answer)


# ==================


from typing import Optional

from .IntcodeLib import IntcodeSolutionBase
from AOC_Lib.SolutionBase import Answer_T


class Solution_2019_09(IntcodeSolutionBase):
    """https://adventofcode.com/2019/day/9"""

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        runner = self._runner_factory()

        outputs = runner.run_sync([1])

        if len(outputs) != 1:
            print("Warning, problematic codes found:")
            print("Inst is done: ", runner.terminated())
            print("Out q empty: ", runner.getOutputQ().empty())
            for o in outputs:
                print(o)
            raise RuntimeError
        
        return outputs[0]

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        runner = self._runner_factory()

        outputs = runner.run_sync([2])
        if len(outputs) != 1:
            print(outputs)
            raise RuntimeError
        
        return outputs[0]
