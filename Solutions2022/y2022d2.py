# from AOC_Lib.name import *

from enum import Enum, unique

@unique
class Action(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def get_action(cls, v: str) -> 'Action':
        return {
            'A': cls.ROCK,
            'B': cls.PAPER,
            'C': cls.SCISSORS,
            'X': cls.ROCK,
            'Y': cls.PAPER,
            'Z': cls.SCISSORS,
        }[v]

    
    @classmethod
    def get_win_outcome(cls, other_move: 'Action'):
        return {
            Action.ROCK: Action.PAPER,
            Action.PAPER: Action.SCISSORS,
            Action.SCISSORS: Action.ROCK
        }[other_move]

    @classmethod
    def get_tie_outcome(cls, other_move: 'Action'):
        return other_move

    @classmethod
    def get_loss_outcome(cls, other_move: 'Action'):
        return {
            Action.ROCK: Action.SCISSORS,
            Action.SCISSORS: Action.PAPER,
            Action.PAPER: Action.ROCK,
        }[other_move]


    @classmethod
    def get_action_by_outcome(cls, other_move: 'Action', desired_outcome: str):
        return {
            'X': cls.get_loss_outcome,
            'Y': cls.get_tie_outcome,
            'Z': cls.get_win_outcome,
        }[desired_outcome](other_move)

    def beats(self, other: 'Action') -> bool:
        if self == Action.ROCK and other == Action.SCISSORS:
            return True
        if self == Action.PAPER and other == Action.ROCK:
            return True
        if self == Action.SCISSORS and other == Action.PAPER:
            return True
        return False

    def ties(self, other: 'Action') -> bool:
        return self == other

def y2022d2(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2022/d2.txt"
    print("2022 day 2:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # for single line inputs
    for c in lineList[-1]:
        pass

    # for multi line inputs

    running_score = 0

    for line in lineList:
        o, m = line.split(" ")
        other_move = Action.get_action(o)
        my_move = Action.get_action(m)

        if my_move.beats(other_move):
            running_score += 6
        elif my_move.ties(other_move):
            running_score += 3
        else:
            running_score += 0
        
        running_score += my_move.value

    Part_1_Answer = running_score

    # ==== Part 2 ====

    running_score = 0

    for line in lineList:
        o, m = line.split(" ")
        other_move = Action.get_action(o)
        my_move = Action.get_action_by_outcome(other_move, m)

        if my_move.beats(other_move):
            running_score += 6
        elif my_move.ties(other_move):
            running_score += 3
        else:
            running_score += 0
        
        running_score += my_move.value

    Part_2_Answer = running_score

    return (Part_1_Answer, Part_2_Answer)