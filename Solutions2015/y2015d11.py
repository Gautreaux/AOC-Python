# from AOC_Lib.name import *

import itertools
from typing import Generator, Iterable

_CHARSET = "abcdefghijklmnopqrstuvwxyz"


def placeGenerator(start: str, charset: str = _CHARSET) -> Generator[str, None, None]:
    """Generate things that go at a particular place"""

    assert len(start) == 1

    itr = iter(charset)

    for i in itr:
        if i != start:
            continue
        yield i
        break

    for i in itr:
        yield i


def candidateGenerator(
    start: str, charset: str = _CHARSET
) -> Generator[tuple, None, None]:
    """Generate all candidates after and including the start
    NOTE: will not loop to explore things before the start
    """
    if len(start) == 1:
        for c in placeGenerator(start, charset=charset):
            yield c
        return

    t = start[0]
    n = start[1:]

    # do this one, until it is exhausted
    for c in candidateGenerator(n, charset=charset):
        yield (t, *c)

    # do the remainder
    itr = placeGenerator(t, charset=charset)
    next(itr)
    b = charset[0] * len(n)
    for t in itr:
        for c in candidateGenerator(b, charset=charset):
            yield (t, *c)


# new in python 3.10
def pairwise(itr: Iterable) -> Iterable:
    a, b = itertools.tee(itr)
    next(b, None)
    return zip(a, b)


def tuplewise(itr: Iterable) -> Iterable:
    a, b, c = itertools.tee(itr, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)


def filterFunction(s: Iterable) -> bool:
    """Return true iff `s` is a valid password

    NOTE: does not check for `iol` - exclude these at generation time
    """

    # question on meaning of different in "different non-overlaping"
    #   going to assume that its different letters

    pair_letters = set()
    tuples = tuplewise(s)

    has_valid_incr: bool = False

    for x, y, z in tuples:
        if x == y:
            pair_letters.add(x)
        if y == z:
            pair_letters.add(z)

        if ((ord(y) - ord(x)) == 1) and ((ord(z) - ord(y)) == 1):
            has_valid_incr = True

    if len(pair_letters) < 2:
        return False

    return has_valid_incr


def y2015d11(inputPath=None):
    if inputPath == None:
        inputPath = "Input2015/d11.txt"
    print("2015 day 11:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # build the charset (enforce contition 2 at generation time)
    my_charset = "".join(f for f in _CHARSET if f not in "iol")

    # in hindsight, you could probably construct the result
    #   no need to explicitly generate the candidates
    password_generator = filter(
        filterFunction, candidateGenerator(lineList[0], charset=my_charset)
    )

    # start_password = next(password_generator)
    # assert(start_password == lineList[0])
    Part_1_Answer = "".join(next(password_generator))
    Part_2_Answer = "".join(next(password_generator))

    return (Part_1_Answer, Part_2_Answer)
