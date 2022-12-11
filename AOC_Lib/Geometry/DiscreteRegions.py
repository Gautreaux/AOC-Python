
from dataclasses import dataclass
from functools import reduce
import itertools
from operator import mul
from typing import Any, Iterable, Union

from .Point import DerivedDiscretePoint_T, DiscreteAbstractPoint


DimensionBounds_T = tuple[int, ...]


def _minmax(bound: tuple[int,int], test:int) -> tuple[int, int]:
    return (min(bound[0], test), max(bound[1], test))


def _minmax_dims(
    bound: tuple[DimensionBounds_T, ...],
    test: Iterable[int],
) -> tuple[DimensionBounds_T, ...]:

    return tuple(map(lambda b,t: _minmax(b,t), bound, test))


@dataclass(frozen=True)
class DiscreteAABBbounds:
    """A Axis Aligned Bounding Box"""

    lower: DiscreteAbstractPoint
    upper: DiscreteAbstractPoint

    @classmethod
    def from_point_set(cls, p: Iterable[DerivedDiscretePoint_T]) -> 'DiscreteAABBbounds':
        """Build a AA Bounds from a point set"""
        itr = iter(p)
        try:
            p1 = next(itr)
        except StopIteration:
            raise RuntimeError('Must provide at least point to find bounds') from None
        
        start_bounds = tuple(map(lambda x: (x,x), p1))

        bounds = reduce(_minmax_dims, itr, start_bounds)

        return cls(
            lower=p1.__class__(*map(lambda x: x[0], bounds)),  # type: ignore
            upper=p1.__class__(*map(lambda x: x[1], bounds)),  # type: ignore
        )

    def generate_bounded_points(self) -> Iterable[DiscreteAbstractPoint]:
        """Generate all the Discrete points bounded by this AA BB"""
        ranges = map(lambda a,b: range(a, b+1), self.lower, self.upper)

        for p in itertools.product(*ranges):
            yield self.lower.__class__(*p)  # type: ignore 

    def __iter__(self):
        return self.generate_bounded_points()

    def generate_corners(self) -> Iterable[DiscreteAbstractPoint]:
        """Generate the corners of this bounding box"""
        
        b = zip(self.lower, self.upper)
        for c in itertools.product(*b):
            yield self.lower.__class__(*c)  # type: ignore

    def contains(self, point: DiscreteAbstractPoint) -> bool:
        """Return `True` iff this bounds contains the point"""
        assert(self.lower.__class__ == point.__class__)

        for smin, smax, test in zip(self.lower, self.upper, point):
            if test < smin:
                return False
            elif test > smax:
                return False
        return True

    def intersects(self, other: 'DiscreteAABBbounds') -> bool:
        """Return `True` iff these bounding boxes intersect"""
        assert(self.lower.__class__ == other.lower.__class__)

        if self.lower == self.upper:
            return other.contains(self.lower)
        elif other.lower == other.upper:
            return self.contains(other.upper)
        
        for corner_point in self.generate_corners():
            if other.contains(corner_point):
                return True
        for corner_point in other.generate_corners():
            if self.contains(corner_point):
                return True
        return False
    
    def combine(self, other: 'DiscreteAABBbounds') -> 'DiscreteAABBbounds':
        """Return the combination of these two bounding boxes"""
        assert(self.lower.__class__ == other.lower.__class__)

        return self.__class__(
            self.lower.__class__(*map(min, self.lower, other.lower)),  # type: ignore
            self.lower.__class__(*map(max, self.upper, other.upper)),  # type: ignore
        )
    
    def area(self) -> int:
        """Return the area bounded
            Returns as number of points generated

            i.e. when lower==upper, bounded area is 1
        """

        return reduce(mul, map(lambda mx, mi: mx - mi + 1, self.upper, self.lower))


if __name__ == "__main__":
    from .Point import DiscretePoint2

    aabb_1 = DiscreteAABBbounds(DiscretePoint2(0,0), DiscretePoint2(1,1))
    aabb_2 = DiscreteAABBbounds(DiscretePoint2(1,1), DiscretePoint2(2,2))
    aabb_3 = DiscreteAABBbounds(DiscretePoint2(1,2), DiscretePoint2(2,4))

    aabb_12 = DiscreteAABBbounds(DiscretePoint2(0,0), DiscretePoint2(2,2))

    for _ in range(3):
        print(list(aabb_1.generate_corners()))
        print(list(aabb_2.generate_corners()))
        assert aabb_1.intersects(aabb_2)
        assert aabb_2.intersects(aabb_1)
        assert aabb_2.intersects(aabb_3)
        assert aabb_3.intersects(aabb_2)
        assert not aabb_1.intersects(aabb_3)
        assert not aabb_3.intersects(aabb_1)

        assert aabb_1.intersects(aabb_2)
        assert aabb_2.intersects(aabb_1)
        assert aabb_2.intersects(aabb_3)
        assert aabb_3.intersects(aabb_2)
        assert not aabb_1.intersects(aabb_3)
        assert not aabb_3.intersects(aabb_1)

        assert aabb_1.combine(aabb_2) == aabb_12
        assert aabb_2.combine(aabb_1) == aabb_12
        assert aabb_1.combine(DiscreteAABBbounds(DiscretePoint2(1,1), DiscretePoint2(1,1))) == aabb_1
