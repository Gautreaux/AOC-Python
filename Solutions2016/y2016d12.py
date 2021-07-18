# from AOC_Lib.name import *

# run program and return the memory map
def runProgram(instructionSet, memory={}):
    for register in ["a", "b", "c", "d"]:
        if register not in memory:
            memory[register] = 0

    print(f"Starting memory: {memory}")
        
    programCounter = 0

    def inc(address):
        nonlocal programCounter
        if isinstance(address, str):
            memory[address] += 1
        programCounter += 1
    
    def dec(address):
        nonlocal programCounter
        if isinstance(address, str):
            memory[address] -= 1
        programCounter += 1

    def cpy(value, target):
        nonlocal programCounter
        if isinstance(target, int):
            programCounter += 1
            return

        if isinstance(value, int):
            memory[target] = value
        else:
            memory[target] = memory[value]
        programCounter += 1
    
    def jnz(check, offset):
        nonlocal programCounter
        if isinstance(check, str):
            check = memory[check]
        if isinstance(offset, str):
            offset = memory[offset]

        if check == 0:
            programCounter += 1
        else:
            programCounter += offset

    # for 2016d23
    def tgl(offset):
        if isinstance(offset, str):
            offset = memory[offset]
        
        nonlocal programCounter
        nonlocal instructionSet

        targetIdx = programCounter + offset

        try:
            cmd = instructionSet[targetIdx]

            if cmd[0] == "inc":
                cmd[0] = "dec"
            elif cmd[0] == "dec":
                cmd[0] = "inc"
            elif cmd[0] == "tgl":
                cmd[0] = "inc"
            elif cmd[0] == "jnz":
                cmd[0] = "cpy"
            elif cmd[0] == "cpy":
                cmd[0] = "jnz"
            else:
                raise ValueError(f"Unknown instruction `{cmd[0]}`")

            instructionSet[targetIdx] = cmd
        except IndexError:
            pass

        programCounter += 1


    grammer = {
        "inc": inc,
        "dec": dec,
        "cpy": cpy,
        "jnz": jnz,
        "tgl" : tgl,
    }

    try:
        while True:
            instruction = instructionSet[programCounter]
            # print(f"{programCounter} {instruction} : {memory}")
            # print(instruction)
            # print(instruction[1:])
            grammer[instruction[0]](*instruction[1:])
    except IndexError:
        return memory

def y2016d12(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d12.txt"
    print("2016 day 12:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    instructionSet = []

    for line in lineList:
        l = line.split(" ")

        for i in [1,2]:
            try:
                l[i] = int(l[i])
            except:
                pass
        instructionSet.append(l)

    Part_1_Answer = runProgram(instructionSet)['a']
    Part_2_Answer = runProgram(instructionSet, memory={'c':1})['a']

    return (Part_1_Answer, Part_2_Answer)