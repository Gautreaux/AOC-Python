# from AOC_Lib.name import *

from collections import namedtuple
import itertools
from typing import Iterable, Generator


def playGame(
    dice: Iterable[int], 
    p1_start: int,
    p2_start: int,
    stop_score: int = 1000,
) -> int:
    """Play a game (part 1) and return the loser score time number of dice rolls"""
    
    p1_pos = p1_start
    p2_pos = p2_start

    p1_score = 0
    p2_score = 0
    next_turn_is_p1 = True
    num_rolls = 0

    while p1_score < stop_score and p2_score < stop_score:
        this_roll = next(dice) + next(dice) + next(dice)
        num_rolls += 3

        if next_turn_is_p1:
            p1_pos = (p1_pos + this_roll) % 10
            p1_score += (p1_pos + 1)
        else:
            p2_pos = (p2_pos + this_roll) % 10
            p2_score += (p2_pos + 1)
        next_turn_is_p1 = not next_turn_is_p1

    if p1_score > p2_score:
        return p2_score * num_rolls
    else:
        return p1_score * num_rolls


DiracState_T = namedtuple("DiracState_T", "p1_next p1_score p2_score p1_pos p2_pos")


def generateSuccessorStates(ds: DiracState_T) -> Generator[DiracState_T, None, None]:
    """Generate the Dirac Successors for the input state"""
    # TODO - need to still roll dice three times
    #   so each round of rolling will produce 27 states
    #   but some states will appear multiple times:
    #   [1,1,1]
    #   [1,1,2] <-------
    #   [1,1,3]
    #   [1,2,1] <-------
    #   [1,2,2]
    #   [1,2,3]
    #   ....
    #   [3,3,3]
    #   [2,1,1] <-------

    if ds.p1_next:
        for i in range(1,4):
            pos = (ds.p1_pos + i) % 10
            yield DiracState_T(False, ds.p1_score + pos, ds.p2_score, pos, ds.p2_pos)
    else:
        for i in range(1,4):
            pos = (ds.p2_pos + i) % 10
            yield DiracState_T(False, ds.p1_score, ds.p2_score + pos, ds.p1_pos, pos)


def playDiracGame(
    p1_start: int,
    p2_start: int,
    stop_score: int = 21, 
):
    """Play a dirac game and return the tuple of p1 wins and p2 wins"""

    p1_total_wins = 0
    p2_total_wins = 0

    l = []
    l.append(DiracState_T(True, 0, 0, p1_start, p2_start))

    for i in itertools.count():
        if len(l) == 0:
            break

        if i % 100000 == 0:
            print(f"i:{i} | l:{len(l)}")
        
        s:DiracState_T = l.pop()

        if s.p1_score >= stop_score:
            assert(s.p2_score < stop_score)
            p1_total_wins += 1
            continue
        elif s.p2_score >= stop_score:
            p2_total_wins += 1
            continue

        l.extend(generateSuccessorStates(s))
    return (p1_total_wins, p2_total_wins)


def y2021d21(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d21.txt"
    print("2021 day 21:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # minus one for offsetting the tile #
    p1_pos = int(lineList[0].rpartition(" ")[-1]) - 1
    p2_pos = int(lineList[1].rpartition(" ")[-1]) - 1 

    dice = itertools.cycle(range(1,101))

    Part_1_Answer = playGame(dice, p1_pos, p2_pos)

    a,b = playDiracGame(p1_pos, p2_pos)

    Part_2_Answer = max(a,b)

    return (Part_1_Answer, Part_2_Answer)