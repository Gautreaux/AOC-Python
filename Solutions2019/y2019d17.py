from .IntcodeLib import IntcodeProgram, IntcodeRunner

from enum import IntEnum, unique
import itertools
from typing import Any, Generator, Iterable, Optional, Union


_MAX_CHAR_PER_LINE = 20

@unique
class ImageComponent(IntEnum):
    NEWLINE = 10,
    SCAFFOLD = 35,
    SPACE = 46,
    ROBOT_UP = 94,

    def render(self) -> int:
        return chr(self.value)


@unique
class RobotDirection(IntEnum):
    UP = 0,
    RIGHT = 1,
    DOWN = 2,
    LEFT = 3

    def turnLeft(self) -> "RobotDirection":
        return RobotDirection((self.value + 3) % 4)

    def turnRight(self) -> "RobotDirection":
        return RobotDirection((self.value + 1) % 4)

    def apply(self, position: tuple[int, int]) -> tuple[int,int]:
        """Apply direction to position to get new position"""
        x,y = position
        if self == RobotDirection.UP:
            return (x, y - 1)
        elif self == RobotDirection.RIGHT:
            return (x + 1, y)
        elif self == RobotDirection.DOWN:
            return (x, y + 1)
        elif self == RobotDirection.LEFT:
            return (x - 1, y)
        else:
            raise RuntimeError()


class Image:
    def __init__(self, iterable) -> None:
        self.rows = []
        
        current = []
        for f in iterable:
            c = ImageComponent(f)
            if c == ImageComponent.NEWLINE:
                if current:
                    self.rows.append(current)
                    current = []
            else:
                current.append(c)
        if current:
            self.rows.append(current)

    def draw(self):
        """Draw image"""
        for row in self.rows:
            print("".join(map(lambda x: x.render(), row)))

    def isScaffold(self, x, y) -> bool:
        """Return true if scaffold or if contains scaffold"""
        c = self.rows[y][x]

        if c == ImageComponent.NEWLINE or c == ImageComponent.SPACE:
            return False
        return True

    def generateAlignmentPositions(self) -> Generator[tuple[int, int], None, None]:
        """Generate all positions that are alignment points"""

        transforms = [
            (0,1),
            (0,-1),
            (0,0),
            (1,0),
            (-1,0)
        ]

        for y in range(1, len(self.rows) - 1):
            for x in range(1, len(self.rows[y]) - 1):
                if all(
                    map(
                        lambda p: self.isScaffold(p[0], p[1]),
                        map(
                            lambda t: (x + t[0], y + t[1]),
                            transforms
                        )
                    )
                ):
                    yield (x,y)


class ResultSimulator:
    """Give option to simulate the results of a program"""

    def __init__(self, img: Image) -> None:
        self._start_robot_pos = None
        self._start_robot_dir = None

        # set of all scaffolding positions
        self._scaffolding_pos = set()

        for y,row in enumerate(img.rows):
            for x,c in enumerate(row):
                if img.isScaffold(x,y):
                    self._scaffolding_pos.add((x,y))

                # TODO - other directions
                if c == ImageComponent.ROBOT_UP:
                    self._start_robot_pos = (x,y)
                    self._start_robot_dir = RobotDirection.UP
    
    def isScaffold(self, x, y) -> bool:
        return ((x,y) in self._scaffolding_pos)

    def getStartPos(self) -> tuple[int, int]:
        """Return the starting position"""
        return self._start_robot_pos
    
    def getStartDirection(self) -> RobotDirection:
        """Return the starting direction"""
        return self._start_robot_dir

    def isForwardScaffold(self, position: tuple[int, int], direction: RobotDirection) -> bool:
        """return True iff, for the position, direction, forward is a scaffold block"""
        x,y = direction.apply(position)
        return self.isScaffold(x,y)

    def isLeftScaffold(self, position: tuple[int, int], direction: RobotDirection) -> bool:
        """Return True iff the tile left of the robot is scaffold"""
        return self.isForwardScaffold(position, direction.turnLeft())
    
    def isRightScaffold(self, position: tuple[int, int], direction: RobotDirection) -> bool:
        """Return True iff the tile left of the robot is scaffold"""
        return self.isForwardScaffold(position, direction.turnRight())

    @classmethod
    def isValidProgram(cls, main: list[str], a: list[str], b: list[str], c: list[str]) -> Optional[str]:
        """Return true if the produced output is valid syntactically
            returns None on success
            otherwise returns sting describing failure
        """
        l = [main, a, b, c]
        if any(map(lambda x: len(x) > _MAX_CHAR_PER_LINE, l)):
            return "One of the methods is too long"

        if any(map(lambda x: len(x) != 1, itertools.chain.from_iterable(l))):
            return "One of the commands is not a single charater"
        
        main_set = set(iter(main)) - {'A', 'B', 'C'}
        if main_set:
            return f"Illegal chars in main: {main_set}"

        # TODO - remainder


