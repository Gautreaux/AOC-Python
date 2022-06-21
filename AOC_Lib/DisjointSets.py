
from typing import Hashable, Iterable, Optional

class DisjointSets():
    
    def __init__(self, initial:Optional[Iterable[Hashable]] = None, allow_insert:bool=True,) -> None:
        self._d = {}
        self._allow_insert = allow_insert
        self._total_sets = 0

        if initial is not None:
            for k in initial:
                assert(k not in self._d)
                self._total_sets += 1
                self._d[k] = k

    def __len__(self) -> int:
        """Return the number of disjoint sets"""
        return self._total_sets

    def union(self, a: Hashable, b: Hashable) -> None:
        """Union the two items together, inserting them if they are new"""
        af = self.find(a)
        bf = self.find(b)
        if af != bf:
            self._d[bf] = af
            self._total_sets -= 1

    def find(self, a: Hashable) -> Hashable:
        """Find for `a` and path compress, inserting if non-existent"""
        if a not in self._d:
            if self._allow_insert:
                self._total_sets += 1
                self._d[a] = a
                return a
            else:
                raise KeyError(f"`{a}` does not exist and `allow_insert` is `False`")

        _to_compress = []
        t = a

        while(self._d[t] != t):
            _to_compress.append(t)
            t = self._d[t]
        for x in _to_compress:
            self._d[x] = t
        return t

    def areInSameGroups(self, a: Hashable, b: Hashable) -> bool:
        """Return `True` iff a and b are in the same set"""
        return (self.find(a) == self.find(b))
            