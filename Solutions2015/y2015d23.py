# from AOC_Lib.name import *

from cProfile import run


def runProgram(instructions, registers):
    program_counter = 0
    while program_counter >= 0 and program_counter < len(instructions):
        inst, arg1, arg2 = instructions[program_counter]
        if inst == "hlf":
            assert(registers[arg1] % 2 == 0)
            registers[arg1] /= 2
            program_counter += 1
            continue
        elif inst == "tpl":
            registers[arg1] *= 3
            program_counter += 1
            continue
        elif inst == "inc":
            registers[arg1] += 1
            program_counter += 1
            continue
        elif inst == "jmp":
            program_counter += arg1
            continue
        elif inst == "jie":
            if registers[arg1] % 2 == 0:
                program_counter += arg2
            else:
                program_counter += 1
            continue
        elif inst == "jio":
            if registers[arg1] == 1:
                program_counter += arg2
            else:
                program_counter += 1
            continue
        else:
            raise ValueError(f"Unknown Instruction: {inst}")
    
    return registers


def y2015d23(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d23.txt"
    print("2015 day 23:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    instructions = []

    for line in lineList:
        tokens = line.replace(",", "").split(" ")
        for i in range(1, len(tokens)):
            try:
                tokens[i] = int(tokens[i])
            except ValueError:
                pass
        if len(tokens) == 2:
            tokens.append(None)
        instructions.append(tuple(tokens))
            
    Part_1_Answer = runProgram(instructions, {"a": 0, "b":0})["b"]
    Part_2_Answer = runProgram(instructions, {"a": 1, "b":0})["b"]
    return (Part_1_Answer, Part_2_Answer)