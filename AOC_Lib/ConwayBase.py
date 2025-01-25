from enum import Enum
import itertools
from typing import Any, Callable, Generator, Iterable, TypeVar

from AOC_Lib.NeighborGenerator import neighborGeneratorFactory

# TODO - refactor all conway problems into using this class

ConwayCell_T = TypeVar("ConwayCell_T", bound=Enum)
ConwayGrid_T = list[list[ConwayCell_T]]

ConwayNeighbors_T = Generator[ConwayCell_T, None, None]
ConwayNext_T = Callable[[ConwayCell_T, ConwayNeighbors_T], ConwayCell_T]


class ConwayBase:
    """Base class for Conway's Game of Life type questions"""

    def __init__(
        self,
        initial_grid: ConwayGrid_T,
        advance: ConwayNext_T,
        use_diagonals: bool = False,
    ) -> None:
        self._grid = initial_grid
        self._advance = advance
        self._diagonals = use_diagonals

        self._y_dim = len(initial_grid)
        if initial_grid:
            self._x_dim = len(initial_grid[0])
        else:
            self._x_dim = 0

    @property
    def grid(self) -> ConwayGrid_T:
        """The current status of the grid"""
        return self._grid

    def _oneRound(self) -> None:
        """Do one round"""

        neighbor_generator = neighborGeneratorFactory(
            self._x_dim - 1, self._y_dim - 1, allow_diagonal=self._diagonals
        )
        new_grid = []
        for y, row in enumerate(self._grid):
            new_row = []
            for x, cell in enumerate(row):
                m = map(lambda w: self._grid[w[1]][w[0]], neighbor_generator(x, y))
                new_row.append(self._advance(cell, m))
            new_grid.append(new_row)
        self._grid = new_grid

    def advance(self, n: int = 1) -> ConwayGrid_T:
        """Play `n` rounds and return the resulting grid"""

        for _ in range(n):
            self._oneRound()

        return self.grid

    def cMap(self, func: Callable[[ConwayCell_T], Any] = lambda x: x) -> Iterable[Any]:
        """Apply function to the current grid and yield results
        in row-major order every time (upper left, going across, then down)
        """
        return map(func, itertools.chain.from_iterable(self.grid))

    def render(self) -> None:
        """render to the console based on the enum value"""
        for row in self._grid:
            print("".join(map(lambda x: x.value, row)))
