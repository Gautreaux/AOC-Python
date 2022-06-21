# from AOC_Lib.name import *


import itertools
from typing import Generator, Iterator, Optional
    

class MarbleCircle:
    """Manages the marble circle (DLList)"""

    class Marble:
        """A Mable (DLList Node)"""

        def __init__(self, value: int) -> None:
            self.clockwise: Optional[MarbleCircle.Marble] = None
            self.counterclockwise: Optional[MarbleCircle.Marble] = None
            self.value = value

        def _insertClockwise(self, value: int) -> "MarbleCircle.Marble":
            """Construct and insert a new Marble clockwise of this marble"""
            m = MarbleCircle.Marble(value)
            m.clockwise = self.clockwise
            m.clockwise.counterclockwise = m
            self.clockwise = m
            m.counterclockwise = self
            return m
        
        def _insertCounterClockwise(self, value: int) -> "MarbleCircle.Marble":
            """Construct and insert a new Marble counter-clockwise of this marble"""
            return self.counterclockwise.insertClockwise(value)

        def _remove(self) -> Optional["MarbleCircle.Marble"]:
            """Remove self from the DLList
                Returns a reference to the next item clockwise, if one exists
            """
            self.counterclockwise.clockwise = self.clockwise
            self.clockwise.counterclockwise = self.counterclockwise
            _r = self.clockwise
            self.clockwise = None
            self.counterclockwise = None

            if _r == self:
                return None
            else:
                return _r
    
    def __init__(self) -> None:
        # The representation of the circle, with the current marble first
        self._current_marble: MarbleCircle.Marble = MarbleCircle.Marble(0)
        self._current_marble.clockwise = self._current_marble
        self._current_marble.counterclockwise = self._current_marble

    def addMarble(self, v: int, n:int = 1) -> None:
        """Add a marble to the circle between the marbles n and n+1 steps clockwise
            and make this the new marble the current marble
        """
        assert(n >= 0)
        for _ in range(n):
            self._current_marble = self._current_marble.clockwise
        self._current_marble = self._current_marble._insertClockwise(v)

    def removeMarbleCCW(self, n: int = 7) -> Marble:
        """Remove and return the marble n places Counter Clockwise of the current marble"""
        assert(n >= 0)
        for _ in range(n):
            self._current_marble = self._current_marble.counterclockwise
        _r = self._current_marble
        self._current_marble = _r._remove()
        return _r

    def __iter__(self) -> Generator[Marble, None, None]:
        t = self._current_marble
        while True:
            yield(t)
            t = t.clockwise

    def __str__(self) -> str:
        return " ".join(map(lambda x: str(x.value), self.IterOnceCycle()))

    def IterOnceCycle(self) -> Iterator[Marble]:
        """Return a iterator that produces one clockwise cycle, starting with the current marble"""
        itr = iter(self)
        start = next(itr)
        return itertools.chain([start], itertools.takewhile(lambda x: x != start, itr))


class Player:
    """A single Player"""
    def __init__(self, player_id: int) -> None:
        self._score = 0
        self.player_id = player_id

    @property
    def score(self) -> int:
        return self._score

    def takeMarble(self, m: MarbleCircle.Marble) -> None:
        self._score += m.value


def getHighestScore(num_players: int, last_points: int) -> int:
    """Play a game and return the highest score"""
    
    all_players = list(map(lambda x: Player(x), range(num_players)))
    mc = MarbleCircle()

    for player,marble_no in zip(
        itertools.cycle(all_players),
        range(1, last_points+1),
    ):
        if(marble_no % 23 == 0):
            player.takeMarble(MarbleCircle.Marble(marble_no))
            player.takeMarble(mc.removeMarbleCCW(n=7))
        else:
            mc.addMarble(marble_no, n=1)

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