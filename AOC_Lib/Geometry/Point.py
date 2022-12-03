
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterator
from operator import add, sub

@abstractmethod
class AbstractPoint(ABC):
    """A point in abstract space"""

    @abstractmethod
    def _iter_dims(self) -> Iterator[Any]:
        """Create an iterator over the dimensions of this point"""
        raise NotImplementedError

    def origin_factory(self) -> 'AbstractPoint':
        """Factory to create an all-zeroed point"""
        return self.__class__(*map(lambda x: 0, self._iter_dims()))

    @property
    def is_origin(self) -> bool:
        """Return `True` iff this is the origin"""
        return all(map(lambda x: x == 0, self._iter_dims()))

    def __len__(self):
        return sum(1 for _ in self._iter_dims())
    
    def __str__(self) -> str:
        return "({})".format(",".join(map(str, self._iter_dims())))

    def dimension(self):
        """Return the dimension of this point"""
        return len(self)
    
    def __add__(self, other: 'AbstractPoint') -> 'AbstractPoint':
        return self.__class__(*map(add, self._iter_dims(), other._iter_dims()))

    def __sub__(self, other: 'AbstractPoint') -> 'AbstractPoint':
        return self.__class__(*map(sub, self._iter_dims(), other._iter_dims()))

    def norm(self, other: 'AbstractPoint', X: int) -> float:
        """Return the X-norm of this point and another point
            Probably do not call this directly
        """

        # Slightly more efficient for manhattan distance
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


class DiscreteAbstractPoint(AbstractPoint):
    """Abstract point, but discrete (integer) space"""
    
    # This is just type-annotating the return value as int in this case
    def manhattan_distance(self, other: 'DiscreteAbstractPoint') -> int:
        return super().manhattan_distance(other)


@dataclass(frozen=True)
class DiscretePoint2(DiscreteAbstractPoint):
    """A point in 2D space, with integer coordinates"""

    x: int
    y: int

    def _iter_dims(self) -> Iterator[int]:
        """Iterate across the dimensions"""
        yield self.x
        yield self.y

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