# from AOC_Lib.name import *

from functools import reduce


def resolvedAddressGenerator(inAddress, mask):
    inAddressBinary = format(inAddress, "036b")
    inAddrList = []

    for i in range(len(mask)):
        if mask[i] == "1":
            inAddrList.append("1")
        elif mask[i] == "X":
            inAddrList.append("X")
        else:
            inAddrList.append(inAddressBinary[i])

    inAddressBinary = "".join(inAddrList)
    addrPieces = inAddressBinary.split("X")

    # the permutations of the floating bits
    permutations = len(addrPieces) - 1
    for i in range(1 << permutations):
        thisAddr = []
        trueFalseMap = format(i, f"0{permutations}b")

        for j in range(permutations):
            thisAddr.append(addrPieces[j])
            thisAddr.append(trueFalseMap[j])
        thisAddr.append(addrPieces[-1])
        yield int("".join(thisAddr), 2)


def y2020d14(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d14.txt"
    print("2020 day 14:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    mask0 = None
    mask1 = None
    maskRaw = None

    memory = {}
    memory2 = {}

    translateDicts = {"X": ("1", "0"), "0": ("0", "0"), "1": ("1", "1")}

    for line in lineList:
        s = line.split(" ")
        if s[0] == "mask":
            # update masks (part 1)
            thisMask0 = []
            thisMask1 = []
            for c in s[2]:
                a, b = translateDicts[c]
                thisMask0.append(a)
                thisMask1.append(b)
            mask0 = int("".join(thisMask0), 2)
            mask1 = int("".join(thisMask1), 2)
            # store mask (part 2)
            maskRaw = s[2]
        else:
            # update memory values
            ss = s[0].replace("[", " ").replace("]", " ").split(" ")
            address = int(ss[1])
            value = int(s[2])

            # part 1
            thisValue = (value & mask0) | mask1
            memory[address] = thisValue

            # part 2
            for translatedAddress in resolvedAddressGenerator(address, maskRaw):
                memory2[translatedAddress] = value

    Part_1_Answer = reduce(lambda x, y: x + y, memory.values())
    Part_2_Answer = reduce(lambda x, y: x + y, memory2.values())

    assert Part_2_Answer != 3422624094064

    return (Part_1_Answer, Part_2_Answer)
