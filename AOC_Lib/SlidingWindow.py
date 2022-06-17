
import collections
from itertools import islice
from typing import Any, Iterable

# from the itertools docs
def sliding_window(iterable: Iterable[Any], n) -> Iterable[tuple[Any]]:
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)
