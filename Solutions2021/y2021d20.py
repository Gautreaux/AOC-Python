# from AOC_Lib.name import *

import functools
from operator import or_
from typing import Any, Callable, Iterator, Optional

from AOC_Lib.SparseGrid import SparseGrid

Pixel_T = int

DARK_PIXEL = 0
LIGHT_PIXEL = 1


def charToPixel(c: str) -> Pixel_T:
    """Convert a char to the corresponding pixel"""
    return {
        ".": DARK_PIXEL,
        "#": LIGHT_PIXEL,
    }[c]


# TODO - refactor into generic SparseGrid type in AOC lib
#   and adapt many existing solutions to use it
class ScannerImage:

    def __init__(
        self, enhancement: tuple[Pixel_T], default: Pixel_T = DARK_PIXEL
    ) -> None:
        self._img = SparseGrid(default)
        assert len(enhancement) == 512
        self.enhancement = enhancement

    @classmethod
    def fromLines(
        cls,
        lines: list[str],
        default: Pixel_T = DARK_PIXEL,
        enhancement: Optional[tuple[Pixel_T]] = None,
    ) -> "ScannerImage":
        """Parse and return an image from lines
        May provide the enhancement directly or
        Provide `enhancement=None` to indicate the first line
            of `lines` is the enhancement and followed by a blank line
        """

        itr = iter(lines)

        if enhancement is None:
            enhancement = tuple(map(charToPixel, next(itr)))
            assert len(enhancement) == 512
            assert next(itr) == ""

        new_img = cls(enhancement, default)

        for y, line in enumerate(itr):
            for x, px_str in enumerate(line):
                px = charToPixel(px_str)
                if px != default:
                    new_img[x, y] = px

        return new_img

    def getPixelEnhance(self, x: int, y: int) -> Pixel_T:
        """Get the enhancement value for a particular pixel"""
        transforms = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (0, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]

        p = map(lambda t: self._img[(x + t[0], y + t[1])], transforms)
        p = list(p)
        assert len(p) == 9
        s = map(lambda px, sf: px << sf, p, range(8, -1, -1))
        s = list(s)
        assert len(s) == 9
        i = functools.reduce(or_, s)
        return self.enhancement[i]

    def __getitem__(self, xy: tuple[int, int]) -> Pixel_T:
        return self._img[xy]

    def __setitem__(self, xy: tuple[int, int], p: Pixel_T):
        self._img[xy] = p

    @property
    def default(self) -> Pixel_T:
        """Return the Default pixel"""
        return self._img.default

    def doesDefaultFlipOnEnhancement(self) -> False:
        """Return True if an pixel infinitely far away will invert on enhance"""
        if self.default == DARK_PIXEL and self.enhancement[0] == DARK_PIXEL:
            return False
        elif self.default == LIGHT_PIXEL and self.enhancement[-1] == LIGHT_PIXEL:
            return False
        return True

    def generatePixelPositions(self, overscan: int = 0) -> Iterator[tuple[int, int]]:
        """Generate all pixel positions: (x,y) tuples
        optional parameter `overscan` specifies distance outside grid to scan

        Positions are generated in y-major (increasing) order
        """
        return self._img.generateAllPositions(overscan=overscan)

    def generatePixels(self, overscan: int = 0) -> Iterator[Pixel_T]:
        """Generate all pixels
        optional parameter `overscan` specifies distance outside grid to scan

        see `generatePixelPositions` for more info
        """
        return self._img.generateAllCells(overscan=overscan)

    def mapOnPixelPositions(
        self,
        callable: Callable[[tuple[int, int]], Any],
        overscan: int = 0,
    ) -> Iterator[Any]:
        """Apply `callable` to each pixel provided coordinates
        and optional `overscan` to scan pixels outside the grid
        """
        return self._img.mapOnPositions(callable, overscan=overscan)

    def mapOnPixels(
        self,
        callable: Callable[[Pixel_T], Any],
        overscan: int = 0,
    ) -> Iterator[Any]:
        """Apply `callable` to each pixel in the image
        and optional `overscan` to scan pixels outside the grid
        """
        return self._img.mapOnCells(callable, overscan=overscan)

    def enhance(self) -> "ScannerImage":
        """Enhance the image"""

        if self.doesDefaultFlipOnEnhancement():
            new_default = DARK_PIXEL if self.default == LIGHT_PIXEL else LIGHT_PIXEL
            new_img = ScannerImage(self.enhancement, new_default)
        else:
            new_img = ScannerImage(self.enhancement, self.default)

        for _ in self.mapOnPixelPositions(
            lambda x: new_img.__setitem__(x, self.getPixelEnhance(*x)), overscan=1
        ):
            pass

        return new_img

    def printImg(self, formatter: Callable[[Pixel_T], str] = str) -> None:
        """Print the image to the console"""
        self._img.printGrid(formatter=formatter, overscan=2)


def y2021d20_test():
    """Test function"""
    lineList = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""".splitlines()

    img = ScannerImage.fromLines(lineList)
    enhanced = img.enhance()
    enhanced_enhanced = enhanced.enhance()

    # f = lambda p: "#" if p == LIGHT_PIXEL else "."
    # print("Starting image:")
    # img.printImg(formatter=f)
    # print("After one round")
    # enhanced.printImg(formatter=f)
    # print("After two rounds")
    # enhanced_enhanced.printImg(formatter=f)

    assert enhanced_enhanced.default == DARK_PIXEL
    s = sum(enhanced_enhanced.mapOnPixels(lambda x: 1 if x == LIGHT_PIXEL else 0))
    assert s == 35

    enhancements = [img]

    while True:
        try:
            final_img = enhancements[50]
            break
        except IndexError:
            enhancements.append(enhancements[-1].enhance())
    assert final_img.default == DARK_PIXEL
    s = sum(final_img.mapOnPixels(lambda x: 1 if x == LIGHT_PIXEL else 0))
    assert s == 3351
    print("Tests passing")


def y2021d20(inputPath=None):
    if inputPath == None:
        inputPath = "Input2021/d20.txt"
    print("2021 day 20:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    y2021d20_test()

    original_image = ScannerImage.fromLines(lineList)

    enhanced_image = original_image.enhance()
    enhanced_enhanced_image = enhanced_image.enhance()

    if enhanced_enhanced_image.default == LIGHT_PIXEL:
        raise RuntimeError(f"The answer will be infinite")

    Part_1_Answer = sum(
        enhanced_enhanced_image.mapOnPixels(lambda x: 1 if x == LIGHT_PIXEL else 0)
    )

    # Part 2

    enhancements = [original_image]

    while True:
        try:
            final_img = enhancements[50]
            break
        except IndexError:
            enhancements.append(enhancements[-1].enhance())

    if final_img.default == LIGHT_PIXEL:
        raise RuntimeError(f"The answer will be infinite")

    Part_2_Answer = sum(final_img.mapOnPixels(lambda x: 1 if x == LIGHT_PIXEL else 0))

    return (Part_1_Answer, Part_2_Answer)
