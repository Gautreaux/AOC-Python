import heapq
from typing import TypeVar, Generic


T = TypeVar("T")


class _PQElement(Generic[T]):
    def __init__(self, value: T, priority: float):
        self.value: T = value
        self.p: float = priority

    def __lt__(self, other: "_PQElement"):
        return self.p < other.p


class PQueue(Generic[T]):
    def __init__(self):
        self._list = []

    def __len__(self) -> int:
        return len(self._list)

    def push(self, item: T, priority: float):
        k = _PQElement(item, priority)
        heapq.heappush(self._list, k)

    def popMin(self) -> T:
        k: _PQElement = heapq.heappop(self._list)
        return k.value
