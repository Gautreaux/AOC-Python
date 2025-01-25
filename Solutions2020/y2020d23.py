# from AOC_Lib.name import *

from typing import Final, Generator

PICKUP_COUNT: Final = 3
# for now, this cannot be changed
assert PICKUP_COUNT == 3

LABEL_GENERATOR_TYPE = Generator[int, None, None]


def playCrabbyCups(
    cupOrderingGenerator: LABEL_GENERATOR_TYPE, numTurns: int
) -> LABEL_GENERATOR_TYPE:
    """Produces a generator that can yield elements in the starting order"""

    indexLabelMapping = []  # map an index to a label
    nextIndexForIndex = []  # the next index following an index
    # use a dict in case there are gaps in the input
    labelIndexMapping = {}  # map a label to an index

    for i in cupOrderingGenerator:
        indexLabelMapping.append(i)
        nextIndexForIndex.append(len(indexLabelMapping))
        labelIndexMapping[indexLabelMapping[-1]] = len(indexLabelMapping) - 1
    nextIndexForIndex[-1] = 0

    # making sure all the labels are unique
    assert len(set(indexLabelMapping)) == len(indexLabelMapping)

    # print("DONG")

    # for label in indexLabelMapping:
    #     labelIndexMapping[label] = indexLabelMapping.index(label)

    # print("DING")

    minLabel = min(indexLabelMapping)
    maxLabel = max(indexLabelMapping)

    # print(indexLabelMapping)
    # print(nextIndexForIndex)
    print("input PreProcessing Completed")

    def safeDecrement(label: int) -> int:
        return maxLabel if label - 1 < minLabel else label - 1

    currentCupIndex = 0
    pickupIndexes = [None] * PICKUP_COUNT

    for turn in range(numTurns):
        # figure out what we are picking up
        pickupIndexes[0] = nextIndexForIndex[currentCupIndex]
        pickupIndexes[1] = nextIndexForIndex[pickupIndexes[0]]
        pickupIndexes[2] = nextIndexForIndex[pickupIndexes[1]]

        pickupValues = list(map(lambda x: indexLabelMapping[x], pickupIndexes))

        # remove these items from the list
        nextIndexForIndex[currentCupIndex] = nextIndexForIndex[pickupIndexes[2]]

        # figure out what the target label is
        activeLabel = indexLabelMapping[currentCupIndex]
        targetLabel = safeDecrement(activeLabel)
        while targetLabel in pickupValues:
            targetLabel = safeDecrement(targetLabel)

        # convert target label to index
        targetIndex = labelIndexMapping[targetLabel]

        # debug info
        # print(pickupIndexes)
        # print(f" Turn {turn+1} pickup {pickupValues}, active: {activeLabel}, target: {targetLabel}")

        # re-do the chaining
        nextIndexForIndex[pickupIndexes[2]] = nextIndexForIndex[targetIndex]
        nextIndexForIndex[targetIndex] = pickupIndexes[0]

        # pick the next active cup
        currentCupIndex = nextIndexForIndex[currentCupIndex]

        # DEBUG
        # check that everything still appears only once
        #   (that the chain property is maintained)
        # assert(len(set(nextIndexForIndex)) == len(nextIndexForIndex))
        # if turn >= 5:
        #     break

        if turn % 1000000 == 0 and turn != 0:
            print(f"Turn on {turn}")

    # time to build the part 1 answer
    startInd = labelIndexMapping[1]
    currentInd = startInd
    while True:
        yield indexLabelMapping[currentInd]
        currentInd = nextIndexForIndex[currentInd]
        if currentInd == startInd:
            break
    return


def y2020d23(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d23.txt"
    print("2020 day 23:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # print("DEBUG ON")
    # lineList[-1] = "389125467"

    def part1InputGenerator():
        for c in lineList[-1]:
            yield int(c)

    part1AnswerGenerator = playCrabbyCups(part1InputGenerator(), 100)
    Part_1_Answer = int("".join(map(str, part1AnswerGenerator))[1:])
    print(f"Part 1 is {Part_1_Answer}, starting part 2")

    def part2InputGenerator():
        yieldedCount = 0
        # ensuring no indexes are in the start
        assert len(set(lineList[-1])) == len(lineList[-1])
        for c in lineList[-1]:
            yield int(c)
            yieldedCount += 1

        yieldedCount += 1

        while yieldedCount <= 1000000:
            yield yieldedCount
            yieldedCount += 1

    # l = list(part2InputGenerator())
    # print(len(l))
    # assert(len(l) == 1000000)
    # assert(len(set(l)) == len(l))
    # assert(min(l) == 1)
    # assert(max(l) == len(l))

    part2AnswerGenerator = playCrabbyCups(part2InputGenerator(), 10000000)
    next(part2AnswerGenerator)
    a = next(part2AnswerGenerator)
    b = next(part2AnswerGenerator)
    assert a != 1 and b != 1
    print(f"P2 : {a} * {b}")
    Part_2_Answer = a * b

    return (Part_1_Answer, Part_2_Answer)
