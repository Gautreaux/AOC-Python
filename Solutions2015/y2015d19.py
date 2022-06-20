# from AOC_Lib.name import *

from collections import defaultdict, deque
import functools
import itertools
from typing import Generator

SOME_BIG_NUMBER = 2**24

ATOM_T = str

MOLECULE_T = tuple[ATOM_T, ...]

# a forward translation from str to str
F_TRANSLATION_T = tuple[ATOM_T, MOLECULE_T]

RN_TRANSLATIONS: list[dict[MOLECULE_T, ATOM_T]] = []

UNIQUE_INVOCATIONS: int = 0 

def isAtom(s: str) -> bool:
    """Return true iff this is an atom"""
    if not s:
        return False
    if s == "e":
        return True
    if not s[0].isupper:
        return False
    return (1 == sum(1 for c in s if c.isupper()))


def parseMolecule(s: str) -> MOLECULE_T:
    """Parse a single molecule"""
    # not efficient lol

    def _g():
        for c in s:
            if c.isupper():
                yield " "
            yield c

    comps = "".join(_g()).strip().split() 
    assert(all(map(lambda x: isAtom(x), comps)))
    assert(len("".join(comps)) == len(s))
    return tuple(comps)


def _generateSingleExpansion(
    molecule: MOLECULE_T, 
    base: ATOM_T, 
    derived: MOLECULE_T
) -> Generator[MOLECULE_T, None, None]:
    """Generate all expansions for a specific molecule/atom pair"""
    lhs = []
    rhs_reversed = list(reversed(molecule))
    while rhs_reversed:
        i = rhs_reversed.pop()
        if i == base:
            t = tuple(itertools.chain(lhs, derived, reversed(rhs_reversed)))
            yield t
        lhs.append(i)
        assert(len(molecule) == (len(lhs) + len(rhs_reversed)))



def generateExpansions(molecule:MOLECULE_T, translations: list[F_TRANSLATION_T]) -> Generator[MOLECULE_T, None, None]:
    """Generate all molecules derived from the input and translations"""
    # items already yielded
    yielded = set()

    for base,derived in translations:
        for m in _generateSingleExpansion(molecule, base, derived):
            # TODO - this could be more efficient
            #   make translations a dict
            if m not in yielded:
                yielded.add(m)
                yield m


def _generateNReductionWorker(molecule: MOLECULE_T, n: int) -> Generator[MOLECULE_T, None, None]:
    """Generate all reductions for a specific length"""
    global RN_TRANSLATIONS
    
    this_translation = RN_TRANSLATIONS[n]

    if not this_translation:
        # empty, no reductions for this length
        return

    if len(molecule) < n:
        return
    elif len(molecule) == n:
        if molecule in this_translation:
            yield tuple(this_translation[molecule])
        return
    # else: we need to check multiple spots for reduction

    lhs = []
    rhs_reversed = list(reversed(molecule))

    dq_pending = deque(maxlen=n)

    while len(dq_pending) < n:
        dq_pending.append(rhs_reversed.pop())
    
    while rhs_reversed:
        try:
            a = this_translation[tuple(dq_pending)]
            t = tuple(itertools.chain(lhs, [a], reversed(rhs_reversed)))
            yield t
        except KeyError:
            pass
        lhs.append(dq_pending.popleft())
        dq_pending.append(rhs_reversed.pop())
    
    # check if the  n-tail can reduce
    _t = tuple(dq_pending)
    if _t in this_translation:
        a = this_translation[_t]
        t = tuple(itertools.chain(lhs, [a]))
        yield t
    return


def generateReductions(molecule: MOLECULE_T) -> Generator[MOLECULE_T, None, None]:
    """Generate all reductions for this molecule""" 
    global RN_TRANSLATIONS
    _s = set()

    # first check for reductions to 'e'
    if molecule in RN_TRANSLATIONS[0]:
        yield tuple(RN_TRANSLATIONS[0][molecule])

    for n in range(1, len(RN_TRANSLATIONS)):
        for k in _generateNReductionWorker(molecule, n):
            if k not in _s:
                _s.add(k)
                yield k


def populateReductions(translations: F_TRANSLATION_T) -> None:
    """Populate the RN_TRANSLATIONS object"""
    global RN_TRANSLATIONS
    
    # find the longest translation so we know how far to go
    max_translation = max(map(lambda x: len(x[1]), translations))

    # create that many empty dicts
    while len(RN_TRANSLATIONS) <= max_translation:
        RN_TRANSLATIONS.append({})
    
    # now populate the dicts
    for a,m in translations:
        if a == 'e':
            assert(m not in RN_TRANSLATIONS[0])
            RN_TRANSLATIONS[0][m] = a
        else:
            assert(m not in RN_TRANSLATIONS[len(m)])
            RN_TRANSLATIONS[len(m)][m] = a


