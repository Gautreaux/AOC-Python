# from AOC_Lib.name import *


from hashlib import md5
import itertools
import multiprocessing

from AOC_Lib.SolutionBase import SolutionBase

# How big each chunk is
_CHUNK_OFFSET = 50000

# How often to synchronize results from all chunks
_BATCH_INTERVAL = 10


def _fn(t: tuple[str, int]) -> list[tuple[int, str]]:
    key, start = t
    l = []

    for i in itertools.islice(
        itertools.count(start=start * _CHUNK_OFFSET), _CHUNK_OFFSET
    ):
        v = md5(f"{key}{i}".encode("ascii")).hexdigest()

        if v.startswith("00000"):
            # only capture the first result
            if len(l) == 0:
                l.append((i, v))
        elif v.startswith("000000"):
            # can stop once we get the first six-digit result
            #   which could also be the first five-digit result
            l.append((i, v))
            break
    return l


class _ExitException(Exception):
    """Raised to signal we are done"""


class Solution_2015_04(SolutionBase):
    """https://adventofcode.com/2015/day/4"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        my_key = self.input_str()

        pool = multiprocessing.Pool()

        ctr = itertools.count()

        try:
            for z in itertools.count():
                for l in pool.map(
                    _fn,
                    zip(
                        itertools.repeat(my_key), itertools.islice(ctr, _BATCH_INTERVAL)
                    ),
                    chunksize=_CHUNK_OFFSET,
                ):
                    for i, r in l:
                        print(f"Possible answer: {i}")
                        if self._part_1_answer is None and r.startswith("00000"):
                            self._part_1_answer = i
                            print(f"Part 1 answer: {i}")
                            if self._part_2_answer:
                                raise _ExitException()
                        if self.part_2_answer is None and r.startswith("000000"):
                            self._part_2_answer = i
                            if self._part_1_answer:
                                raise _ExitException()
                print(
                    f"Finished batch {z:>4} ({((z+1)*_CHUNK_OFFSET*_BATCH_INTERVAL):>10})"
                )
        except _ExitException:
            pass
