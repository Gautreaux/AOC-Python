# from AOC_Lib.name import *

from copy import deepcopy
from typing import Iterable, List, Tuple

NEGATIVE_ZERO = -0xFFFFFFFF

class BreakAll(Exception):
    pass

class BingoBoard:
    def __init__(self, num_rows:int=0, num_cols:int=0) -> None:
        self._dims = (num_rows, num_cols)
        self._board = []

        a_row = [None]*num_cols

        while len(self._board) < num_rows:
            self._board.append(deepcopy(a_row))

    def markNumber(self, num: int) -> Tuple[bool, bool]:
        """
        Returns pair (was_marked, marked_winner)
            bool if any number was marked
            bool if any marked number is on a winning part of the board

        NOTE: marked_winner may return false even though the board
            was already a winner. 
        NOTE: marked_winner may return false even `was_marked`
            is true AND the board was a winner
        """

        marked_something = False
        is_now_winner = False

        for i, row in enumerate(self._board):
            for j, cell in enumerate(row):
                if cell != num:
                    continue

                if cell == 0:
                    self._board[i][j] == NEGATIVE_ZERO
                else:
                    self._board[i][j] == -cell

                marked_something = True

                if is_now_winner:
                    # someone else already marked this as winner
                    # so no need to check anymore
                    continue

                # check and see if this is now a winner
                
                # check the row
                row_winner = True
                for j_t in range(self._dims[1]):
                    if self._board[i][j_t] >= 0:
                        row_winner = False
                        break
                if row_winner:
                    is_now_winner = True
                    continue

                # check the column
                col_winner = True
                for i_t in range(self._dims[0]):
                    if self._board[i_t][j] >= 0:
                        col_winner = False
                        break
                if col_winner:
                    is_now_winner = True
                    continue

                # check the diagonal
                # assert(self._dims[0] == self._dims[1])
                # if(i == j):
                # need to check the \ diagonal
                # also need to check the / diagonal
                raise NotImplementedError()

        return (marked_something, is_now_winner)
    
    def isWinner(self) -> bool:
        raise NotImplementedError()

    def getUnmarkedSum(self) -> int:
        s = 0
        for i, row in enumerate(self._board):
            for j, cell in enumerate(row):
                if cell >= 0:
                    s += cell
        return s

    @classmethod
    def fromLineIter(cls, itr: Iterable, num_rows:int = 5) -> "BingoBoard":
        lines = []

        for _ in range(num_rows):
            l = next(itr)
            lines.append(l.replace("  ", " "))

        num_cols = len(lines[0].split(" "))

        b = BingoBoard(num_rows=num_rows, num_cols=num_cols)

        for i, row_s in enumerate(lines):
            row = row_s.split(" ")
            for j, cell_s in enumerate(row):
                assert(int(cell_s) >= 0)
                b._board[i][j] = int(cell_s)
        return b


def y2021d4(inputPath = None):
    if(inputPath == None):
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
            next(itr) # for the empty lines
        except StopIteration:
            break

    print(f"Loaded {len(bingo_boards)} bingo boards, {len(number_list)} numbers")

    try:
        for number in number_list:
            for b in bingo_boards:
                _,w = b.markNumber(number)
                if w:
                    Part_1_Answer = b.getUnmarkedSum() * number
                    raise BreakAll
        raise RuntimeError("No winning board found")
    except BreakAll:
        pass

    return (Part_1_Answer, Part_2_Answer)