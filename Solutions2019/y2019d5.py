from .IntcodeLib import *

def y2019d5(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d5.txt"
    print("2019 day 5:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    prog = IntcodeProgram(map(int, lineList[0].split(",")))

    inst = IntcodeRunner(prog)

    outputs = inst.run_sync([1])

    # print(outputs)

    Part_1_Answer = outputs.pop()

    assert(all(map(lambda x: x == 0, outputs)))

    inst = IntcodeRunner(prog)

    outputs = inst.run_sync([5])

    assert(len(outputs) == 1)

    Part_2_Answer = outputs[0]

    return Part_1_Answer, Part_2_Answer

#part 2: 14250156 incorrect
# 15386262 -- too high