# from AOC_Lib.name import *
from collections import Counter
from typing import Iterator
from itertools import product


_SAMPLE = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


class WordSearch:
    def __init__(self, rows: list[str]):
        self.rows: list[str] = rows

        # Assert all rows are the same length
        assert len({len(r) for r in rows}) == 1
        assert rows  # is not empty
        assert rows[0]  # is not empty

    @staticmethod
    def _assert_no_repeated_characters(search_term: str):
        """Assert no repeated characters in the search term"""
        c = Counter(search_term)
        assert all(v for v in c.values() if v == 1)

    def at(self, point: tuple[int, int]) -> str:
        """Get the character at the point"""
        if point[0] < 0:
            raise IndexError()
        if point[1] < 0:
            raise IndexError()
        return self.rows[point[1]][point[0]]

    def locate_character(self, character: str) -> Iterator[tuple[int, int]]:
        """Locate the occurances of a given character"""
        assert len(character) == 1

        for y, row in enumerate(self.rows):
            for x, c in enumerate(row):
                if c == character:
                    yield (x, y)

    def term_occurs_at_with_transformer(
        self, search_term: str, start: tuple[int, int], transformer: tuple[int, int]
    ) -> bool:
        """Return true iff the search term occurs at start with given transformer (direction)"""
        if not search_term:
            raise RuntimeError("Cannot search with an empty search term")

        for i, c in enumerate(search_term):
            pos = (
                start[0] + i * transformer[0],
                start[1] + i * transformer[1],
            )
            try:
                if c != self.at(pos):
                    return False
            except IndexError:
                return False

        return True

    def get_occurances_starting_at(
        self, search_term: str, start: tuple[int, int]
    ) -> tuple[tuple[int, int], ...]:
        """Get the transforms where the occurances are for the starting point and term"""

        if not search_term:
            return 0

        if self.at(start) != search_term[0]:
            return 0

        transformers = tuple(
            p for p in product((-1, 0, 1), (-1, 0, 1)) if not all(t == 0 for t in p)
        )
        assert len(transformers) == 8, list(transformers)
        assert all(len(t) == 2 for t in transformers)
        assert len(set(transformers)) == len(transformers)  # Assert no repeats

        results = tuple(
            [
                t
                for t in transformers
                if self.term_occurs_at_with_transformer(search_term, start, t)
            ]
        )
        return results

    def get_occurances(
        self, search_term: str
    ) -> dict[tuple[int, int], tuple[tuple[int, int]]]:
        """Get the locations and transforms the search term appears"""

        # Don't think this is necessary anymore
        self._assert_no_repeated_characters(search_term)

        to_return = {}

        for start in self.locate_character(search_term[0]):
            to_return[start] = self.get_occurances_starting_at(search_term, start)

        return to_return

    def count_occurances(self, search_term: str) -> int:
        """Count the number of times the search term appears"""

        occurances = self.get_occurances(search_term)
        return sum(len(v) for v in occurances.values())


def _assert_sample_passes():
    lines: list[str] = _SAMPLE.splitlines()  # type: ignore
    
    assert isinstance(lines, list)
    assert isinstance(lines[0], str)

    ws_sample = WordSearch(lines)
    search_term = "XMAS"

    expected_answers_start_and_transform = {
        (4, 0): [(1, 1)],
        (5, 0): [(1, 0)],
        (4, 1): [(-1, 0)],
        (9, 3): [(0, 1), (-1, 1)],
        (0, 4): [(1, 0)],
        (6, 4): [(-1, 0), (0, -1)],
        (0, 5): [(1, -1)],
        (6, 5): [(-1, -1)],
        (1, 9): [(1, -1)],
        (3, 9): [(1, -1), (-1, -1)],
        (5, 9): [(1, -1), (-1, -1), (1, 0)],
        (9, 9): [(-1, -1), (0, -1)],
    }

    for start, trans in expected_answers_start_and_transform.items():
        for t in trans:
            msg = f"FAILED with: Start {start}, Transform {t}"
            assert ws_sample.term_occurs_at_with_transformer(search_term, start, t), msg
        l = ws_sample.get_occurances_starting_at(search_term, start)
        assert set(l) == set(
            trans
        ), f"FAILED with: Start {start}, {len(trans)} expected but found {len(l)} {l}"

    assert sum(len(l) for l in expected_answers_start_and_transform.values()) == 18
    assert ws_sample.count_occurances("XMAS") == 18, str(
        ws_sample.count_occurances("XMAS")
    )


def y2024d4(inputPath=None):
    if inputPath == None:
        inputPath = "Input2024/d4.txt"
    print("2024 day 4:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    _assert_sample_passes()

    ws = WordSearch(lineList)
    Part_1_Answer = ws.count_occurances("XMAS")

    locations = ws.get_occurances("MAS")

    # transform to the locations of the A characters
    a_locations = set()
    a_locations_with_pairs = set()

    for start, transforms in locations.items():
        for t in transforms:
            # Has to be an X
            #   so only the diagonal transforms
            if t[0] == 0 or t[1] == 0:
                continue

            a_loc = (start[0] + t[0], start[1] + t[1])
            if a_loc in a_locations:
                # Should always pass
                assert a_loc not in a_locations_with_pairs
                a_locations_with_pairs.add(a_loc)
            a_locations.add(a_loc)

    Part_2_Answer = len(a_locations_with_pairs)

    return (Part_1_Answer, Part_2_Answer)
