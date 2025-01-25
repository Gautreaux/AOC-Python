import asyncio
import functools
import itertools
from typing import Generator, Iterable

from .IntcodeLib import IntcodeProgram, IntcodeRunner


TestPos_t = tuple[int, int]


def generateCornersForValue(
    pos: TestPos_t, size: int
) -> Generator[TestPos_t, None, None]:
    """Generate the corners of a square of a specific size"""
    min_x, min_y = pos
    yield (min_x, min_y)
    yield (min_x + size - 1, min_y)
    yield (min_x, min_y + size - 1)
    yield (min_x + size - 1, min_y + size - 1)


def _generateTestSquaresAcross(
    pos: TestPos_t, size: int
) -> Generator[Generator[TestPos_t, None, None], None, None]:
    """Generate grid squares going across some row at `size` resolution, forever"""
    for x in itertools.count(pos[0], size - 1):
        yield generateCornersForValue((x, pos[1]), size)


def generateTestSetsAtResolution(
    size: int, min_x: int = 0, min_y: int = 0
) -> Generator[Generator[TestPos_t, None, None], None, None]:
    """Allows querying the grid at a specific resolution for points
    each successive element is four corners of the test square
    returns in roughly increasing order of radius, forever
    """
    y_vals = itertools.count(min_y, size - 1)
    all_gens = []

    while True:
        for g in all_gens:
            yield next(g)

        all_gens.append(
            _generateTestSquaresAcross(pos=(min_x, next(y_vals)), size=size)
        )


def applyTransform(
    positions: Iterable[TestPos_t], transform: tuple[int, int]
) -> Iterable[TestPos_t]:
    """Apply `transform` to `positions`"""
    return map(lambda p: (p[0] + transform[0], p[1] + transform[1]), positions)


def shiftLeft(positions: Iterable[TestPos_t], amount: int = 1) -> Iterable[TestPos_t]:
    """Shift all `positions` left by `amount`"""
    return applyTransform(positions=positions, transform=(-amount, 0))


def shiftUp(positions: Iterable[TestPos_t], amount: int = 1) -> Iterable[TestPos_t]:
    """Shift all `positions` up by `amount`"""
    return applyTransform(positions=positions, transform=(0, -amount))


def y2019d19(inputPath=None):
    if inputPath == None:
        inputPath = "Input2019/d19.txt"
    print("2019 day 19:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    prog = IntcodeProgram(map(int, lineList[0].split(",")))
    loop = asyncio.get_event_loop()

    @functools.cache
    def checkPosInBeam(x: int, y: int) -> bool:
        """Return True iff the point is inside the beam"""
        runner = IntcodeRunner(prog)
        run_task = loop.create_task(runner.run())
        runner.getInputQ().put_nowait(x)
        runner.getInputQ().put_nowait(y)
        runner.runTillBlockOrExit(run_task, loop)
        assert runner.getOutputQ().qsize() == 1
        out_val = runner.getOutputQ().get_nowait()
        if out_val == 1:
            return True
        elif out_val == 0:
            return False
        else:
            raise RuntimeError("Should be unreachable")

    def printRegion(upper_left: TestPos_t, width: int, height: int) -> None:
        """Print some region to the console"""
        nonlocal checkPosInBeam
        for y in itertools.islice(itertools.count(upper_left[1]), height):
            for x in itertools.islice(itertools.count(upper_left[0]), width):
                if checkPosInBeam(x, y):
                    print("#", end="")
                else:
                    print(".", end="")
            print("")

    printRegion((0, 0), 50, 50)

    pos_in_beam = set()
    for y in range(50):
        for x in range(50):
            if checkPosInBeam(x, y):
                pos_in_beam.add((x, y))
    Part_1_Answer = len(pos_in_beam)

    # theres probably a math way to find this easier
    #   by getting an approximating line
    #   but whatever

    def areAllInBeam(positions: Iterable[TestPos_t]) -> bool:
        """Return `True` iff all positions are inside the beam"""
        nonlocal checkPosInBeam
        return all(map(lambda p: checkPosInBeam(*p), positions))

    best_guess_pos = None

    # find the first one where all squares are inside at 100 resolution
    for f in generateTestSetsAtResolution(100):
        l = list(f)
        if areAllInBeam(l):
            print(f"First all inside: {l}")
            best_guess_pos = l
            break

    if best_guess_pos is None:
        raise RuntimeError("Should be unreachable")

    while True:
        n = list(applyTransform(best_guess_pos, (-1, -1)))
        if areAllInBeam(n):
            best_guess_pos = n
            continue
        n = list(shiftLeft(best_guess_pos))
        if areAllInBeam(n):
            best_guess_pos = n
            continue
        n = list(shiftUp(best_guess_pos))
        if areAllInBeam(n):
            best_guess_pos = n
            continue
        break

    print(f"Best guess is now: ", best_guess_pos)

    # TODO - finalize

    mx = min(map(lambda p: p[0], best_guess_pos))
    my = min(map(lambda p: p[1], best_guess_pos))

    Part_2_Answer = mx * 10000 + my

    print(f"mx: {mx}, my: {my}, ANS: {Part_2_Answer}")
    # printRegion((mx-2, my-2), 104, 104)
    # assert(Part_2_Answer < 7960953)

    return (Part_1_Answer, Part_2_Answer)
