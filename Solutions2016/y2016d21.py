# from AOC_Lib.name import *

from enum import Enum, unique

from AOC_Lib.DLList import DLList

@unique
class OpType(Enum):
    SWAP_POS = 8
    SWAP_LETTER = 9
    ROTATE_POSITION = 16
    ROTATE_STEPS = 17
    REVERSE_POSITION = 32
    MOVE_POSITION = 64


class PasswordScrambler:
    
    def __init__(self, start_password: str = "abcdefgh") -> None:
        self._list: DLList = DLList()
        for chr in start_password:
            self._list.addDLListNode(chr)

        self._chr_to_node: dict[str, DLList.DLListNode] = {k.value:k for k in self._list.IterOnceCycle()}
        self._fixed_pos_to_node: list[DLList.DLListNode] = list(self._list.IterOnceCycle())
        self._node_to_fixed_pos: dict[DLList.DLListNode, int] = {k:v for v,k in enumerate(self._fixed_pos_to_node)}

    def __len__(self) -> int:
        return len(self._list)

    def _getNodeForPos(self, pos: int) -> DLList.DLListNode:
        """Return a node given a `pos`"""
        offset_fixed_pos = self._node_to_fixed_pos[self._list.current]
        lookup_pos = pos + offset_fixed_pos
        if lookup_pos >= len(self):
            lookup_pos -= len(self)
        return self._fixed_pos_to_node(lookup_pos)

    def _getPosForLetter(self, chr_a: str) -> int:
        fixed_pos = self._node_to_fixed_pos[self._chr_to_node[chr_a]]
        offset_fixed_pos = self._node_to_fixed_pos[self._list.current]
        lookup_pos = offset_fixed_pos - fixed_pos
        if lookup_pos < 0:
            lookup_pos += len(self)
        return lookup_pos

    def getPassword(self) -> str:
        """Get the resulting password"""
        return "".join(self._list.IterOnceCycle())

    def swapPos(self, pos_a: int, pos_b: int) -> None:
        """Swap Positions by index"""
        a = self._getNodeForPos(pos_a)
        b = self._getNodeForPos(pos_b)
        a.swapValues(b)
        self._chr_to_node[b.value] = b
        self._chr_to_node[a.value] = a

    def swapLetter(self, chr_a: str, chr_b: str) -> None:
        """Swap Positions by value"""
        a = self._chr_to_node[chr_a]
        b = self._chr_to_node[chr_b]
        a.swapValues(b)
        self._chr_to_node[a.value] = a
        self._chr_to_node[b.value] = b

    def rotateLeftSteps(self, steps: int) -> None:
        """Rotate left by some amount of steps"""
        self._list.Rotate(steps)

    def rotateRightSteps(self, steps: int) -> None:
        """Rotate right by some amount of steps"""
        self._list.Rotate(-steps)
    
    def rotatePositions(self, chr_a: str) -> None:
        """Rotate based on position"""
        i = self._getPosForLetter(chr_a)
        self.rotateRightSteps(i*2 + (1 if i < 4 else 2))

    def reversePositions(self, pos_a: int, pos_b: int) -> None:
        """Reverse based on position"""
        raise NotImplementedError()

    def MovePosition(self, pos_a: int, pos_b: int) -> None:
        """Move based on position"""
        raise NotImplementedError()

def y2016d21(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2016/d21.txt"
    print("2016 day 21:")

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

    return (Part_1_Answer, Part_2_Answer)