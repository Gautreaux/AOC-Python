# from AOC_Lib.name import *

from collections import Counter
from enum import Enum, unique
import itertools


# TODO - refactor, this should be in the library, many things use this
@unique
class CartDirection(Enum):
    """The direction a cart is facing"""
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    @classmethod
    def turn_left(cls, dir: "CartDirection") -> "CartDirection":
        """Turn left from given direction"""
        if dir == cls.UP:
            return cls.LEFT
        elif dir == cls.LEFT:
            return cls.DOWN
        elif dir == cls.DOWN:
            return cls.RIGHT
        elif dir == cls.RIGHT:
            return cls.UP
        else:
            raise RuntimeError(dir)

    @classmethod
    def turn_right(cls, dir: "CartDirection") -> "CartDirection":
        """Turn right from given direction"""
        if dir == cls.UP:
            return cls.RIGHT
        elif dir == cls.RIGHT:
            return cls.DOWN
        elif dir == cls.DOWN:
            return cls.LEFT
        elif dir == cls.LEFT:
            return cls.UP
        else:
            raise RuntimeError(dir)


class Cart:
    """A Cart"""

    def __init__(self, position: tuple[int, int], direction:CartDirection) -> None:
        self.pos = position
        self.dir = direction
        self.turn = itertools.cycle([
            lambda x: CartDirection.turn_left(x),
            lambda x: x,
            lambda x: CartDirection.turn_right(x),
        ])

    def advance(self, layout:list[str]) -> None:
        """Advance the cart and update appropriately"""
        if self.dir == CartDirection.LEFT:
            self.pos = (self.pos[0] - 1, self.pos[1])
        elif self.dir == CartDirection.RIGHT:
            self.pos = (self.pos[0] + 1, self.pos[1])
        elif self.dir == CartDirection.UP:
            self.pos = (self.pos[0], self.pos[1] - 1)
        elif self.dir == CartDirection.DOWN:
            self.pos = (self.pos[0], self.pos[1] + 1)
        
        # now see if we need to turn
        c = layout[self.pos[1]][self.pos[0]]

        if c == '/':
            if self.dir in [CartDirection.UP, CartDirection.DOWN]:
                self.dir = CartDirection.turn_right(self.dir)
            else:
                self.dir = CartDirection.turn_left(self.dir)
        elif c == "\\":
            if self.dir in [CartDirection.UP, CartDirection.DOWN]:
                self.dir = CartDirection.turn_left(self.dir)
            else:
                self.dir = CartDirection.turn_right(self.dir)
        elif c == "+":
            # this is an intersection
            self.dir = next(self.turn)(self.dir)


def getCollidingPositions(cart_list: list[Cart]) -> list[tuple[int, int]]:
    """Return a list of all the currently colliding positions"""

    c = Counter(map(lambda x: x.pos, cart_list))
    return list(map(lambda x: x[0], filter(lambda x: x[1] >= 2, c.items())))


# TODO - this seems like it should also be in the library
def drawLayoutRegion(layout: list[str], pos: tuple[int, int], scope: int = 5):
    """Draw `scope` squares on each side of `pos` from `layout` """
    for y in range(max(0, pos[1] - scope), min(pos[1] + scope + 1, len(layout))):
        for x in range(max(0, pos[0] - scope), min(pos[0] + scope + 1, len(layout[y]))):
            if (x,y) == pos:
                print("*", end="")
            else:
                print(layout[y][x], end="")
        print("")
    print(f"At given pos char is `{layout[y][x]}`")


def y2018d13(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d13.txt"
    print("2018 day 13:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip("\r\n")
            lineList.append(line)

    track_layout = []
    cart_list: list[Cart] = []

    for y, row in enumerate(lineList):
        new_row = []
        for x, cell in enumerate(row):
            if cell == "<":
                cart_list.append(Cart((x,y), CartDirection.LEFT))
                print(f"Adding cart at {(x,y)}: `{lineList[y][x]}`")
                new_row.append("-")
            elif cell == ">":
                cart_list.append(Cart((x,y), CartDirection.RIGHT))
                print(f"Adding cart at {(x,y)}: `{lineList[y][x]}`")
                new_row.append("-")
            elif cell == "^":
                cart_list.append(Cart((x,y), CartDirection.UP))
                print(f"Adding cart at {(x,y)}: `{lineList[y][x]}`")
                new_row.append("|")
            elif cell == "v":
                cart_list.append(Cart((x,y), CartDirection.DOWN))
                print(f"Adding cart at {(x,y)}: `{lineList[y][x]}`")
                new_row.append("|")
            else:
                new_row.append(cell)
        assert(len(new_row) == len(row))
        track_layout.append("".join(new_row))
  
    assert(len(track_layout) == len(lineList))
    assert(len(getCollidingPositions(cart_list)) == 0)
    
    # check for added or removed characters
    assert(sum(1 for _ in itertools.chain.from_iterable(track_layout)) == sum(1 for _ in itertools.chain.from_iterable(lineList)))
    # check that characters are valid
    try:
        assert(all(map(lambda x: x in " |-/+\\", itertools.chain.from_iterable(track_layout))))
    except AssertionError:
        print(set(itertools.chain.from_iterable(track_layout)))
        raise

    for this_time in itertools.count():
        if this_time % 200 == 0:
            print(f"Starting time: {this_time}")

        # print(f"Carts are at: {list(map(lambda x: x.pos, cart_list))}")
        
        for cart in cart_list:
            if track_layout[cart.pos[1]][cart.pos[0]] == " ":
                print(cart.pos)
                drawLayoutRegion(track_layout, cart.pos)
                assert(False)

        # advance the carts
        for cart in cart_list:
            cart.advance(track_layout)
        
        # check for new collisions
        c = getCollidingPositions(cart_list)

        if Part_1_Answer is None:
            if len(c) == 0:
                pass
            elif len(c) == 1:
                Part_1_Answer = c[0]
            else:
                raise RuntimeWarning(f"Multiple candidates for first collision: {c}")
                Part_1_Answer = c[0]
        
        # part 2:
        if len(c) > 0:
            cart_list = list(filter(lambda x: x.pos not in c, cart_list))
            print(f"{this_time}: Total Carts Remaining: {len(cart_list)}")
            if len(cart_list) == 0:
                raise RuntimeError(f"All carts are colliding")
            elif len(cart_list) == 1:
                Part_2_Answer = cart_list[0].pos
                break

    Part_1_Answer = f"{Part_1_Answer[0]},{Part_1_Answer[1]}"
    
    assert(Part_2_Answer != (52,33))

    return (Part_1_Answer, Part_2_Answer)