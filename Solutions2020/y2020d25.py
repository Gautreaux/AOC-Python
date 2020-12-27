# from AOC_Lib.name import *

from typing import Final

DEFAULT_SUBJECT_NUMBER : Final = 7
DEFAULT_REMAINDER : Final = 20201227

def getLoopSize(desiredKey : int, subjectNumber = DEFAULT_SUBJECT_NUMBER) -> int:
    v = 1
    i = 0
    while True:
        v = (v * subjectNumber) % DEFAULT_REMAINDER
        i += 1
        if v == desiredKey:
            return i

def transformKey(subjectNumber : int, loopSize : int ) -> int:
    v = 1 
    for _ in range(loopSize):
        v = (v * subjectNumber) % DEFAULT_REMAINDER
    return v

def y2020d25(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2020/d25.txt"
    print("2020 day 25:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # i don't know what order the input is in, 
    #   but it shouldn't matter
    CARD_PUBLIC_KEY = int(lineList[0])
    DOOR_PUBLIC_KEY = int(lineList[1])

    CARD_LOOP_SIZE = getLoopSize(CARD_PUBLIC_KEY)
    DOOR_LOOP_SIZE = getLoopSize(DOOR_PUBLIC_KEY)

    ENCRYPTION_KEY_DOOR = transformKey(DOOR_PUBLIC_KEY, CARD_LOOP_SIZE)
    ENCRYPTION_KEY_CARD = transformKey(CARD_PUBLIC_KEY, DOOR_LOOP_SIZE)

    assert(ENCRYPTION_KEY_CARD == ENCRYPTION_KEY_DOOR)
    Part_1_Answer = ENCRYPTION_KEY_DOOR



    return (Part_1_Answer, Part_2_Answer)