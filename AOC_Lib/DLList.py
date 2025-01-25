import itertools
from typing import Any, Generator, Iterator, Optional

# Designed for y2018d9
#   used elsewhere too


class DLList:
    """Manages the (circular) DLList"""

    class DLListNode:
        """A Mable (DLList Node)"""

        def __init__(self, value: Any, dllist: Optional["DLList"] = None) -> None:
            self.clockwise: DLList.DLListNode = self
            self.counterclockwise: DLList.DLListNode = self
            self.value = value
            self._list: DLList = dllist

        def _insertClockwise(self, value: Any) -> "DLList.DLListNode":
            """Construct and insert a new DLListNode clockwise of this DLListNode"""
            m = DLList.DLListNode(value, self._list)
            m.clockwise = self.clockwise
            m.clockwise.counterclockwise = m
            self.clockwise = m
            m.counterclockwise = self
            self._list._len += 1
            return m

        def _insertCounterClockwise(self, value: Any) -> "DLList.DLListNode":
            """Construct and insert a new DLListNode counter-clockwise of this DLListNode"""
            return self.counterclockwise.insertClockwise(value)

        def _remove(self) -> Optional["DLList.DLListNode"]:
            """Remove self from the DLList
            Returns a reference to the next item clockwise, if one exists
            """
            if self._list:
                self._list._PreRemove(self)

            self.counterclockwise.clockwise = self.clockwise
            self.clockwise.counterclockwise = self.counterclockwise
            _r = self.clockwise
            self.clockwise = None
            self.counterclockwise = None

            self._list._len -= 1
            self._list = None

            if _r == self:
                return None
            else:
                return _r

        def swapValues(self, other: "DLList.DLListNone") -> None:
            """Swap values with the other node"""
            assert id(self._list) == id(self._list)
            t = self.value
            self.value = other.value
            other.value = t

    def __init__(self) -> None:
        # The representation of the circle, with the current DLListNode first
        self._len = 0
        self._current_DLListNode: Optional[DLList.DLListNode] = None

    def __len__(self) -> int:
        return self._len

    def _PreRemove(self, n: "DLList.DLListNode"):
        """A pre-remove hook indicating the node `n` is about to be removed"""
        if n == self._current_DLListNode:
            if len(self) == 1:
                self._current_DLListNode = None
            else:
                self._current_DLListNode = self._current_DLListNode.clockwise

    @property
    def current(self) -> "DLList.DLListNode":
        """Return the current node"""
        return self._current_DLListNode

    def addDLListNode(self, v: Any, n: int = 1) -> None:
        """Add a DLListNode to the circle between the DLListNodes n and n+1 steps clockwise
        and make this the new DLListNode the current DLListNode

        If there is no node, `n` is ignored
        """
        if len(self) == 0:
            assert self._current_DLListNode is None
            self._current_DLListNode = DLList.DLListNode(0, self)
            self._len = 1
            return

        assert n >= 0
        self.Rotate(n)
        self._current_DLListNode = self._current_DLListNode._insertClockwise(v)

    def removeDLListNodeCCW(self, n: Any = 1) -> DLListNode:
        """Remove and return the DLListNode n places Counter Clockwise of the current DLListNode"""
        assert n >= 0
        self.Rotate(-n)
        _r = self._current_DLListNode
        self._current_DLListNode = _r._remove()
        return _r

    def __iter__(self) -> Generator[DLListNode, None, None]:
        t = self._current_DLListNode
        while True:
            yield (t)
            t = t.clockwise

    def __str__(self) -> str:
        return " ".join(map(lambda x: str(x.value), self.IterOnceCycle()))

    def IterOnceCycle(self) -> Iterator[DLListNode]:
        """Return a iterator that produces one clockwise cycle, starting with the current DLListNode"""
        itr = iter(self)
        start = next(itr)
        return itertools.chain([start], itertools.takewhile(lambda x: x != start, itr))

    def Rotate(self, n: int) -> DLListNode:
        """Advance the current node by `n` steps in the Clockwise direction
        supports n < 0 for counterclockwise rotation
        """
        if n > 0:
            for _ in range(n % len(self)):
                self._current_DLListNode = self._current_DLListNode.clockwise
        else:
            for _ in range((-n) % len(self)):
                self._current_DLListNode = self._current_DLListNode.counterclockwise
        return self._current_DLListNode
