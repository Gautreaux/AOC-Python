# from AOC_Lib.name import *

GEN_A_FACTOR = 16807
GEN_B_FACTOR = 48271
DIVISOR = 2147483647

def genericGenerator(startingValue, stepValue, checker = (lambda _ : True)):
    i = startingValue
    while True:
        i = (i * stepValue) % DIVISOR
        if checker(i) is False:
            continue
        yield i

def y2017d15(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d15.txt"
    print("2017 day 15:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    GEN_A_START = int(lineList[0].split(" ")[4])
    GEN_B_START = int(lineList[1].split(" ")[4])

    # GEN_A_START = 65
    # GEN_B_START = 8921

    print(f"start: {GEN_A_START} {GEN_B_START}")

    generatorA = genericGenerator(GEN_A_START, GEN_A_FACTOR)
    generatorB = genericGenerator(GEN_B_START, GEN_B_FACTOR)

    generator2A = genericGenerator(GEN_A_START, GEN_A_FACTOR, (lambda x : x % 4 == 0))
    generator2B = genericGenerator(GEN_B_START, GEN_B_FACTOR, (lambda x : x % 8 == 0))

    matches = 0
    matches2 = 0
    mask = (1 << 16) - 1

    # TODO - this feels like another Chineese Remainder Theorem problem
    for i in range(40*(10**6)):
        a = next(generatorA)
        b = next(generatorB)

        bin_both = (a ^ b) & mask

        if bin_both == 0:
            matches += 1

    for i in range(5*(10**6)):
        a2 = next(generator2A)
        b2 = next(generator2B)

        bin_both_2 = (a2 ^ b2) & mask

        if bin_both_2 == 0:
            matches2 += 1 
        

    Part_1_Answer = matches
    Part_2_Answer = matches2

    return (Part_1_Answer, Part_2_Answer)