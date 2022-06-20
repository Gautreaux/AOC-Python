# from AOC_Lib.name import *

from AOC_Lib.SlidingWindow import sliding_window

from collections import defaultdict, deque, namedtuple, Counter
from enum import Enum, unique
import functools
import itertools
from typing import Any, Callable, Generator, Iterable, Optional

SOME_BIG_NUMBER = 2**24

ATOM_T = str

MOLECULE_T = tuple[ATOM_T, ...]

# a forward translation from str to str
F_TRANSLATION_T = tuple[ATOM_T, MOLECULE_T]

R_TRANSLATION: dict[MOLECULE_T, ATOM_T] = {}
RN_TRANSLATIONS: list[dict[MOLECULE_T, ATOM_T]] = []

UNIQUE_INVOCATIONS: int = 0 

TAIL_FOLD_CANDIDATE_T = namedtuple('TAIL_FOLD_CANDIDATE_T', "result molecule_tail match_tail num_folds")

@unique
class ReduceType(Enum):
    FULL_REDUCTION = 0
    HEAD_MATCH = 1 # reduce where the reduction's head matches input
    TAIL_MATCH = 2 # reduce where the reduction's tail matches input


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
    """Populate the R_TRANSLATIONS and RN_TRANSLATIONS object"""
    global R_TRANSLATION

    for a, m in translations:
        assert(m not in R_TRANSLATION)
        R_TRANSLATION[m] = a

    # FOR RN_Translations
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



def generateTailFoldCandidates(molecule: MOLECULE_T, num_folds:int) -> Generator[int, None, None]:
    """Generate the Tail Fold candidates,
        that is 
        TODO - elaborate
    """
    global R_TRANSLATION

    for m,a in R_TRANSLATION.items():
        if m[0] == molecule[0]:
            yield TAIL_FOLD_CANDIDATE_T(
                result=a,
                molecule_tail=molecule[1:],
                match_tail=m[1:],
                num_folds=num_folds+1
            )



def calculateKeyPoints(translations: F_TRANSLATION_T) -> list[MOLECULE_T]:
    """Determine any sequences that uniquely identify one molecule"""
    to_return = []

    molecules_only = list(map(lambda x: x[1], translations))
    
    # all the tokens
    token_set = set(itertools.chain.from_iterable(molecules_only))

    print("Token set is:", token_set)

    # check if any token is unique to one molecule
    for t in token_set:
        s = sum(map(lambda x: 1 if t in x else 0, molecules_only))
        if s == 0:
            raise RuntimeError("BIG BAD")
        elif s == 1:
            to_return.append(t)

    # Find tokens that only appear in the middle of molecules
    start_tokens = set(map(lambda x: x[0], molecules_only))
    end_tokens = set(map(lambda x: x[-1], molecules_only))
    middle_only_tokens = (token_set - start_tokens) - end_tokens

    print("Middle only tokens:", middle_only_tokens)

    # now find all pairs that includes middle only tokens
    _all_interior_pairs = map(lambda z: sliding_window(z,2), molecules_only)

    middle_only_pairs = list(filter(
        lambda x: any(map(lambda y: y in middle_only_tokens, x)),
        itertools.chain.from_iterable(_all_interior_pairs),
    ))

    print("Middle only pairs:", middle_only_pairs)

    # now find the ones that appear exactly once in all interior pairs
    _s = Counter(middle_only_pairs)
    unique_pairs = list(filter(lambda x: _s[x] == 1,_s.keys()))
    print("Unique pairs are:", unique_pairs)

    to_return.extend(unique_pairs)

    return to_return

# Thoughts:
# TiRn is a key point
# TiRnSiRnFYFArCaSiRnBFArCaSiRnTiMgArSiThCaSiThCaFArPRnFArSiRnFArTiTiTiTiBCaCaSiRnCaCaFYFArSiThCaPTiBPTiBCaSiThSiRnMgArCaF
#   must fold into B (via B => TiRnFAr)
# so
# SiRnFYFArCaSiRnBFArCaSiRnTiMgArSiThCaSiThCaFArPRnFArSiRnFArTiTiTiTiBCaCaSiRnCaCaFYFArSiThCaPTiBPTiBCaSiThSiRnMgArCaF
#   must fold into FAr
#   and by extension:
#       FAr => CaFAr => ...
#       FAr => PMgAr => ...
#       FAr => SiAl => 
#          implies Al => RnFyFAr..........
#   but note PRn is another key point: FArSiRnFArTiTiTiTiBCaCaSiRnCaCaFYFArSiThCaPTiBPTiBCaSiThSiRnMgArCaF
#     must fold into Ca (via Ca ==> PRnFAr) 
#       either this reduces directly to Ca and passed remainder up
#       or the entire FArSiRnFAr... folds into FA
# and anything to the left must fold completely independently


