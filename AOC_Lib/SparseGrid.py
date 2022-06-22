

from collections import Counter
from typing import Any, Callable, Iterator, Optional, TypeVar

SparseGridPos_T = tuple[int, int]
SparseGridCell_T = TypeVar("SparseGridCell_T")


class EmptyGridException(Exception):
    """Raised when the grid is empty"""


# TODO - this model can be applied to may solutions
class SparseGrid:
    

    def __init__(self, default: SparseGridCell_T) -> None:
        # the default value
        self._default = default

        self._non_defaults: dict[SparseGridPos_T, SparseGridCell_T] = {}

        # counter of how many non-default cells in each X column
        self._x_value_refs = Counter()

        # counter of how many non-default cells in each Y column
        self._y_value_refs = Counter()

    @property
    def default(self) -> SparseGridCell_T:
        """Return the default object"""
        return self._default

    @property
    def x_keys(self) -> Iterator[int]:
        """Return an iterator of unique x values
            representing each column with a non-default value
        """
        return iter(self._x_value_refs.keys())
    
    @property
    def y_keys(self) -> Iterator[int]:
        """Return an iterator of unique y values
            representing each row with a non-default value
        """
        return iter(self._y_value_refs.keys())

    @property
    def number_non_default(self) -> bool:
        """Return the number of cells that are not default"""
        return len(self._non_defaults)

    @property
    def is_all_default(self) -> bool:
        """Return `True` iff all cells are default"""
        return self.number_non_default == 0
    
    @property 
    def min_x(self) -> Optional[int]:
        """Return the smallest x value for a Non-default cell
            otherwise, None
        """
        if self.is_all_default:
            return None
        return min(self.x_keys)
    
    @property 
    def max_x(self) -> Optional[int]:
        """Return the largest x value for a Non-default cell
            otherwise, None
        """
        if self.is_all_default:
            return None
        return max(self.x_keys)
    
    @property 
    def min_y(self) -> Optional[int]:
        """Return the smallest y value for a Non-default cell
            otherwise, None
        """
        if self.is_all_default:
            return None
        return min(self.y_keys)
    
    @property 
    def max_y(self) -> Optional[int]:
        """Return the largest y value for a Non-default cell
            otherwise, None
        """
        if self.is_all_default:
            return None
        return max(self.y_keys)

    def __getitem__(self, pos: SparseGridPos_T) -> SparseGridCell_T:
        """Return the item at the position"""
        if pos in self._non_defaults:
            return self._non_defaults[pos]
        else:
            return self.default
        
    def __setitem__(self, pos: SparseGridPos_T, val: SparseGridCell_T) -> None:
        """Set the item at pos `pos` to `val`"""
        if val == self.default:
            self.resetCell(pos)
        else:
            if pos not in self._non_defaults:
                self._x_value_refs.update([pos[0]])
                self._y_value_refs.update([pos[1]])
            self._non_defaults[pos] = val

    def resetCell(self, pos: SparseGridPos_T):
        """roughly SparseGrid[pos] = SparseGrid.default"""
        if pos in self._non_defaults:
            self._x_value_refs.subtract([pos[0]])
            if self._x_value_refs[pos[0]] == 0:
                self._x_value_refs.pop(pos[0])
            self._y_value_refs.subtract([pos[1]])
            if self._y_value_refs[pos[1]] == 0:
                self._y_value_refs.pop(pos[1])
            self._non_defaults.pop(pos)

    def generateAllPositions(self, overscan: int = 0) -> Iterator[SparseGridPos_T]:
        """Generate all positions in the grid which are
            inside (boundary-inclusive) the points (min_x, min_y) (max_x, max_y)

            parameter `overscan` specifies an augmentation to these bounds
                with positive values increasing the distance
            
            Iterator produces positions ordered in increasing y with ties broken by increasing x
        """
        if self.is_all_default:
            raise EmptyGridException

        x_range = range(self.min_x - overscan, self.max_x + 1 + overscan)
        y_range = range(self.min_y - overscan, self.max_y + 1 + overscan)

        # NOTE - this is not the same as itertools.product
        def _g():
            for y in y_range:
                for x in x_range:
                    yield (x,y)
        return (iter(_g()))

    def generateAllCells(self, overscan: int = 0) -> Iterator[SparseGridPos_T]:
        """Like `generateAllPositions` but for values"""
        return map(lambda p: self[p], self.generateAllPositions(overscan=overscan))

    def mapOnPositions(self, callable: Callable[[SparseGridPos_T], Any], overscan: int = 0) -> Any:
        """Like `generateAllPositions` but as a mapping"""
        return map(callable, self.generateAllPositions(overscan=overscan))
    
    def mapOnCells(self, callable: Callable[[SparseGridCell_T], Any], overscan: int = 0) -> Any:
        """Like `generateAllCells` but as a mapping"""
        return map(callable, self.generateAllCells(overscan=overscan))

    def printGrid(
        self, 
        overscan: int = 0, 
        formatter: Callable[[SparseGridCell_T], str] = str,
        line_break: str = '\n',
    ) -> None:
        """Print the grid to the console in lines of increasing y
            cells are formatted with `formatter` and 
            `line_break` is inserted between lines
        """
        if self.is_all_default:
            return

        last_y = None

        for pos in self.generateAllPositions(overscan=overscan):
            if last_y is None or pos[1] > last_y:
                print(line_break, end="")
                last_y = pos[1]
            print(formatter(self[pos]), end="")
        print(line_break, end="")


    