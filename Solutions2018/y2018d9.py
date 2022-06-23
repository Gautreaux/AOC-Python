# from AOC_Lib.name import *


import itertools
    
from AOC_Lib.DLList import DLList


class Player:
    """A single Player"""
    def __init__(self, player_id: int) -> None:
        self._score = 0
        self.player_id = player_id

    @property
    def score(self) -> int:
        return self._score

    def takeMarble(self, m: DLList.DLListNode) -> None:
        self._score += m.value


def getHighestScore(num_players: int, last_points: int) -> int:
    """Play a game and return the highest score"""
    
    all_players = list(map(lambda x: Player(x), range(num_players)))
    marble_circle = DLList()
    marble_circle.addDLListNode(0)

    for player,marble_no in zip(
        itertools.cycle(all_players),
        range(1, last_points+1),
    ):
        if(marble_no % 23 == 0):
            player.takeMarble(DLList.DLListNode(marble_no))
            player.takeMarble(marble_circle.removeDLListNodeCCW(n=7))
        else:
            marble_circle.addDLListNode(marble_no, n=1)

        # print(f"[{player.player_id}]", str(mc))

    return max(map(lambda x: x.score, all_players))

def y2018d9(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d9.txt"
    print("2018 day 9:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    assert(len(lineList) == 1)
    _s = lineList[0].split()

    num_players = int(_s[0])
    last_points = int(_s[-2])

    # Tests Cases
    _t = [
        ((9, 25),        32),
        ((10, 1618),   8317),
        ((13, 7999), 146373),
        ((17, 1104),   2764),
        ((21, 6111),  54718),
        ((30, 5807),  37305),
    ]

    for (np, lp), e in _t:
        v = getHighestScore(np, lp)
        if e != v:
            print(f"Test {np},{lp} returned: {v}, expected {e}.")
        assert(e == v)

    Part_1_Answer = getHighestScore(num_players, last_points)
    Part_2_Answer = getHighestScore(num_players, last_points*100)

    return (Part_1_Answer, Part_2_Answer)