def generateRFoldCandidate(head: MOLECULE_T, source: MOLECULE_T) -> Generator[MOLECULE_T, None, None]:
    """Generate Right Fold candidates of `source`
        where `head` is the start
        Generator yields the remainder for a valid folding
    """

    # if head[0] == source[0]:


def partitionMolecule(
    molecule: MOLECULE_T, 
    break_on: MOLECULE_T
) -> tuple[MOLECULE_T, Optional[MOLECULE_T]]:
    """Break a molecule in half based on another one
        returns a Tuple of the two halves
        or the original molecule and an empty tuple if no match was found
    """

    for i,w in enumerate(sliding_window(molecule, len(break_on))):
        if w == break_on:
            print("DING")
            return ((molecule[:i], molecule[i+len(break_on):]))
    return (molecule, None)

# TODO - refactor into a class or something
def partitionOnKeyPoints(
    molecule: MOLECULE_T,
    translations: F_TRANSLATION_T, 
    key_points: list[MOLECULE_T],
    target: MOLECULE_T
) -> None:
    """Partition the molecule based on key point"""

    # find any unique partition
    rhs = None
    for splitter in key_points:
        lhs,rhs = partitionMolecule(molecule, splitter)
        if rhs is not None:
            assert(len(molecule) == (len(lhs) + len(splitter) + len(rhs)))
            break
    if rhs is None:
        print(f" No Partition found")
        return
    print(lhs,"|",splitter,"|",rhs)
    
    # find what translation owns `splitter`
    _l = list(filter(
        lambda x: splitter in sliding_window(x[1], len(splitter)),
        translations,
    ))
    assert(len(_l) == 1)
    
    reduced, must_match = _l[0]

    must_match_lhs, must_match_rhs = partitionMolecule(must_match, splitter)

    print(must_match_lhs, must_match_rhs)
 


def getNumReduceSteps(
    molecule: MOLECULE_T,
    target: MOLECULE_T,
    translations: F_TRANSLATION_T, 
    key_points: list[MOLECULE_T],
    reduce_type: ReduceType,
) -> int:
    """Return the number of steps to `molecule` into `target`"""


