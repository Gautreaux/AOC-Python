
class BoundedInt:
    """An integer fixed between lower inclusive and upper exclusive bound with arithmetic rollover/under"""
    def __init__(self, upper_bound, lower_bound=0, value=0) -> None:
        if lower_bound != 0:
            # TODO - there is some error when lowerbound is not zero
            raise NotImplementedError("Lowerbound should be 0")
        
        self.v = value
        self.u = upper_bound
        self.l = lower_bound

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
    
    def __add__(self, o: 'BoundedInt') -> 'BoundedInt':
        return BoundedInt(self.u, self.l, self.v + o)

    def __sub__(self, o: 'BoundedInt') -> 'BoundedInt':
        return BoundedInt(self.u, self.l, self.v - o)
    
    def __mul__(self, o: 'BoundedInt') -> 'BoundedInt':
        return BoundedInt(self.u, self.l, self.v * o)
    
    def __mul__(self, o: 'BoundedInt') -> 'BoundedInt':
        return BoundedInt(self.u, self.l, self.v / o)
    
    def __eq__(self, o: 'BoundedInt') -> bool:
        return self.v == o

# TODO - proper unit testing on this one