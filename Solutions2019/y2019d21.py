# from AOC_Lib.name import *

import itertools
from typing import Optional
from .IntcodeLib import IntcodeProgram, IntcodeRunner


def printDeath(o: list[int]) -> None:
    """Print when a death occurred"""
    print("".join(map(chr, o)))


def didEndInDeath(o: list[int]) -> bool:
    """Return `True` iff this run ended in death"""
    return (o[-1] < 128)


def runSpringCode(
    spring_code_program: list[str],
    intcode_program: IntcodeProgram,
    execute_command: str
) -> Optional[int]:
    """Run the spring code program amd Return the spring code result if one exists"""
    assert(len(spring_code_program) <= 15)

    to_send = list(map(ord, itertools.chain(
        "\n".join(spring_code_program),
        "\n", # to separate code and command
        execute_command,
    )))

    if to_send[-1] != ord('\n'):
        # execute command did not end in '\n'
        to_send.append(ord('\n'))
    
    runner = IntcodeRunner(intcode_program)
    o = runner.run_sync(to_send)

    if didEndInDeath(o):
        printDeath(o)
        return None
    else:
        return o[-1]

def y2019d21(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d21.txt"
    print("2019 day 21:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    prog = IntcodeProgram(map(int, lineList[0].split(",")))

    my_spring_script = [
        # check if need to jump
        "NOT A J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        # check if can jump
        "AND D J",
    ]

    Part_1_Answer = runSpringCode(my_spring_script, prog, "WALK")

    if Part_1_Answer is None:
        return (Part_1_Answer, Part_2_Answer)

    my_spring_script = [
        # We want to jump whenever:
        # TODO - jumping opportunistically (like above) doesnt seem to work
        #   need to jump only when it is required
        "NOT A J",
        "NOT B T",
        ""

    ]

    Part_2_Answer = runSpringCode(my_spring_script, prog, "RUN")

    return (Part_1_Answer, Part_2_Answer)