class ReductionManager:

    def __init__(self, translations: list[F_TRANSLATION_T]) -> None:
        # all atoms
        self.all_atoms: set[ATOM_T] = set(itertools.chain.from_iterable(map(
            lambda x: itertools.chain([x[0]], x[1]),
            translations,
        )))

        # the forward translations
        self.f_translations: dict[ATOM_T, MOLECULE_T] = dict(translations)

        # the reverse translations
        self.r_translations: dict[MOLECULE_T, ATOM_T] = dict(map(lambda x: (x[1], x[0]), translations))

        # translations organized by how the output molecule ends
        _d = defaultdict(list)
        for t in translations:
            _d[t[1][-1]].append(t)
        self.output_ends_with: dict[ATOM_T, list[F_TRANSLATION_T]] = dict(_d.items())

        # translations organized by how the output molecule begins
        _d = defaultdict(list)
        for t in translations:
            _d[t[1][0]].append(t)
        self.output_starts_with: dict[ATOM_T, list[F_TRANSLATION_T]] = dict(_d.items())

        # force computation early
        list(self.mapOntoAtoms(lambda x: self.reachable_reduction_ends(x)))
        list(self.mapOntoAtoms(lambda x: self.reachable_reduction_starts(x)))

    def _common_CRRS(self, atom:ATOM_T, is_starts: bool = True) -> set[ATOM_T]:
        """Common logic for _computeReachableReduction..."""
        if is_starts:
            translations_dict = self.output_starts_with
        else:
            translations_dict = self.output_ends_with

        _s = set()
        _q = deque()
        _q.append(atom)
        while _q:
            t = _q.popleft()

            if t in self.output_starts_with:
                n = map(lambda x: x[0], self.output_starts_with[t])
                f = filter(lambda x: x not in _s, n)
                a,b = itertools.tee(f)
                _s.update(a)
                _q.extend(b)
        return _s

    @functools.cache
    def reachable_reduction_starts(self, atom: ATOM_T) -> set[ATOM_T]:
        """Return the reduction starts set for the provided atom
            That is the set of all starts any reduction (or series of reduction)
                could produce
        """
        return self._common_CRRS(atom, True)

    @functools.cache
    def reachable_reduction_ends(self, atom: ATOM_T) -> set[ATOM_T]:
        """Return the reduction ends set for the provided atom
            That is the set of all ends any reduction (or series of reduction)
                could produce
        """
        return self._common_CRRS(atom, False)

    # TODO - proper type var
    def mapOntoAtoms(self, c: Callable[[ATOM_T], Any]) -> Iterable[Any]:
        """Apply the callable to each atom"""
        return map(c, self.all_atoms)

    def getPossibleLeftRemainders(
        self, molecule: MOLECULE_T, target: MOLECULE_T
    ) -> Generator[MOLECULE_T, None, None]:
        """Yield where each is the left remainder of folding molecule into target"""

        print(f"    Attempting to fold <molecule:{len(molecule)}> into {target}")
        if target not in self.r_translations:
            print(f"      No translation exists to produce {target}")
            return
        
        if molecule == target:
            yield tuple()

    def reduce(self, molecule: MOLECULE_T, target=('e', )) -> int:
        """Reduce molecule and return number steps"""

        if molecule == target:
            return 0

        # DEBUG
        molecule = tuple(itertools.chain(molecule[:-2], [molecule[-1]]))

        print(f"Molecule ends with: {molecule[-1]} : {self.output_ends_with[molecule[-1]]}")

        for a,m in self.output_ends_with[molecule[-1]]:
            print(f"  TRY: {(a,m)}")
            if (a, ) == target:
                # special conditions?
                pass
            elif a not in self.output_ends_with:
                # Any fold will fail
                #   so dont even bother
                print(f"SKIP {(a,m)} : No molecule ends in {a}")
                continue
            head = m[:-1]
            print(f"    Head: {head}")

            for f in self.getPossibleLeftRemainders(molecule[:-1], head):
                print(f"Found a possible solution folding {m} -> {a}")

            # a must right fold into `head`
            #   

    def _isReductionPossibleCommon(self, molecule: MOLECULE_T, target: MOLECULE_T) -> Optional[bool]:
        """Common logic for `_isReductionPossible`
            returns an answer or `None` if undecided
        """
        if molecule == target:
            return True
        
        if molecule == target:
            return True

        # first check if the left end is possible
        if target[0] not in self.reachable_reduction_starts(molecule[0]):
            # There is no way to convert the starting atom in `molecule`
            #   to the starting atom in `target`
            #   regardless of any other formatting
            return False

        # then the right end
        if target[-1] not in self.reachable_reduction_ends(molecule[0]):
            return False

        if molecule[0] not in self.output_starts_with:
            # There is no translation that produces an output with
            #   this starting atom
            #   so there is no way this works
            # Presumably, his should be caught in the earlier conditions
            return False

        if molecule[-1] not in self.output_ends_with:
            # See above
            return False
        
        return None


    def isPartialReductionPossible(self, molecule: MOLECULE_T, target: MOLECULE_T) -> bool:
        """Return `True` iff a reduction is possible,
            but note there may be a remainder
        """
        _b = self._isReductionPossibleCommon(molecule, target)
        if _b is not None:
            return _b

    # TODO - cache?
    def isCompleteReductionPossible(self, molecule: MOLECULE_T, target: MOLECULE_T) -> bool:
        """Return `True` iff there is at least one reduction of `molecule` into `target`
            with no remaining extraneous characters
        """
        _b = self._isReductionPossibleCommon(molecule, target)
        if _b is not None:
            return _b

        possible_reductions = self.output_starts_with[molecule[0]]

        # for reduced_atom, needed_molecule in possible_reductions:
        #     for i in range(len(need
            

        print(possible_reductions)



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

    populateReductions(translations)
    key_points = calculateKeyPoints(translations)

    print("Key Points:", key_points)

    # partitionOnKeyPoints(base_molecule, translations, key_points)

    # for t in generateTailFoldCandidates(base_molecule):
    #     print(t)

    rm = ReductionManager(translations)
    # rm.reduce(base_molecule)

    # print(rm.getCandidateLeftRedux(base_molecule))

    for k in rm.mapOntoAtoms(lambda x: (x, rm.reachable_reduction_starts(x))):
        print(k[0], "=>", k[1])

    print(rm.isCompleteReductionPossible(base_molecule, ('e', )))

    return (Part_1_Answer, Part_2_Answer)

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
