from typing import Optional

from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.SlidingWindow import sliding_window


class NiceString(str):
    """A nice string"""

    vowels: str = "aeiou"
    illegal_substrings: list[str] = ["ab", "cd", "pq", "xy"]

    @classmethod
    def is_nice(cls, s: str) -> bool:
        """Return `True` iff this is a nice string"""

        vowel_count = sum(1 for c in s if c in cls.vowels)
        if vowel_count < 3:
            return False

        if not any(map(lambda x: x[0] == x[1], sliding_window(s, 2))):
            return False

        if any(map(lambda x: x in s, cls.illegal_substrings)):
            return False

        return True


class NicerString(str):
    """A nicer string"""

    @classmethod
    def is_nice(cls, s: str) -> bool:
        """Return `True` iff this is a nice string"""

        # Check for 'aba' structure
        if not any(map(lambda i: s[i] == s[i + 2], range(len(s) - 2))):
            return False

        # find the double not overlapping

        seen: set[tuple[str, str]] = set()

        last_seen = (" ", " ")

        # These are either "aaa" or "aaaa"
        possible_double_doubles: list[tuple[tuple[str, str], int]] = []

        for i, t in enumerate(sliding_window(s, 2)):
            if t in seen and t != last_seen:
                return True
            elif t not in seen:
                last_seen = t
                seen.add(t)
                continue

            assert t in seen
            assert t[0] == t[1]

            possible_double_doubles.append((t, i))

        for t, i in possible_double_doubles:
            f = s.find("".join(t))
            if i - f >= 2:
                return True
        return False


class Solution_2015_05(SolutionBase):
    """https://adventofcode.com/2015/day/5"""

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return sum(1 for s in self.input_str_list() if NiceString.is_nice(s))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        return sum(1 for s in self.input_str_list() if NicerString.is_nice(s))
