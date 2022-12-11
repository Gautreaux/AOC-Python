
from abc import ABC, abstractmethod
from dataclasses import dataclass
import itertools
from typing import Any, Iterator, Type, TypeVar
from operator import add, sub


DerivedPoint_T = TypeVar('DerivedPoint_T', bound='AbstractPoint')
DerivedDiscretePoint_T = TypeVar('DerivedDiscretePoint_T', bound='DiscreteAbstractPoint')

@abstractmethod
class AbstractPoint(ABC):
    """A point in abstract space"""

    @abstractmethod
    def _iter_dims(self) -> Iterator[Any]:
        """Create an iterator over the dimensions of this point"""
        raise NotImplementedError

    def origin_factory(self: DerivedPoint_T) -> DerivedPoint_T:
        """Factory to create an all-zeroed point"""
        return self.__class__(*map(lambda x: 0, self._iter_dims())) # type: ignore

    @property
    def is_origin(self) -> bool:
        """Return `True` iff this is the origin"""
        return all(map(lambda x: x == 0, self._iter_dims()))

    def __len__(self):
        return sum(1 for _ in self._iter_dims())
    
    def __str__(self) -> str:
        return "({})".format(",".join(map(str, self._iter_dims())))

    def __iter__(self) -> Iterator[float]:
        return self._iter_dims()

    def __getitem__(self, key: int):
        """Return the value at the given dimension; Probably inefficient"""

        try:
            return next(itertools.islice(self, key, None))
        except StopIteration:
            raise IndexError(key) from None

    def dimension(self) -> int:
        """Return the dimension of this point"""
        return len(self)
    
    def __add__(self: DerivedPoint_T, other: DerivedPoint_T) -> DerivedPoint_T:
        return self.__class__(*map(add, self._iter_dims(), other._iter_dims())) # type: ignore

    def __sub__(self: DerivedPoint_T, other: DerivedPoint_T) -> DerivedPoint_T:
        return self.__class__(*map(sub, self._iter_dims(), other._iter_dims())) # type: ignore

    def scale(self: DerivedPoint_T, scalar: float) -> DerivedPoint_T:
        return self.__class__(*map(lambda x: x*scalar, self._iter_dims)) # type: ignore

    def norm(self: DerivedPoint_T, other: DerivedPoint_T, X: int) -> float:
        """Return the X-norm of this point and another point
            Probably do not call this directly
        """

        # Slightly more efficient for 1-norm (manhattan distance)
        if X == 1:
            return sum(map(
                lambda a,b: abs(a-b),
                self._iter_dims(),
                other._iter_dims(),
            ))

        return pow(
            sum(map(
                lambda a,b: pow(abs(a-b), X),
                self._iter_dims(),
                other._iter_dims(),
            )),
            1/X
        )
    
    def distance(self, other: 'AbstractPoint') -> float:
        """Return the straight-line distance between this point and other point"""
        return self.norm(other, 2)
    
    def manhattan_distance(self, other: 'AbstractPoint') -> float:
        """Return the manhattan distance between this point and other point"""
        return self.norm(other, 1)


@dataclass(frozen=True)
class Point2(AbstractPoint):
    """A Point in 2D space"""

    x: float
    y: float

    def _iter_dims(self) -> Iterator[Any]:
        yield self.x
        yield self.y


@dataclass(frozen=True)
class Point3(AbstractPoint):
    """A Point in 3D space"""

    x: float
    y: float
    z: float

    def _iter_dims(self) -> Iterator[Any]:
        yield self.x
        yield self.y
        yield self.z


class DiscreteAbstractPoint(AbstractPoint):
    """Abstract point, but discrete (integer) space"""
    
    # This is just type-annotating the return value as int in this case
    def manhattan_distance(self: DerivedDiscretePoint_T, other: DerivedDiscretePoint_T) -> int:
        return super().manhattan_distance(other) # type: ignore

    # This is just type-annotating the return value as int in this case
    def scale_discrete(self: DerivedDiscretePoint_T, scalar: int) -> DerivedDiscretePoint_T:
        return super().scale(self, scalar) # type: ignore

    # This is just type-annotating the return value as int in this case
    def __iter__(self) -> Iterator[int]:
        return super().__iter__() # type: ignore

    def cartesian_neighbors(
        self: DerivedDiscretePoint_T,
        include_self: bool = False
    ) -> Iterator[DerivedDiscretePoint_T]:
        """Return an iterator over the cartesian neighbors of this point"""
        
        if include_self:
            yield self

        dim = len(self)
        for i in range(dim):
            yield self.__class__(*map(lambda a,b: b+1 if a == i else b, range(dim), self._iter_dims())) # type: ignore
            yield self.__class__(*map(lambda a,b: b-1 if a == i else b, range(dim), self._iter_dims())) # type: ignore

    def cartesian_neighbors_with_diagonals(
        self: DerivedPoint_T,
        include_self: bool = False
    ) -> Iterator[DerivedPoint_T]:
        """Return an iterator over the cartesian neighbors of this point, with diagonals"""

        dims = (-1, 0, 1)
        iters = map(lambda _: dims, range(len(self)))

        for t in itertools.product(*iters):
            if all(map(lambda x: x == 0, t)) and not include_self:
                 continue
            yield self.__class__(*map(lambda a,b: a+b, t, self._iter_dims())) # type: ignore


@dataclass(frozen=True)
class DiscretePoint2(DiscreteAbstractPoint):
    """A point in 2D space, with integer coordinates"""

    x: int
    y: int

    def _iter_dims(self) -> Iterator[int]:
        """Iterate across the dimensions"""
        yield self.x
        yield self.y

    def scale(self, scalar: float) -> Point2:
        return Point2(self.x*scalar, self.y*scalar)


@dataclass(frozen=True)
class DiscretePoint3(DiscreteAbstractPoint):
    """A point in 3D space, with integer coordinates"""

    x: int
    y: int
    z: int

    def _iter_dims(self) -> Iterator[int]:
        """Iterate across the dimensions"""
        yield self.x
        yield self.y
        yield self.z

    def scale(self, scalar: float) -> Point3:
        return Point3(self.x*scalar, self.y*scalar, self.z*scalar)

