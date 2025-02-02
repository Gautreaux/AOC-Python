from dataclasses import dataclass


from AOC_Lib.SolutionBase import SolutionBase
from AOC_Lib.Grid2d import Grid2d, Point2
from AOC_Lib.pqueue import PQueue


@dataclass(frozen=True)
class SearchState:
    """A state while searching for a path through the memory grid"""
    position: Point2
    depth: int


class Solution_2024_18(SolutionBase):
    """https://adventofcode.com/2024/day/18"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        self.corruption_list: list[tuple[int, int]] = []

        for line in self.input_str_list(include_empty_lines=False):
            t = line.split(",")
            assert len(t) == 2
            self.corruption_list.append((int(t[0]), int(t[1])))

        memory_grid = Grid2d([["."] * 71 for _ in range(71)])
        assert memory_grid.dimensions == (71, 71)
        assert memory_grid.at((70, 70)) == "."

        # First kilobyte of corruption
        for corruption_location in self.corruption_list[:1024]:
            memory_grid.rows[corruption_location[1]][corruption_location[0]] = "#"

        path = self.get_shortest_path(memory_grid)
        # -1 to account for both start and stop being in the path
        self._part_1_answer = len(path) - 1

        best_path: set[Point2] = set(path)

        for corruption_location in self.corruption_list[1024:]:
            memory_grid.rows[corruption_location[1]][corruption_location[0]] = "#"
            if Point2(*corruption_location) not in best_path:
                continue

            try:
                best_path = set(self.get_shortest_path(memory_grid))
            except RuntimeError:
                self._part_2_answer = "".join(
                    c for c in str(corruption_location) if c in "0123456789,"
                )
                return

        raise RuntimeError("There is still a path after applying all the corrution.")

    def get_shortest_path(
        self, grid: Grid2d, start: Point2 = Point2(0, 0), end: Point2 = Point2(70, 70)
    ) -> list[Point2]:
        """Return the shortest path from start to end"""
        parent_map: dict[Point2, Point2 | None] = {}
        frontier: PQueue[SearchState] = PQueue()

        frontier.push(SearchState(start, 0), 0)
        parent_map[start] = None

        while frontier:
            current_pos = frontier.popMin()
            # print(f'Fontier size {len(frontier)}; {current_pos.position}')

            if current_pos.position == end:
                break

            for next_pos, _ in grid.generate_neighbor_points(
                current_pos.position, value_filter=lambda x: x == "."
            ):
                if next_pos not in parent_map:
                    parent_map[next_pos] = current_pos.position
                    frontier.push(
                        SearchState(next_pos, current_pos.depth + 1),
                        current_pos.depth + 1,
                    )

        if end not in parent_map:
            raise RuntimeError("No Path Possible")

        current_pos = end
        r_path = []
        while current_pos is not None:
            r_path.append(current_pos)
            current_pos = parent_map[current_pos]

        return list(reversed(r_path))
