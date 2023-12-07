# from AOC_Lib.name import *

from dataclasses import dataclass
from enum import StrEnum


class Color(StrEnum):
    RED='red'
    BLUE='blue'
    GREEN='green'


@dataclass(frozen=True)
class Turn:
    quantity_red: int
    quantity_blue: int
    quantity_green: int

    def stasifies_limits(self, limit_red: int, limit_blue: int, limit_green: int) -> bool:
        return self.quantity_blue <= limit_blue and self.quantity_green <= limit_green and self.quantity_red <= limit_red


@dataclass(frozen=True)
class Game:
    id: int
    turns: tuple[Turn, ...]

    @classmethod
    def parse_from_line(cls, line:str) -> 'Game':
        tokens = line.split()

        id_ = int(tokens[1][:-1])
        turns = []

        qr = 0
        qg = 0
        qb = 0

        for i in range(2, len(tokens), 2):
            end = False
            qty = int(tokens[i])
            color = tokens[i+1]
            if color.endswith(','):
                color = color[:-1]
            elif color.endswith(';'):
                color = color[:-1]
                end = True

            if Color(color) == Color.RED:
                qr += qty
            if Color(color) == Color.BLUE:
                qb += qty
            if Color(color) == Color.GREEN:
                qg += qty
            
            if end:
                turns.append(Turn(qr, qb, qg))
                qr = 0
                qb = 0
                qg = 0
            
        if (qr + qb + qg):
            turns.append(Turn(qr, qb, qg))
        
        return Game(id=id_, turns=tuple(turns))
    
    def stasifies_limits(self, limit_red: int, limit_blue: int, limit_green: int) -> bool:
        return all(t.stasifies_limits(limit_red, limit_blue, limit_green) for t in self.turns)
    
    def get_minimums(self) -> tuple[int, int, int]:
        return (
            max(t.quantity_red for t in self.turns),
            max(t.quantity_blue for t in self.turns),
            max(t.quantity_green for t in self.turns)
        )

    def get_minimum_power(self) -> int:
        a,b,c = self.get_minimums()
        return a*b*c


def y2023d2(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2023/d2.txt"
    print("2023 day 2:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    games = [Game.parse_from_line(line) for line in lineList]

    part_1_games = [g for g in games if g.stasifies_limits(12, 14, 13)]

    Part_1_Answer = sum(g.id for g in part_1_games)
    Part_2_Answer = sum(g.get_minimum_power() for g in games)

    assert Part_2_Answer > 388

    return (Part_1_Answer, Part_2_Answer)