def buildIdealPath(sim: ResultSimulator) -> list[Union[str,int]]:
    """Build the perfect path"""

    out = []

    r_pos = sim.getStartPos()
    r_dir = sim.getStartDirection()

    counter = 0
    while True:
        if sim.isForwardScaffold(r_pos, r_dir):
            counter += 1
            r_pos = r_dir.apply(r_pos)
            continue

        right_is_scaffold = sim.isRightScaffold(r_pos, r_dir)
        left_is_scaffold = sim.isLeftScaffold(r_pos, r_dir)

        if right_is_scaffold and left_is_scaffold:
            print(f"Start: {sim.getStartPos()} {sim.getStartDirection()}")
            print(out)
            print(counter)
            print(sim.isForwardScaffold(r_pos, r_dir))
            print(f"Pos: {r_pos}, Dir: {r_dir}")
            raise RuntimeError("Should be unreachable")
        if (not right_is_scaffold) and (not left_is_scaffold):
            # ending condition
            if counter:
                out.append(counter)
                counter = 0
            break
        assert(left_is_scaffold != right_is_scaffold)
        
        if counter:
            out.append(counter)
        counter = 0

        if left_is_scaffold:
            out.append('L')
            r_dir = r_dir.turnLeft()
        else:
            assert(right_is_scaffold)
            out.append('R')
            r_dir = r_dir.turnRight()
    return out


def pairwise(iterable: Iterable[Any]) -> Generator[tuple[Any, Any], None, None]:
    a,b = itertools.tee(iterable)
    _ = next(b)
    return zip(a,b)


def listCompressIterator(iterable: Iterable[Any], p: tuple[Any, Any]) -> Generator[Any, None, None]:
    """Return a generator of the same thing compressed so that
        any two consecutive elements matching p are compressed into one
    """
    a,b = itertools.tee(iterable)
    _ = next(b)

    while True:
        try:
            a_val = next(a)
        except StopIteration:
            return
        
        try:
            b_val = next(b)
        except StopIteration:
            yield a_val
            return
        
        if a_val == p[0] and b_val == p[1]:
            yield (a_val,b_val)
            try:
                _ = next(a)
                _ = next(b)
            except StopIteration:
                pass
        else:
            yield a_val


def flatten(maybe_iterable) -> Generator[Any, None, None]:
    """Flatten nested iterables into one"""

    try:
        a = iter(maybe_iterable)
    except TypeError:
        yield maybe_iterable 
        return

    for f in a:
        try:
            i = iter(f)
            for k in i:
                yield k
        except TypeError:
            yield f



def compressPath(full_path: list[Any]) -> Generator[tuple[Any, Any], None, None]:

    tried = set()

    for p in pairwise(full_path):
        if p in tried:
            continue
        else:
            tried.add(p)
            new_l = list(listCompressIterator(full_path, p))
            new_l = list(map(lambda x: tuple(flatten(x)), new_l))
            print(f"Compressing {p} -> {new_l}")
            compressPath(new_l)
            return
            


def y2019d17(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d17.txt"
    print("2019 day 17:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    prog = IntcodeProgram(map(int, lineList[0].split(",")))
    runner = IntcodeRunner(prog)

    image = Image(runner.run_sync())

    image.draw()

    Part_1_Answer = sum(map(
        lambda x: x[0]*x[1],
        image.generateAlignmentPositions()
    ))

    ### part2

    ### generate the ideal path

    simulator = ResultSimulator(image)
    ideal = buildIdealPath(simulator)

    print(ideal)

    compressPath(ideal)


    # runner = IntcodeRunner(prog)
    # runner.setAddr(0, 2)

    return (Part_1_Answer, Part_2_Answer)