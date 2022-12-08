
from functools import reduce
from operator import mul
import itertools
from typing import Iterator, Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T
from AOC_Lib.Geometry.Point import DiscretePoint2

# A series of Point2_T
Point2_Gen_T = Iterator[DiscretePoint2]

class Solution_2022_08(SolutionBase):
    """https://adventofcode.com/2022/day/8"""

    def generate_neighbors(self, point: DiscretePoint2) -> tuple[Point2_Gen_T, Point2_Gen_T, Point2_Gen_T, Point2_Gen_T]:
        """Return a tuple of iterators of points each dimension moving away from the given point"""
        point_factory = lambda x,y : DiscretePoint2(x,y)
        return (
            map(point_factory, reversed(range(0,point.x)), itertools.repeat(point.y)),
            map(point_factory, range(point.x+1,self.width), itertools.repeat(point.y)),
            map(point_factory, itertools.repeat(point.x), reversed(range(0, point.y))),
            map(point_factory, itertools.repeat(point.x), range(point.y+1, self.height)),
        )

    def is_visible(self, point: DiscretePoint2) -> bool:
        """Return True iff the tree at `point` is visible"""

        this_height = self.at(point)
        test = lambda p: self.at(p) < this_height
        return any(
            map(
                lambda i: all(map(test, i)), 
                self.generate_neighbors(point)
            )
        )


    def get_scenic_score(self, point: DiscretePoint2) -> int:
        this_height = self.at(point)

        def filter_scenic_direction(p_gen: Point2_Gen_T) -> Point2_Gen_T:
            """While `<=` but break on first `=>`"""
            for p in p_gen:
                test_height = self.at(p)
                yield p
                if test_height >= this_height:
                    return
        per_dim = map(
            lambda x: sum(1 for _ in x), 
            map(
                lambda i: filter_scenic_direction(i), 
                self.generate_neighbors(point)
            )
        )

        return reduce(mul, per_dim)
        
    def gen_all_pos(self) -> Point2_Gen_T:
        """Generate all positions"""
        for x,y in itertools.product(range(self.width), range(self.height)):
            yield DiscretePoint2(x,y)

    def at(self, point: DiscretePoint2) -> str:
        """Get the tree at the point"""
        return self.tree_grid[point.y][point.x]
    
    def __post_init__(self):
        """Runs Once After `__init__`"""
        
        self.tree_grid = list(self.input_str_list(include_empty_lines=False))
        self.width = len(self.tree_grid[0])
        self.height = len(self.tree_grid)

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""
        return sum(1 for _ in filter(lambda p: self.is_visible(p), self.gen_all_pos()))

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""
        return max(map(lambda p: self.get_scenic_score(p), self.gen_all_pos()))