from enum import Enum, unique
from typing import Literal, Union


from .Point import DiscretePoint2


CarrotDirections_T = Union[Literal[">"], Literal["<"], Literal["v"], Literal["^"]]
LetterDirections_T = Union[
    Literal["u"],
    Literal["U"],
    Literal["d"],
    Literal["D"],
    Literal["r"],
    Literal["R"],
    Literal["l"],
    Literal["L"],
]
DirectionsCharset_T = Union[CarrotDirections_T, LetterDirections_T]


@unique
class Direction2(Enum):
    """A direction coordinate system and utilities"""

    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    @property
    def opposite(self) -> "Direction2":
        """Get the Opposite Direction"""
        if self == Direction2.RIGHT:
            return Direction2.LEFT
        elif self == Direction2.UP:
            return Direction2.DOWN
        elif self == Direction2.LEFT:
            return Direction2.RIGHT
        elif self == Direction2.DOWN:
            return Direction2.UP
        raise NotImplementedError(self)

    @property
    def get_transform(self) -> DiscretePoint2:
        if self == Direction2.RIGHT:
            return DiscretePoint2(1, 0)
        elif self == Direction2.UP:
            return DiscretePoint2(0, 1)
        elif self == Direction2.LEFT:
            return DiscretePoint2(-1, 0)
        elif self == Direction2.DOWN:
            return DiscretePoint2(0, -1)
        raise NotImplementedError(self)

    def turn_right(self) -> "Direction2":
        if self == Direction2.RIGHT:
            return Direction2.DOWN
        elif self == Direction2.DOWN:
            return Direction2.LEFT
        elif self == Direction2.LEFT:
            return Direction2.UP
        else:
            assert self == Direction2.UP
            return Direction2.RIGHT

    def turn_left(self) -> "Direction2":
        if self == Direction2.RIGHT:
            return Direction2.UP
        elif self == Direction2.UP:
            return Direction2.LEFT
        elif self == Direction2.LEFT:
            return Direction2.DOWN
        else:
            assert self == Direction2.DOWN
            return Direction2.RIGHT

    @classmethod
    def from_str(cls, direction: DirectionsCharset_T) -> "Direction2":
        """Get a direction from a string"""
        if direction in "rR>":
            return cls.RIGHT
        elif direction in "uU^":
            return cls.UP
        elif direction in "lL<":
            return cls.LEFT
        elif direction in "dDv":
            return cls.DOWN
        raise ValueError(direction)

    @classmethod
    def transform_point(
        cls,
        point: DiscretePoint2,
        direction: DirectionsCharset_T,
    ) -> DiscretePoint2:
        return point + cls.from_str(direction).get_transform
