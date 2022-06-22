# from AOC_Lib.name import *

from collections import Counter
from itertools import tee
from copy import copy

# TODO - in standard library in py3.10
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


# a collection of substitutions
SUBS_T = dict[str, str]


ElementCounter_T = Counter[str]


class PolymerExpander:

    def __init__(self, subs: SUBS_T) -> None:
        self._subs = subs
        self._cache = {}
        self._r_depth = 0

    @classmethod
    def parseLine(cls, s: str) -> tuple[str, str]:
        """Parse a str into a singular substitution"""
        k,_,v = s.partition(" -> ")
        assert(len(k) == 2)
        assert(len(v) == 1)
        return (k,v)
    
    @classmethod
    def fromLineList(cls, lineList: list[str]) -> "PolymerExpander":
        """Build a PolymerExpander from a list of lines"""
        s = {k:v for k,v in map(cls.parseLine, lineList)}
        pe = cls(s)
        return pe

    # functools.cache didn't work?
    def _ExpansionCount(self, s: str, num_rounds: int) -> ElementCounter_T:
        """Worker for _ExpansionCount"""
        if num_rounds <= 0:
            return Counter(s)

        if len(s) > 2:
            c = Counter()
            for p in pairwise(s):
                p = "".join(p)
                e = self.ExpansionCount(p, num_rounds)
                # print("  RECR: ", p, num_rounds, "->", e)
                # print(c, "+=", e, "-> ", end="")
                c.update(e)
                # print(c)
            c.subtract(s[1:-1])
            return c

        assert(len(s) == 2)
        try:
            r = self._subs[s]
        except KeyError:
            return Counter(s)

        lhs = s[0] + r
        rhs = r + s[1]
        e_lhs = self.ExpansionCount(lhs, num_rounds-1)
        e_rhs = self.ExpansionCount(rhs, num_rounds-1)

        e_lhs.update(e_rhs)
        e_lhs.subtract([r])
        return e_lhs
    

    def ExpansionCount(self, s: str, num_rounds: int) -> ElementCounter_T:
        """Calculate the quantity of each Element in the molecule
            resulting from expanding `s` `num_rounds` times
        """
        t = (s,num_rounds)

        # print(" "*self._r_depth*4, "GET", t)
        try:
            a = self._cache[t]
        except KeyError:
            # print(" "*self._r_depth*4,"COMPUTE", t)
            self._r_depth += 1
            a = self._ExpansionCount(s, num_rounds)
            self._r_depth -= 1
            self._cache[t] = a
            # print(" "*self._r_depth*4,"SET CACHE", t, a)
        return copy(a)


def getMinMaxDiff(c: ElementCounter_T) -> int:
    """Return the difference between the min and max count"""
    l = list(c.values())
    return max(l) - min(l)


def y2021d14_tests():
    lineList = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""".splitlines()

    def assert_expansion(lhs: ElementCounter_T, rhs: ElementCounter_T) -> None:
        if lhs != rhs:
            lhs_t = sum(lhs.values())
            rhs_t = sum(rhs.values())
            print(lhs, rhs)
            print("  ", lhs_t, rhs_t)
        assert(lhs == rhs)

    em = PolymerExpander.fromLineList(lineList[2:])

    assert_expansion(em.ExpansionCount("CH", 0), Counter("CH"))
    assert_expansion(em.ExpansionCount("HH", 0), Counter("HH"))
    assert_expansion(em.ExpansionCount("CHH", 0), Counter("CHH"))
    assert_expansion(em.ExpansionCount("zN", 0), Counter("zN"))
    assert_expansion(em.ExpansionCount("zz", 0), Counter("zz"))
    
    assert_expansion(em.ExpansionCount("CH", 1), Counter("CBH"))
    assert_expansion(em.ExpansionCount("HH", 1), Counter("HNH"))
    assert_expansion(em.ExpansionCount("CHH", 1), Counter("CBHNH"))
    assert_expansion(em.ExpansionCount("zN", 1), Counter("zN"))
    assert_expansion(em.ExpansionCount("zHN", 1), Counter("zHCN"))
    assert_expansion(em.ExpansionCount("zHz", 1), Counter("zHz"))
    assert_expansion(em.ExpansionCount("NB", 1), Counter("NBB"))
    assert_expansion(em.ExpansionCount("BC", 1), Counter("BBC"))

    assert_expansion(em.ExpansionCount("NN", 0), Counter("NN"))

    assert_expansion(em.ExpansionCount("NN", 1), Counter("NCN"))

    assert_expansion(em.ExpansionCount("NCN", 1), Counter("NBCCN"))
    assert_expansion(em.ExpansionCount("NN", 2),  Counter("NBCCN"))

    assert_expansion(em.ExpansionCount("NBCCN", 1), Counter("NBBBCNCCN"))
    assert_expansion(em.ExpansionCount("NCN", 2),   Counter("NBBBCNCCN"))
    assert_expansion(em.ExpansionCount("NN", 3),    Counter("NBBBCNCCN"))

    # and for the example above
    assert_expansion(lineList[0], "NNCB")
    assert_expansion(em.ExpansionCount("NNCB", 1), Counter("NCNBCHB"))
    assert_expansion(em.ExpansionCount("NNCB", 2), Counter("NBCCNBBBCBHCB"))
    assert_expansion(em.ExpansionCount("NNCB", 3), Counter("NBBBCNCCNBBNBNBBCHBHHBCHB"))
    assert_expansion(em.ExpansionCount("NNCB", 4), Counter("NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"))


def y2021d14(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d14.txt"
    print("2021 day 14:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    y2021d14_tests()

    em = PolymerExpander.fromLineList(lineList[2:])

    c = em.ExpansionCount(lineList[0], 10)

    Part_1_Answer = getMinMaxDiff(c)

    c = em.ExpansionCount(lineList[0], 40)

    Part_2_Answer = getMinMaxDiff(c)

    return (Part_1_Answer, Part_2_Answer)