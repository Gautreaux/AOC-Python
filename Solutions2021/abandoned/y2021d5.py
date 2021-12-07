# from AOC_Lib.name import *

import itertools
from typing import DefaultDict, Tuple, Optional, overload

class InfiniteIntersectionDegeneracy(Exception):
    pass

# needs to be descritized

class Line2D:
    def __init__(self, x1, y1, x2, y2) -> None:
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def isHorizontal(self) -> bool:
        return self.y1 == self.y2
    
    def isVertical(self) -> bool:
        return self.x1 == self.x2

    def __str__(self) -> str:
        return f"{self.x1},{self.y1} -> {self.x2},{self.y2}"

    @classmethod
    def fromInputLine(cls, line_str: str) -> "Line2D":
        start_s, _, end_s = line_str.partition(" -> ")
        x1_s,_,y1_s = start_s.partition(",")
        x2_s,_,y2_s = end_s.partition(",")

        l = Line2D(int(x1_s), int(y1_s), int(x2_s), int(y2_s))
        return l

    def getIntersectionPoint(self, other: "Line2D") -> Optional[Tuple[float, float]]:
        # via cramers rule

        d = (self.x2 - self.x1)*(other.y2 - other.y1) - (other.x2 - other.x1)*(self.y2 - self.y1)
        if d == 0:
            # this is the parallel case
            if self.isPointOnLine(other.x1, other.y1):
                raise InfiniteIntersectionDegeneracy()
            else:
                return None
        
        a = (self.x2*self.y1 - self.x1*self.y2)
        b = (other.x2*other.x1 - other.x1*other.y2)

        x = round((a * (other.x2 - other.x1) - b * (self.x2 - self.x1)) / d, 8)
        y = round((a * (other.y2 - other.y1) - b * (self.y2 - self.y1)) / d, 8)

        return (x,y)

    def isPointOnLine(self, x, y) -> bool:
        if self.isVertical():
            return self.x1 == x
        if self.isHorizontal():
            return self.y1 == y
        return (self.x1 - self.x2)*(self.y1 - self.y2) == (self.x2 - x)*(self.y2 - y)

class LineSegment2D(Line2D):
    @classmethod
    def fromInputLine(cls, line_str: str) -> "LineSegment2D":
        start_s, _, end_s = line_str.partition(" -> ")
        x1_s,_,y1_s = start_s.partition(",")
        x2_s,_,y2_s = end_s.partition(",")

        l = LineSegment2D(int(x1_s), int(y1_s), int(x2_s), int(y2_s))
        return l

    def isPointInSegment(self, x, y) -> bool:
        """DOES NOT CHECK IF POINT IS ON LINE"""

        # endpoint checks
        if self.x1 == x and self.y1 == y:
            return True
        if self.x2 == x and self.y2 == y:
            return True

        if self.isVertical():
            return ((self.y1 < y) != (self.y2 < y)) and (self.x1 == x)
        elif self.isHorizontal():
            return ((self.x1 < x) != (self.x2 < x)) and (self.y1 == y)
        else:
            return ((self.x1 < x) != (self.x2 < x)) and ((self.y1 < y) != (self.y2 < y))

    def getIntersectionPoint(self, other: "LineSegment2D") -> Optional[Tuple[float, float]]:
        try:
            s = super().getIntersectionPoint(other)
        except InfiniteIntersectionDegeneracy:
            print(self)
            print(other)
            raise NotImplementedError("TODO - need to check overlap in here")
        
        if s is None:
            return None
        x_int,y_int = s

        if self.isPointInSegment(x_int, y_int) and other.isPointInSegment(x_int, y_int):
            return (x_int, y_int)
        return None

def y2021d5(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d5.txt"
    print("2021 day 5:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    lineList = list(map(LineSegment2D.fromInputLine, lineList))

    lines_h_v = [l for l in lineList if l.isHorizontal() or l.isVertical()]

    point_set_1 = DefaultDict(int)

    for a,b in itertools.combinations(lines_h_v, r=2):
        s = a.getIntersectionPoint(b)
        if s:
            point_set_1[s] += 1

    Part_1_Answer = len(point_set_1)

    return (Part_1_Answer, Part_2_Answer)