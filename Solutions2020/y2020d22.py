# from AOC_Lib.name import *

from copy import deepcopy
from typing import Optional, Tuple

from AOC_Lib.queue import CircularQueue


def calculateScore(winningDeck: CircularQueue) -> int:
    score = 0

    while len(winningDeck) > 0:
        i = len(winningDeck)
        score += i * winningDeck.pop()

    return score


def getCacheKeyValue(
    Player_1_Deck: CircularQueue, Player_2_Deck: CircularQueue
) -> Tuple[Tuple[int, int], Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    key = (len(Player_1_Deck), len(Player_2_Deck))
    value = (
        tuple(Player_1_Deck.generatorNonConsuming()),
        tuple(Player_2_Deck.generatorNonConsuming()),
    )
    return (key, value)


recursionCache = {}


def playRecursiveCombatGame(
    Player_1_Deck: CircularQueue, Player_2_Deck: CircularQueue
) -> Tuple[Optional[CircularQueue], Optional[CircularQueue]]:
    _, start_v = getCacheKeyValue(Player_1_Deck, Player_2_Deck)
    if start_v in recursionCache:
        return recursionCache[start_v]

    statesCache = set()

    while True:
        # checking if someone has won
        if len(Player_2_Deck) == 0:
            toReturn = (Player_1_Deck, None)
            recursionCache[start_v] = toReturn
            return toReturn
        if len(Player_1_Deck) == 0:
            toReturn = (None, Player_2_Deck)
            recursionCache[start_v] = toReturn
            return toReturn

        # checking to see if the state was already visited
        _, v = getCacheKeyValue(Player_1_Deck, Player_2_Deck)
        if v in statesCache:
            toReturn = (Player_1_Deck, None)
            recursionCache[start_v] = toReturn
            return toReturn
        statesCache.add(v)

        # now deal
        P1_card = Player_1_Deck.pop()
        P2_card = Player_2_Deck.pop()

        # checking if able to recurse
        if len(Player_2_Deck) >= P2_card and len(Player_1_Deck) >= P1_card:
            # able to recurse
            New_P1_Deck = Player_1_Deck.copyN(P1_card)
            New_P2_Deck = Player_2_Deck.copyN(P2_card)

            assert len(New_P1_Deck) == P1_card
            assert len(New_P2_Deck) == P2_card

            results = playRecursiveCombatGame(New_P1_Deck, New_P2_Deck)
            assert len(results) == 2

            if results[0] != None:
                assert results[1] == None
                # player 1 won
                Player_1_Deck.push(P1_card)
                Player_1_Deck.push(P2_card)
            elif results[1] != None:
                assert results[0] == None
                # player 2 won
                Player_2_Deck.push(P2_card)
                Player_2_Deck.push(P1_card)
            else:
                print(results)
                raise RuntimeError()
        else:
            # unable to recurse
            # higher value card wins the round
            if P1_card > P2_card:
                Player_1_Deck.push(P1_card)
                Player_1_Deck.push(P2_card)
            else:
                Player_2_Deck.push(P2_card)
                Player_2_Deck.push(P1_card)


def y2020d22(inputPath=None):
    if inputPath == None:
        inputPath = "Input2020/d22.txt"
    print("2020 day 22:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    linesIterable = iter(lineList)

    k = next(linesIterable)
    assert "Player" in k
    Player_1_Deck = []
    for row in linesIterable:
        if row == "":
            break
        Player_1_Deck.append(int(row))

    k = next(linesIterable)
    assert "Player" in k
    Player_2_Deck = []
    for row in linesIterable:
        if row == "":
            break
        Player_2_Deck.append(int(row))

    # TODO - remove DEBUG
    # print("DEBUG ON")
    # Player_1_Deck = [9,2,6,3,1]
    # Player_2_Deck = [5,8,4,7,10]

    totalCards = len(Player_1_Deck) + len(Player_2_Deck)

    Player_1_Deck = CircularQueue(totalCards, Player_1_Deck)
    Player_2_Deck = CircularQueue(totalCards, Player_2_Deck)

    # just storing for part 2
    Player_1_Deck_copy = deepcopy(Player_1_Deck)
    Player_2_Deck_copy = deepcopy(Player_2_Deck)

    while (len(Player_1_Deck) * len(Player_2_Deck)) > 0:
        P1_card = Player_1_Deck.pop()
        P2_card = Player_2_Deck.pop()

        if P1_card > P2_card:
            Player_1_Deck.push(P1_card)
            Player_1_Deck.push(P2_card)
        else:
            Player_2_Deck.push(P2_card)
            Player_2_Deck.push(P1_card)

    winningDeck = Player_1_Deck if len(Player_1_Deck) > 0 else Player_2_Deck
    losingDeck = Player_2_Deck if winningDeck == Player_1_Deck else Player_1_Deck

    assert len(winningDeck) == totalCards
    assert len(losingDeck) == 0

    Part_1_Answer = calculateScore(winningDeck)

    results = playRecursiveCombatGame(Player_1_Deck_copy, Player_2_Deck_copy)

    assert len(results) == 2
    assert None in results
    assert (results[0] is not None) or (results[1] is not None)
    if results[0] != None:
        Part_2_Answer = calculateScore(results[0])
    else:
        Part_2_Answer = calculateScore(results[1])

    return (Part_1_Answer, Part_2_Answer)
