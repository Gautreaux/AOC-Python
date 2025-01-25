
import collections
from itertools import islice
from typing import Iterable, TypeVar

IteratedType_T = TypeVar('IteratedType_T')


# from the itertools docs
def sliding_window(iterable: Iterable[IteratedType_T], n: int) -> Iterable[tuple[IteratedType_T, ...]]:
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


# also from the itertools docs
def batched(iterable: Iterable[IteratedType_T], n: int) -> Iterable[tuple[IteratedType_T, ...]]:
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := tuple(islice(it, n))):
        yield batch
