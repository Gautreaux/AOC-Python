# from AOC_Lib.name import *

from copy import copy
import itertools

BLOCK_STATE_T = list[int]


def getNextState(state: BLOCK_STATE_T) -> BLOCK_STATE_T:
    """Get the next state"""

    state = copy(state)

    m_index, m_value = max(enumerate(state), key=lambda x: x[1])
    state[m_index] = 0

    i_gen = itertools.cycle(itertools.chain(range(m_index+1, len(state)), range(m_index)))

    for index,_ in zip(i_gen, range(m_value)):
        state[index]+=1
    return state


def y2017d6(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d6.txt"
    print("2017 day 6:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    block_sizes = list(map(int, lineList[0].split("\t")))
    
    config_cache = {}

    config_cache[tuple(block_sizes)] = 0

    for i in itertools.count(1):
        block_sizes = getNextState(block_sizes)
        t = tuple(block_sizes)
        if t in config_cache:
            if Part_1_Answer is None:
                Part_1_Answer = i
            else:
                j = config_cache[t]
                Part_2_Answer = i - j 
                break
        else:
            config_cache[t] = i

    return (Part_1_Answer, Part_2_Answer)