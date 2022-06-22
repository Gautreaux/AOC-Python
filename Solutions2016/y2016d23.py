# from AOC_Lib.name import *

from .AssemBunny import AssemBunnyRunner, AssemBunnyProgram

def y2016d23(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d23.txt"
    print("2016 day 23:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    lineList = [
        "cpy 2 a",
        "tgl a",
        "tgl a",
        "tgl a",
        "cpy 1 a",
        "dec a",
        "dec a",
    ]
    
    program = AssemBunnyProgram.fromStrs(lineList)

    program_e = program.copy()
    program_e.unlock()

    runner = AssemBunnyRunner(program_e)
    runner.setMemValue('a', 7)
    runner.run_sync()

    Part_1_Answer = runner.getMemValue('a')

    # instructionSet = []

    # for line in lineList:
    #     l = line.split(" ")

    #     for i in [1,2]:
    #         try:
    #             l[i] = int(l[i])
    #         except:
    #             pass
    #     instructionSet.append(l)

    # Part_1_Answer = runProgram(instructionSet, {'a':7})['a']
    # Part_2_Answer = runProgram(instructionSet, {'a':12})['a']

    # assert(Part_2_Answer > 7716)

    return (Part_1_Answer, Part_2_Answer)