# from AOC_Lib.name import *


def y2018d14(inputPath=None):
    if inputPath == None:
        inputPath = "Input2018/d14.txt"
    print("2018 day 14:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    puzzleInput = int(lineList[-1])

    elf1Index = 0
    elf2Index = 1

    counter = [3, 7]

    pendingCharacters = str(puzzleInput)
    matchedChars = 0

    while (len(counter) < puzzleInput + 10) or Part_2_Answer is None:
        # expand the recipes
        now = counter[elf1Index] + counter[elf2Index]
        s = str(now)
        for c in s:
            counter.append(int(c))
            if c == pendingCharacters[matchedChars]:
                matchedChars += 1
                if matchedChars >= len(pendingCharacters):
                    Part_2_Answer = len(counter)
                    # since the match may occur on the first ones
                    matchedChars = 0
            else:
                matchedChars = 0

        # print(elf1Index, end=" ")
        # print(elf2Index, end=" ")

        # now advance the elves
        elf1Index = (elf1Index + counter[elf1Index] + 1) % len(counter)
        elf2Index = (elf2Index + counter[elf2Index] + 1) % len(counter)

        # print(counter, end=" ")
        # print(elf1Index, end=" ")
        # print(elf2Index)

    partial = ""
    for i in range(puzzleInput, puzzleInput + 10):
        partial += str(counter[i])

    Part_1_Answer = partial

    assert Part_1_Answer != 120

    # i think there is an off by 1 in here sometimes
    Part_2_Answer -= len(pendingCharacters)

    # i hate this solution but it works so...
    # k = "".join(map(lambda x: str(x), counter))
    # i = k.find(str(puzzleInput))
    # Part_2_Answer = i

    assert Part_2_Answer != "1197361681"
    assert Part_2_Answer != "119736168"
    assert Part_2_Answer != "1511197361"

    return (Part_1_Answer, Part_2_Answer)
