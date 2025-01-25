# from AOC_Lib.name import *

from copy import deepcopy
from typing import Iterable, List, Optional, Tuple

NEGATIVE_ZERO = -0xFFFFFFFF


class BreakAll(Exception):
    pass


class BingoBoard:
    def __init__(self, num_rows: int = 0, num_cols: int = 0) -> None:
        self._dims = (num_rows, num_cols)
        self._board = [None] * (num_rows * num_cols)
        self.clearMarks()

    def markCell(self, cell: int, check: Optional[int] = None) -> None:
        """
        Mark the cell as taken,
        if check is provided, assert the value at the cell matches
        """

        if check != None:
            assert self._board[cell] == check
        self._marked[cell] = True

    def setCell(
        self,
        cell: int,
        value: int,
        allow_overwrite: bool = False,
        clear_marked: bool = True,
    ) -> None:
        """
        Set the cell to value
        error if allow_overwrite is false and value was set
        """

        if not allow_overwrite:
            assert self._board[cell] == None
        self._board[cell] = value

        if clear_marked:
            self._marked[cell] = False

    def isColWinner(self, column_id: int) -> bool:
        assert column_id >= 0 and column_id < self._dims[1]
        for i in range(self._dims[0]):
            if not self._marked[i * self._dims[1] + column_id]:
                return False
        return True

    def isRowWinner(self, row_id: int) -> bool:
        assert row_id >= 0 and row_id < self._dims[0]
        for i in range(self._dims[1]):
            if not self._marked[row_id * self._dims[1] + i]:
                return False
        return True

    def isDiagonalWinner(self) -> bool:
        """
        Check if the \ diagonal is winner
        Only works on squares
        """
        assert self._dims[0] == self._dims[1]
        for i in range(self._dims[0]):
            if not self._marked[i * self._dims[1] + i]:
                return False
        return True

    def isDiagonalWinnerAlt(self) -> bool:
        """
        Check if the / diagonal is winner
        Only works on squares
        """
        assert self._dims[0] == self._dims[1]
        for i in range(self._dims[0]):
            if not self._marked[i * self._dims[1] + self._dims[1] - i - 1]:
                return False
        return True

    def isWinner(self, print_winner=True) -> bool:
        """Check all rows, columns, and diagonals for winners"""
        for r in range(self._dims[0]):
            if self.isRowWinner(r):
                if print_winner:
                    print(f"Winner in row {r}")
                return True
        for c in range(self._dims[1]):
            if self.isColWinner(c):
                if print_winner:
                    print(f"Winner in col {c}")
                return True
        # diagonals dont count
        # if self.isDiagonalWinner() or self.isDiagonalWinnerAlt():
        #     return True
        return False

    def getUnmarkedSum(self) -> int:
        total = 0
        for c, m in zip(self._board, self._marked):
            if m is False:
                total += c
        return total

    @classmethod
    def fromLineIter(cls, itr: Iterable, num_rows: int = 5) -> "BingoBoard":
        cells = []

        num_cols = None

        for _ in range(num_rows):
            l = next(itr)
            cells.extend(map(int, l.replace("  ", " ").split(" ")))

            if num_cols == None:
                num_cols = len(cells)
            else:
                # check that the latest line did append the proper number
                assert len(cells) % num_cols == 0

        b = BingoBoard(num_rows=num_rows, num_cols=num_cols)
        b._board = cells
        return b

    def markByNumber(self, value):
        for i, k in enumerate(self._board):
            if k == value:
                self.markCell(i)

    def clearMarks(self):
        self._marked = [False] * (self._dims[0] * self._dims[1])


def y2021d4(inputPath=None):
    if inputPath == None:
        inputPath = "Input2021/d4.txt"
    print("2021 day 4:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    number_list = list(map(int, lineList[0].split(",")))

    itr = iter(lineList)
    next(itr)
    next(itr)

    bingo_boards: List[BingoBoard] = []

    while True:
        try:
            bingo_boards.append(BingoBoard.fromLineIter(itr, num_rows=5))
            next(itr)  # for the empty lines
        except StopIteration:
            break

    print(f"Loaded {len(bingo_boards)} bingo boards, {len(number_list)} numbers")
    print(number_list)

    try:
        for number in number_list:
            for b in bingo_boards:
                b.markByNumber(number)
                if b.isWinner():
                    Part_1_Answer = b.getUnmarkedSum() * number
                    print(
                        f"Found first winner after number {number}, um_sum {b.getUnmarkedSum()}"
                    )
                    print(list(zip(b._board, b._marked)))
                    raise BreakAll
        raise RuntimeError("No winning board found")
    except BreakAll:
        pass

    print(bingo_boards[-1]._board)

    for b in bingo_boards:
        b.clearMarks()
    o_non_winners = bingo_boards

    for number in number_list:
        non_winners = []
        this_winners = []

        for b in o_non_winners:
            b.markByNumber(number)
            if b.isWinner(print_winner=False):
                print(f"Board removed after {number} : {b._board[:5]}")
                this_winners.append(b)
            else:
                non_winners.append(b)

        if len(non_winners) == 0:
            assert len(this_winners) == 1
            last_winner = this_winners[0]
            break
        else:
            o_non_winners = non_winners

    print((last_winner.getUnmarkedSum(), number))
    print(last_winner._board)
    Part_2_Answer = last_winner.getUnmarkedSum() * number

    assert Part_2_Answer > 2896

    return (Part_1_Answer, Part_2_Answer)
