# from AOC_Lib.name import *
from typing import Iterator
from itertools import chain

class LinenLayout:
    def __init__(self, options: Iterator[str]):
        self.components: set[str] = set(options)
        self.solutions: dict[str, tuple[str, ...]] = {k:(k,) for k in self.components}
        self.pending: set[str] = set()
        # assert all(len(c) >= 2 for c in self.components)
        self._prefix_lut: dict[str, list[str]] = self._build_prefix_lut()
        self._postfix_lut: dict[str, list[str]] = self._build_postfix_lut()

    def _build_prefix_lut(self) -> dict[str, list[str]]:
        lut: dict[str, list[str]] = {}
        for component in self.components:
            c2 = component[:2]
            if c2 in lut:
                lut[c2].append(component)
            else:
                lut[c2] = [component]
        return lut

    def _build_postfix_lut(self) -> dict[str, list[str]]:
        lut: dict[str, list[str]] = {}
        for component in self.components:
            c2 = component[-2:]
            if c2 in lut:
                lut[c2].append(component)
            else:
                lut[c2] = [component]
        return lut

    def get_solution(self, pattern: str) -> tuple[str, ...] | None:
        """Get the solution for the given pattern, or None if no solution possible"""
        cached_solution = self.solutions.get(pattern)
        if cached_solution:
            return cached_solution
        assert pattern not in self.pending, f"Found cycle? : {pattern}"
        self.pending.add(pattern)
        sol = self._get_solution(pattern)
        self.pending.remove(pattern)
        self.solutions[pattern] = sol
        return sol

    def _get_solution(self, pattern: str) -> tuple[str, ...] | None:
        """Build the solution, or None if no solution possible"""

        for opt in self._prefix_lut.get(pattern[:2], []):
            if opt == pattern:
                return (opt, )
            if not pattern.startswith(opt):
                continue
            rhs_remainder = pattern[len(opt):]
            if not rhs_remainder:
                continue
            rhs_sol = self.get_solution(rhs_remainder)
            if rhs_sol:
                return tuple(chain([opt], rhs_sol))

        for opt in self._postfix_lut.get(pattern[-2:], []):
            if opt == pattern:
                return (opt, )
            if not pattern.endswith(opt):
                continue
            lhs_remainder = pattern[:len(opt)]
            if not lhs_remainder:
                continue
            lhs_sol = self.get_solution(lhs_remainder)
            if lhs_sol:
                return tuple(chain(lhs_sol, [opt]))

        return None

def _assert_sample_passes():
    sample_compoenents = 'r, wr, b, g, bwu, rb, gb, br'.replace(',', '').split()
    linen = LinenLayout(sample_compoenents)

    sol = linen.get_solution('brwrr')
    assert sol is not None
    assert ''.join(sol) == 'brwrr'

    assert linen.get_solution('bggr') # is not none
    assert linen.get_solution('gbbr') # is not none
    assert linen.get_solution('ubwu') is None
    assert linen.get_solution('bwurrg') # is not none
    assert linen.get_solution('brgr') # is not none
    assert linen.get_solution('bbrgwb') is None

def y2024d19(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2024/d19.txt"
    print("2024 day 19:")

    # _assert_sample_passes()

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    options = lineList[0].replace(',', '').split()
    
    layout = LinenLayout(options)

    Part_1_Answer = 0
    for i,p in enumerate(lineList[2:]):
        print('i =', i)
        sol = layout.get_solution(p)
        if sol:
            Part_1_Answer += 1

    assert Part_1_Answer < 231

    return (Part_1_Answer, Part_2_Answer)