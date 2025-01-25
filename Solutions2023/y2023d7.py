# from AOC_Lib.name import *
from dataclasses import dataclass, field, replace
from enum import IntEnum
from collections import Counter

class TypeScore(IntEnum):
    FIVE_OF_A_KIND=1000
    FOUR_OF_A_KIND=900
    FULL_HOUSE=800
    THREE_OF_A_KIND=700
    TWO_PAIR=600
    ONE_PAIR=500
    HIGH_CARD=100
    NOT_SET=0

@dataclass(frozen=True)
class Hand:
    cards: str
    bid: int
    is_part_two: bool = False
    typescore: TypeScore = field(init=False, default=TypeScore.NOT_SET)

    def __post_init__(self):
        assert len(self.cards) == 5
        if self.is_part_two:
            ts = self.resolve_typescore_part_two(self.cards)
        else:
            ts = self.resolve_typescore(self.cards)
        object.__setattr__(self, 'typescore', ts)

    @staticmethod
    def resolve_typescore(cards: str) -> TypeScore:
        c = Counter(cards)
        if len(c) == 1:
            return TypeScore.FIVE_OF_A_KIND
        if len(c) == 2:
            if set(c.values()) == {1,4}:
                return TypeScore.FOUR_OF_A_KIND
            if set(c.values()) == {2,3}:
                return TypeScore.FULL_HOUSE
        if 3 in c.values():
            return TypeScore.THREE_OF_A_KIND
        
        pairs = sum(1 for v in c.values() if v == 2)

        if pairs == 2:
            return TypeScore.TWO_PAIR
        if pairs == 1:
            return TypeScore.ONE_PAIR
        return TypeScore.HIGH_CARD

    @staticmethod
    def resolve_typescore_part_two(cards: str) -> TypeScore:
        num_jokers= sum(1 for c in cards if c == 'J')

        p1_ts = Hand.resolve_typescore(cards)

        if p1_ts == TypeScore.FIVE_OF_A_KIND:
            return TypeScore.FIVE_OF_A_KIND
        elif p1_ts == TypeScore.FOUR_OF_A_KIND:
            if num_jokers == 0:
                return TypeScore.FOUR_OF_A_KIND
            if num_jokers == 1:
                return TypeScore.FIVE_OF_A_KIND
            if num_jokers == 4:
                return TypeScore.FIVE_OF_A_KIND
            assert False
        elif p1_ts == TypeScore.FULL_HOUSE:
            if num_jokers == 0:
                return TypeScore.FULL_HOUSE
            if num_jokers == 1:
                return TypeScore.FOUR_OF_A_KIND
            if num_jokers == 2:
                return TypeScore.FIVE_OF_A_KIND
            if num_jokers == 3:
                return TypeScore.FIVE_OF_A_KIND
            assert False
        elif p1_ts == TypeScore.THREE_OF_A_KIND:
            if num_jokers == 0:
                return TypeScore.THREE_OF_A_KIND
            if num_jokers == 1:
                return TypeScore.FOUR_OF_A_KIND
            if num_jokers == 2:
                # JJAAAA
                return TypeScore.FIVE_OF_A_KIND
            if num_jokers == 3:
                # JJJAB
                # JJJAA would be a Full House
                return TypeScore.FOUR_OF_A_KIND
            assert False
        elif p1_ts == TypeScore.TWO_PAIR:
            if num_jokers == 0:
                return TypeScore.TWO_PAIR
            if num_jokers == 1:
                return TypeScore.FULL_HOUSE
            if num_jokers == 2:
                return TypeScore.FOUR_OF_A_KIND
            assert False
        elif p1_ts == TypeScore.ONE_PAIR:
            if num_jokers == 0:
                return TypeScore.ONE_PAIR
            if num_jokers == 1:
                return TypeScore.THREE_OF_A_KIND
            if num_jokers == 2:
                return TypeScore.THREE_OF_A_KIND
            assert False
        elif p1_ts == TypeScore.HIGH_CARD:
            if num_jokers == 0:
                return TypeScore.HIGH_CARD
            if num_jokers == 1:
                return TypeScore.ONE_PAIR
            assert False
        assert False

    
    def get_lexo_cards(self) -> str:
        map = {
            'A': 'a',
            'K': 'b',
            'Q': 'c',
            'J': 'z' if self.is_part_two else 'd',
            'T': 'e',
            '9': 'f',
            '8': 'h',
            '7': 'i',
            '6': 'j',
            '5': 'k',
            '4': 'l',
            '3': 'm',
            '2': 'n'
        }
        return ''.join(map[c] for c in self.cards)


def y2023d7(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2023/d7.txt"
    print("2023 day 7:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    hands: list[Hand] = []

    for line in lineList:
        h,b = line.split()
        hands.append(Hand(h, int(b)))

    hands.sort(key=lambda h:h.get_lexo_cards(), reverse=True)
    hands.sort(key=lambda h:h.typescore.value)

    Part_1_Answer = 0

    for rank, hand in enumerate(hands, start=1):
        Part_1_Answer += rank*hand.bid

    hands = [replace(h, is_part_two=True) for h in hands]

    hands.sort(key=lambda h:h.get_lexo_cards(), reverse=True)
    hands.sort(key=lambda h:h.typescore.value)

    for h in hands:
        print(h)

    Part_2_Answer = 0

    for rank, hand in enumerate(hands, start=1):
        Part_2_Answer += rank*hand.bid

    return (Part_1_Answer, Part_2_Answer)