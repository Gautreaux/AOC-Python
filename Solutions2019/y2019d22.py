# from AOC_Lib.name import *

import itertools
from typing import Iterable

Card_T = int
Deck_T = Iterable[Card_T]


def dealIntoNewStack(deck: Deck_T) -> Deck_T:
    """Deal the deck into a new stack and then use this as the new deck"""
    l = list(deck)
    return reversed(l)


def _cutNegN(deck:Deck_T, n:int) -> Deck_T:
    """Handler for when n < 0"""
    assert(n < 0)
    l = list(deck)
    return itertools.chain(l[n:], l[:n])


def cutN(deck: Deck_T, n: int) -> Deck_T:
    """Preform the cut operation"""
    if n == 0:
        return deck
    if n < 0:
        return _cutNegN(deck, n)
    
    l = list(itertools.islice(deck, n))
    return itertools.chain(deck, l)


def dealWithIncrementN(deck: Deck_T, n: int) -> Deck_T:
    """Deal with the increment n"""
    old = list(zip(deck, itertools.count(0, n)))
    l = len(old)
    assert(l != 0)
    old.sort(key=(lambda x: x[1]%l))
    return map(lambda x: x[0], old)


def shuffle(deck: Deck_T, deals: list[str]) -> Deck_T:
    """Apply a series of deals onto deck"""
    new_deck = deck
    for d in deals:
        s = d.split()

        if s[0] == "cut":
            new_deck = cutN(new_deck, int(s[1]))
        elif s[0] == "deal":
            if s[-1] == "stack":
                new_deck = dealIntoNewStack(new_deck)
            else:
                new_deck = dealWithIncrementN(new_deck, int(s[-1]))
        else:
            raise ValueError(d)
    return new_deck


def shuffleFromFactoryOrder(num_cards: int, deals: list[str]) -> Deck_T:
    """Do all the deals from a factory order deck of n cards"""
    return shuffle(iter(range(num_cards)), deals)


def y2019d22_tests() -> bool:
    """Run tests and return `True` iff all are passing"""

    r = shuffleFromFactoryOrder(10, [
        "deal with increment 7",
        "deal into new stack",
        "deal into new stack",
    ])
    assert(list(r) == [0,3,6,9,2,5,8,1,4,7])

    r = shuffleFromFactoryOrder(10, [
        "cut 6",
        "deal with increment 7",
        "deal into new stack",
    ])
    assert(list(r) == [3,0,7,4,1,8,5,2,9,6])

    r = shuffleFromFactoryOrder(10, [
        "deal with increment 7",
        "deal with increment 9",
        "cut -2",
    ])
    assert(list(r) == [6,3,0,7,4,1,8,5,2,9])

    r = shuffleFromFactoryOrder(10, [
        "deal into new stack",
        "cut -2",
        "deal with increment 7",
        "cut 8",
        "cut -4",
        "deal with increment 7",
        "cut 3",
        "deal with increment 9",
        "deal with increment 3",
        "cut -1",
    ])
    assert(list(r) == [9,2,5,8,1,4,7,0,3,6])
    return True


def y2019d22(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d22.txt"
    print("2019 day 22:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    assert(y2019d22_tests())

    deck = shuffleFromFactoryOrder(10007, lineList)

    for i, v in enumerate(deck):
        if v == 2019:
            Part_1_Answer = i
            break

    # Not sure how to continue
    #   but fairly sure its Chinese Remainder Theorem:
    #       Each step will be cyclic in some period
    #       so the whole thing will be cyclic in some period
    #       so we can get it to just a remainder
    #   then rewrite the deals to take an index and size and say where
    #       the next index is 
    # TODO

    return (Part_1_Answer, Part_2_Answer)