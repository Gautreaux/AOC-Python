# maintains the data structure for point(s)


from typing import Type


class Point2:
    def __init__(self, p1, p2=None):
        try:
            if len(p1) == 1:
                raise TypeError  # a dummy error
            if len(p1) == 2:
                self.x = p1[0]
                self.y = p1[1]
        except TypeError:
            self.x = p1
            self.y = p2

        # TODO - validate that p1 and p2 are both numeric types

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0 or key == "x":
            return self.x
        elif key == 1 or key == "y":
            return self.y

        raise KeyError(f"Invalid key ({str(key)}) in point2")

    def __setitem__(self, key, item):
        # TODO - validate item on success
        if key == 0 or key == "x":
            self.x = item
        elif key == 0 or key == "y":
            self.y = item

        raise KeyError(f"Invalid key ({str(key)}) in point2")

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, o: "Point2") -> bool:
        return self.x == o.x and self.y == o.y

    def __add__(self, o: "Point2") -> "Point2":
        return Point2(self.x + o.x, self.y + o.y)

    def __sub__(self, o: "Point2") -> "Point2":
        return Point2(self.x - o.x, self.y - o.y)

    def __mul__(self, o: int) -> "Point2":
        return Point2(self.x * o, self.y * o)

    def manhattan(self, o: "Point2 | tuple[int, int]" = (0, 0)) -> int:
        "compute the manhattan distance from this point to another"
        return abs(self[0] - o[0]) + abs(self[1] - o[1])


Y_DOWN_2_TRANSFORMS = {
    "U": Point2(0, -1),
    "L": Point2(-1, 0),
    "R": Point2(1, 0),
    "D": Point2(0, 1),
}

Y_UP_2_TRANSFORMS = {
    "U": Point2(0, 1),
    "L": Point2(-1, 0),
    "R": Point2(1, 0),
    "D": Point2(0, -1),
}

Y_2_TRANSLATIONS = {
    "N": "U",
    "S": "D",
    "E": "R",
    "W": "L",
    "U": "U",
    "D": "D",
    "L": "L",
    "R": "R",
    0: "U",
    2: "D",
    3: "L",
    1: "R",
    "^": "U",
    "v": "D",
    ">": "R",
    "<": "L",
}


# TODO - finish point3 implementation
class Point3:
    def __init__(self):
        pass
