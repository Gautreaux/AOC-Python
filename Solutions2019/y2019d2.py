from .IntcodeLib import *


def y2019d2(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d2.txt"
    print("2019 day 2:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    prog = IntcodeProgram(map(int, lineList[0].split(",")))

    inst = IntcodeRunner(prog)
    inst.setAddr(1, 12)
    inst.setAddr(2, 2)

    inst.run_sync()

    Part_1_Answer = inst.readAddr(0)

    target_value = 19690720

    # TODO - multiprocess if slow
    for noun in range(100):
        for verb in range(100):
            inst = IntcodeRunner(prog)
            inst.setAddr(1, noun)
            inst.setAddr(2, verb)

            inst.run_sync()

            v = inst.readAddr(0)

            if v == target_value:
                Part_2_Answer = 100 * noun + verb
                return (Part_1_Answer, Part_2_Answer)

    return (Part_1_Answer, Part_2_Answer)
