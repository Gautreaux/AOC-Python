class BoundedInt:
    """An integer fixed between lower inclusive and upper exclusive bound with arithmetic rollover/under"""

    def __init__(self, upper_bound: int, lower_bound: int = 0, value: int = 0) -> None:
        assert lower_bound < upper_bound

        if lower_bound != 0:
            # TODO - there is some error when lowerbound is not zero
            raise NotImplementedError("Lowerbound should be 0")

        self.v: int = value
        self.u: int = upper_bound
        self.l: int = lower_bound

        self.__bound()

    def __int__(self) -> int:
        return self.v

    def asInt(self) -> int:
        return int(self)

    def __str__(self) -> str:
        return str(self.v)

    def __repr__(self) -> str:
        return f"{str(self.v)} bounded [{self.l}, {self.u})"

    # actually implements the bounding behavior
    def __bound(self):
        if self.v >= self.u or self.v < self.l:
            self.v = self.v % (self.u - self.l) + self.l

    def __add__(self, o: int) -> "BoundedInt":
        return BoundedInt(self.u, self.l, self.v + o)

    def __sub__(self, o: int) -> "BoundedInt":
        return BoundedInt(self.u, self.l, self.v - o)

    def __mul__(self, o: int) -> "BoundedInt":
        return BoundedInt(self.u, self.l, self.v * o)

    def __div__(self, o: int) -> "BoundedInt":
        return BoundedInt(self.u, self.l, self.v // o)

    def __eq__(self, o: int) -> bool:
        return self.v == o

    def __hash__(self) -> int:
        return hash(self.v)


# TODO - proper unit testing on these items


class LockedInt:
    """An integer fixed between lower and upper inclusive bound (no rollover)"""

    def __init__(self, lower_bound, upper_bound, value=None) -> None:
        assert lower_bound <= upper_bound

        self.v: int = value if value is not None else lower_bound
        self.u: int = upper_bound
        self.l: int = lower_bound

        self.__bound()

    def __int__(self) -> int:
        return self.v

    def asInt(self) -> int:
        return int(self)

    def __str__(self) -> str:
        return str(self.v)

    def __repr__(self) -> str:
        return f"{str(self.v)} locked [{self.l}, {self.u}]"

    # actually implements the bounding behavior
    def __bound(self):
        if self.v < self.l:
            self.v = self.l
        elif self.v > self.u:
            self.v = self.u

    def __add__(self, o: int) -> "LockedInt":
        return LockedInt(self.l, self.u, self.v + o)

    def __sub__(self, o: int) -> "LockedInt":
        return LockedInt(self.l, self.u, self.v - o)

    def __mul__(self, o: int) -> "LockedInt":
        return LockedInt(self.l, self.u, self.v * o)

    def __div__(self, o: int) -> "LockedInt":
        return LockedInt(self.l, self.u, self.v // o)

    def __eq__(self, o: int) -> bool:
        return self.v == o

    def __hash__(self) -> int:
        return hash(self.v)