@functools.cache
def getQtyStepsToFullyReduce(molecule: MOLECULE_T) -> int:
    """Get the minimum number of steps to fully reduce this molecule"""
    global UNIQUE_INVOCATIONS

    UNIQUE_INVOCATIONS += 1

    if UNIQUE_INVOCATIONS % 5000 == 0:
        print("UNI:", UNIQUE_INVOCATIONS)

    if molecule == ('e', ):
        return 0

    best_guess = SOME_BIG_NUMBER

    for m in map(getQtyStepsToFullyReduce, generateReductions(molecule)):
        if m == 0:
            return 1
        best_guess = min(best_guess, m+1)
    
    return best_guess


def findConstructively(goal_molecule: MOLECULE_T, translations: F_TRANSLATION_T) -> int:
    """Find the shortest path to `molecule`"""
    # TODO - this is broken

    if goal_molecule == (('e',)):
        return 0

    all_molecules = set()
    last_molecules = set()
    last_molecules.add(('e',))

    for i in itertools.count(start=1):
        if i > len(goal_molecule):
            return SOME_BIG_NUMBER
        print(f"Starting {i} ({len(last_molecules)} this round) ({len(all_molecules)} total)")
        new_molecules = set()
        for new_m in itertools.chain.from_iterable(
            map(lambda x: generateExpansions(x, translations), last_molecules)
        ):
            old_len = len(all_molecules)
            all_molecules.add(new_m)
            if len(all_molecules) > old_len:
                # new item
                new_molecules.add(new_m)
                if new_molecules == goal_molecule:
                    return i
        last_molecules = new_molecules



def y2015d19(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d19.txt"
    print("2015 day 19:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # lineList = [
    #     "e => H",
    #     "e => O",
    #     "H => HO",
    #     "H => OH",
    #     "O => HH",
    #     "",
    #     "OHO",
    # ]

    base_molecule = parseMolecule(lineList[-1].strip())
    lineList.pop()
    lineList.pop()

    translations = []

    for line in lineList:
        base, _, result = line.partition(" => ")
        assert(isAtom(base))
        m = parseMolecule(result)
        translations.append((base, m))

    Part_1_Answer = sum(1 for _ in generateExpansions(base_molecule, translations))

    return (Part_1_Answer, Part_2_Answer)
    populateReductions(translations)

    # tests = [
    #     (('e', ), 0),
    #     (('H', ), 1),
    #     (('O', ), 1),
    #     (('H', 'O'), 2),
    #     (('O', 'H' ), 2),
    #     (('H', 'H'), 2),
    #     (('O', 'O'), SOME_BIG_NUMBER),
    # ]

    tests = [
        (('e', ), 0),
        (('Z', ), SOME_BIG_NUMBER),
        (('H', 'F'), 1),
        (('N', 'Al'), 1),
        (('O', 'Mg'), 1),
        (('H', 'P', 'Mg'), 2),
        (('N', 'Th', 'F'), 2),
        (('N', 'Th', 'Rn', 'F', 'Ar'), 2),
        (('H', 'Si', 'Al'), 2),
    ]

    for t,v in tests:
        print("Testing", t)
        print("  ", list(generateReductions(t)))
        ans = getQtyStepsToFullyReduce(t)
        ans2 = findConstructively(t, translations)
        print("  ", ans, "| ", ans2, " | Expected ", v)
        assert(ans == v)
        assert(ans2 == v)

    print(f"The goal molecule is {len(base_molecule)} long")

    # TODO - neither of these will reasonably terminate
    #   Need to use `anchor points` to reduce the search
    #       that is, the two ends are highly informative
    #   for example, for my molecule to end in `F`
    #       there is exactly four options:
    #           Al => ThF
    #           F => CaF
    #           Mg => BF
    #           e => HF
    #       the list can be partitioned into three parts:
    #           remainder head `F`
    #       where head is a sub string that reduces to one of the above
    #       
    # Part_2_Answer = getQtyStepsToFullyReduce(base_molecule)
    Part_2_Answer = findConstructively(base_molecule, translations)

    return (Part_1_Answer, Part_2_Answer)
