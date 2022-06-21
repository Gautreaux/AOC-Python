from AOC_Lib.SlidingWindow import sliding_window
from .IntcodeLib import IntcodeProgram, IntcodeRunner

from copy import  deepcopy
from enum import IntEnum, unique
import itertools
from typing import Any, Generator, Iterable, Optional, Union


PATH_T = list[tuple[str, int]]

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


def buildIdealPath(sim: ResultSimulator) -> PATH_T:
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

    out_paired = []
    itr = iter(out)
    assert(len(out) % 2 == 0)
    while True:
        try:
            lhs = next(itr)
            rhs = next(itr)
            out_paired.append((lhs, rhs))
        except StopIteration:
            break
    return out_paired


class Compressor:
    """Manages compressing a `raw_path` int an Ascii-Code program"""

    def __init__(self) -> None:
        self._reset()

    def _reset(self):
        """reset to a ready state"""
    
    def _is_full_mask(self, mask: list[Optional[str]]) -> bool:
        """Return `True` iff the mask completely covers the path"""
        return all(map(lambda x: x is not None, mask))

    def _compressor_worker(self, raw_path: PATH_T) -> list[str]:
        """Worker for the first layer"""
        mask = [None]*len(raw_path)

        for i,v in enumerate(raw_path):
            if v == raw_path[0]:
                mask[i] = 'A'

        if self._is_full_mask(mask):
            return mask

        mask_iter = iter(mask)
        next(mask_iter)
        max_function_len = 1 + sum(1 for _ in itertools.takewhile(
            lambda x: x is None, mask_iter
        ))

        # debug
        max_function_len = 3

        print("The longest length possible for the first function is:", max_function_len)

        for first_function_len in range(1, max_function_len+1):
            mask = [None]*len(raw_path)
            hunk = tuple(raw_path[:first_function_len])

            # print('START A:', to_match)

            self._sliding_window_mask(raw_path, mask, hunk, 'A')

            if self._is_full_mask(mask):
                return {'A' : hunk, 0: mask }

            print("".join(map(lambda x: x if x is not None else '.', mask)))

            r = self._compressor_worker_b(raw_path, mask, 'B')
            if r is not None:
                r['A'] = hunk
                return r
            # print('END A:', to_match)

    def _compressor_worker_b(
        self, 
        raw_path: PATH_T, 
        mask: list[Optional[str]], 
        group: str
    ) -> Optional[list[str]]:
        """Handles the sub partitioning for secondary layers"""

        # find the first hole
        hunk = list(
            map(
                lambda x: x[0],
                itertools.takewhile(
                    lambda x: x[1] is None, 
                    itertools.dropwhile(
                        lambda x: x[1] is not None,
                        zip(raw_path, mask)
                    )
                )
            )
        )

        next_group = chr(ord(group) + 1)

        # print(f"Attempting to place `{group}` into {hunk}")

        old_mask = deepcopy(mask)

        for function_len in range(1, len(hunk)+1):
            # ensure that we have no side effects
            mask = deepcopy(old_mask) 

            to_match = tuple(hunk[:function_len])

            # print("START", group, to_match)
            self._sliding_window_mask(raw_path, mask, to_match, group)

            print("".join(map(lambda x: x if x is not None else '.', mask)))
            if self._is_full_mask(mask):
                return {group: hunk, 0: mask}
            
            if next_group <= 'C':
                r = self._compressor_worker_b(raw_path, mask, next_group)
                if r is not None:
                    r[group] = hunk
                    return r
            # print("END", group, to_match)

    def _sliding_window_mask(self, raw_path: PATH_T, mask: list[Optional[str]], hunk, val: str):
        """Apply a sliding widow over `raw_path`
            if the window matches `hunk` and the corresponding `mask` is entirely None,
                update (in place) the `mask` to have `val`
        """
    
        fn_len = len(hunk)
        for i,w in enumerate(sliding_window(raw_path, fn_len)):
            if w != hunk:
                    continue

            # make sure that this section of the mask is None
            mask_hunk = mask[i:(i+fn_len)]
            if any(map(lambda x: x is not None, mask_hunk)):
                continue

            for j in range(i, i+fn_len):
                mask[j] = val


    def compress(self, raw_path: PATH_T) -> tuple[list[str], PATH_T, PATH_T, PATH_T]:
        """Actually do the compression"""

        # The idea is that the first item in `raw_path` must the first `function`
        #   likewise, the first piece after the first function must begin the second `function`
        m = self._compressor_worker(raw_path)

        if m is None:
            print("Could not create a mask...")
            assert(False)

        print(f"Got Mask back:", m)

        # TODO - reduce the mask back into `ABACACACB`
        #   return




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

    c = Compressor()
    print(c.compress(ideal))

    # runner = IntcodeRunner(prog)
    # runner.setAddr(0, 2)

    return (Part_1_Answer, Part_2_Answer)