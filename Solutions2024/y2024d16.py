from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator, Optional


from AOC_Lib.Geometry.PointTransforms import Direction2
from AOC_Lib.Grid2d import Grid2d, Point2
from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.pqueue import PQueue


@dataclass
class _SearchState:
    position: Point2
    score: int
    direction: Direction2

    def __hash__(self) -> int:
        return hash((self.position.x, self.position.y, self.direction.value))


class Solution_2024_16(SolutionBase):
    """https://adventofcode.com/2024/day/16"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.map: Grid2d = Grid2d([list(c) for c in self.input_str_list()])

        start = list(self.map.generate_matching_points("S"))
        end = list(self.map.generate_matching_points("E"))

        if len(start) != 1:
            raise RuntimeError("Multiple starts found")
        if len(end) != 1:
            raise RuntimeError("Multiple ends found")

        self.start = start[0][0]
        self.end = end[0][0]

        self.map.rows[self.start.y][self.start.x] = "."
        self.map.rows[self.end.y][self.end.x] = "."

    def generate_successor_states(self, state: _SearchState) -> Iterator[_SearchState]:
        """Generate all the succesor state of the given state"""

        tx = state.direction.get_transform

        # TODO - merge the Point2 with DiscretePoint2
        next_pos = state.position + Point2(tx.x, tx.y)

        if self.map.at(next_pos) == ".":
            yield _SearchState(next_pos, state.score + 1, state.direction)

        # The Turn States
        yield _SearchState(
            state.position, state.score + 1000, state.direction.turn_right()
        )
        yield _SearchState(
            state.position, state.score + 1000, state.direction.turn_left()
        )

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Relatively Simple BFS implementation"""
        start_state = _SearchState(self.start, 0, Direction2.RIGHT)
        frontier: PQueue[_SearchState] = PQueue()
        frontier.push(start_state, start_state.score)
        seen_pos: set = set()

        while frontier:

            now = frontier.popMin()
            if now.position == self.end:
                return now.score

            # Already seen this position
            if hash(now) in seen_pos:
                continue
            seen_pos.add(hash(now))

            for s in self.generate_successor_states(now):
                frontier.push(s, s.score)

        raise RuntimeError("No solution found. Is the end reachable?")

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        score_to_beat: int = self.part_1_answer  # type: ignore
        if not isinstance(score_to_beat, int):
            raise TypeError(
                f"Expected part_1_answer to be {type(0)} but got {type(score_to_beat)}"
            )

        frontier: PQueue[_SearchState] = PQueue()
        priors: defaultdict[_SearchState, list[_SearchState]] = defaultdict(list)
        seen_pos: set = set()

        start_state = _SearchState(self.start, 0, Direction2.RIGHT)
        frontier.push(start_state, 0)

        while frontier:
            now = frontier.popMin()

            if now.score > score_to_beat:
                continue
            if now.position == self.end:
                continue

            # Already seen this position
            if hash(now) in seen_pos:
                continue
            seen_pos.add(hash(now))

            for s in self.generate_successor_states(now):
                priors[s].append(now)
                frontier.push(s, s.score)

        to_check: list[_SearchState] = []
        for state in priors.keys():
            if state.position == self.end:
                to_check.append(state)

        unique_to_check: set[Point2] = set()

        while to_check:
            now = to_check.pop()
            unique_to_check.add(now.position)
            for s in priors[now]:
                to_check.append(s)

        return len(unique_to_check)
