# from AOC_Lib.name import *


import itertools
from math import isqrt
from typing import Any, Callable, Generator, Iterable, Iterator, Optional

from functools import cached_property


def isPerfectSquare(i: int) -> bool:
    """Return `True` iff a number is a perfect square"""
    return i == (isqrt(i)**2)


class EnhanceTransform:

    def __init__(self, start: str, result:str) -> None:
        self._start: str = start
        self._result: str = result

        l = sum(1 for c in self._start if c != "/")
        assert(l == 4 or l == 9)
        self._sz = (2 if l == 4 else 3)
        self._lines = self.start.split("/")
        assert(len(self._lines) == self._sz)
        assert(all(map(lambda x: self._sz == len(x), self._lines)))
    
    @property
    def size(self) -> int:
        """Return the dimensionality of this square"""
        return self._sz
    
    @property
    def start(self) -> str:
        """Return the starting condition"""
        return self._start

    @property
    def result(self) -> str:
        """Return the resulting condition"""
        return self._result

    @cached_property
    def num_set_in_start(self) -> int:
        """Return the number of pixels that are set in start"""
        return sum(1 for c in self.start if c == "#")
        
    @classmethod
    def _do_rotate_90(cls, s:str, sz:int) -> str:
        """Rotate the input `tile` by 90 degrees clockwise and return"""
        if sz == 2:
            return "".join([s[3], s[0], '/', s[4], s[1]])
        elif sz == 3:
            return "".join([s[8], s[4], s[0], '/', s[9], s[5], s[1], '/', s[10], s[6], s[2]])
        else:
            raise NotImplementedError(f"Unsupported size: {sz}")

    @cached_property
    def start_horiz_flip(self) -> str:
        """Return the horizontal flip of the starting condition"""
        return "/".join(map(lambda x: "".join(reversed(x)), self._lines))
    
    @cached_property
    def start_vert_flip(self) -> str:
        """Return the vertical flip of the starting condition"""
        return "/".join(iter(reversed(self._lines)))
    
    @cached_property
    def start_rotate_90(self) -> str:
        """Return the 90 degree rotation of the starting condition"""
        return self._do_rotate_90(self.start, self._sz)
    
    @cached_property
    def start_rotate_180(self) -> str:
        """Return the 180 degree rotation of the starting condition"""
        return self._do_rotate_90(self.start_rotate_90, self._sz)
    
    @cached_property
    def start_rotate_270(self) -> str:
        """Return the 270 degree rotation of the starting condition"""
        return self._do_rotate_90(self.start_rotate_180, self._sz)

    @cached_property
    def start_flip_h_rot_90(self) -> str:
        """Return the horizontal flip rotated again"""
        return self._do_rotate_90(self.start_horiz_flip, self._sz)
    
    @cached_property
    def start_flip_v_rot_90(self) -> str:
        """Return the vertical flip rotated again"""
        return self._do_rotate_90(self.start_vert_flip, self._sz)

    def generateAllStartTransforms(self) -> Generator[str, None, None]:
        """Return a generator of all start permutations"""
        yield self.start
        yield self.start_horiz_flip
        yield self.start_vert_flip
        yield self.start_rotate_90
        yield self.start_rotate_180
        yield self.start_rotate_270
        yield self.start_flip_h_rot_90
        yield self.start_flip_v_rot_90


class EnhancedImage():
    def __init__(self, 
        transforms: Optional[list[EnhanceTransform]]=None, 
        pattern: Optional[Iterable[str]]=None,
        cache: Optional[dict[str, str]]=None,
    ) -> None:
        if transforms is None:
            self.two_transforms = []
            self.thr_transforms = []
        else:
            assert(all(map(lambda x: x.size in [2,3], transforms)))
            self.two_transforms = list(filter(lambda x: x.size == 2, transforms))
            self.thr_transforms = list(filter(lambda x: x.size == 3, transforms))
        
        if cache is not None:
            self.cache = cache
        else:
            self.cache = {}

        if pattern is not None:
            self.pattern = str(pattern)
            self.size = sum(1 for _ in itertools.takewhile(lambda x: x != '/', pattern))
        else:
            self.pattern = ".#./..#/###"
            self.size = 3

    @classmethod
    def fromLines(cls, lines: list[str], pattern: str = None) -> 'EnhancedImage':
        """Construct an `EnhancedImage` from lines"""
        all_transforms = list(map(lambda x: EnhanceTransform(*x.split(" => ")), lines))
        e = cls(transforms=all_transforms, pattern=pattern)
        return e

    def iterPixels(self) -> Iterator[str]:
        """Return an iterator over all pixels"""
        return filter(lambda x: x!= '/', iter(self.pattern))

    def mapOntoPixels(self, callable: Callable[[str], Any]) -> Iterator[Any]:
        """Apply callable to each pixel"""
        return map(callable, self.iterPixels())

    def generateTiles(self) -> Generator[str, None, None]:
        """Return a Generator of sub tiles that cover the image"""
        if self.size % 2 == 0:
            dim_sz = 2
        elif self.size % 3 == 0:
            dim_sz = 3
        else:
            raise RuntimeError(f"The size {self.size} is not a multiple of 2 or 3")
        
        # number of rows of tiles
        #   coincidentally, also number of rows of columns
        n_tile_rows = self.size // dim_sz
        n_tile_cols = n_tile_rows

        i = iter(self.pattern)

        for _ in range(n_tile_rows):
            # split into rows
            token_queues = []
            
            for _ in range(dim_sz):
                q = list(itertools.takewhile(lambda x: x != '/', i))
                token_queues.append(iter(q))
            
            for _ in range(n_tile_cols):
                # now represent the tile
                tile = "/".join(
                    map(
                        lambda q: "".join(itertools.islice(q, dim_sz)), 
                        token_queues
                    )
                )
                yield tile

    @classmethod
    def fromTiles_Class(cls, tiles: Iterable[Iterator[str]]) -> 'EnhancedImage':
        """Build an image from tiles
            Approximately the inverse of `generateTiles()`

            Invoked in the class context; does not populate transforms or cache on sub object
        """
        tiles = list(tiles)
        
        if not isPerfectSquare(len(tiles)):
            raise RuntimeError(f"Cannot build a new tile, there were `{len(tiles)}` and this is not a perfect square")

        n_tile_rows = isqrt(len(tiles))
        n_tile_cols = n_tile_rows

        print("Starting recombine with {} tiles in a {}x{} grid".format(
            len(tiles), n_tile_rows, n_tile_cols,
        ))

        pattern_lines = []
        i = iter(tiles)

        for _ in range(n_tile_rows):
            rows = []

            for tile in itertools.islice(i, n_tile_cols):
                j = iter(tile)
                for sub_row_i in itertools.count(0):
                    while len(rows) <= sub_row_i:
                        rows.append([])
                    ol = len(rows[sub_row_i])
                    rows[sub_row_i].extend(itertools.takewhile(lambda x: x != '/', j))
                    nl = len(rows[sub_row_i])
                    if ol == nl:
                        break
            while not rows[-1]:
                rows.pop()

            for r in rows:
                if len(pattern_lines):
                    pattern_lines.append("/")                 
                pattern_lines.append(r)

        # print(pattern_lines)
        pattern = "".join(itertools.chain.from_iterable(pattern_lines))
        new_img = cls(pattern=pattern)
        return new_img

    def fromTiles(self, tiles: Iterable[Iterator[str]]) -> 'EnhancedImage':
        """Build an image from tiles
            Approximately the inverse of `generateTiles()`

            Will populate cache and transforms of new object with those in the calling object
        """
        new_img = self.fromTiles_Class(tiles)
        new_img.cache = self.cache
        new_img.two_transforms = self.two_transforms
        new_img.thr_transforms = self.thr_transforms
        return new_img
                
    def enhance(self) -> 'EnhancedImage':
        """Run the enhance process and return the new image"""
        tiles = self.generateTiles()
        enhanced_tiles = map(self.enhanceTile, tiles)
        new_img = self.fromTiles(enhanced_tiles)
        return new_img

    def _enhanceTile_Worker(self, tile: str):
        """Enhance a single tile and return the result"""

        if self.size % 2 == 0:
            candidate_transforms: list[EnhanceTransform] = self.two_transforms
        elif self.size % 3 == 0:
            candidate_transforms: list[EnhanceTransform] = self.thr_transforms

        num_set = sum(1 for c in tile if c == "#")
        filtered_transforms = filter(lambda x: x.num_set_in_start == num_set, candidate_transforms)

        for ct in filtered_transforms:
            for opt in ct.generateAllStartTransforms():
                if opt == tile:
                    return ct.result
        
        raise RuntimeError(f"Could not find a transform for: {tile}")

    def enhanceTile(self, tile: str):
        """Enhance a single tile and return the result"""
        
        if tile in self.cache:
            return self.cache[tile]
        else:
            t = self._enhanceTile_Worker(tile)
            self.cache[tile] = t
            return t


def y2017d21_tests() -> None:
    """Test utilities"""

    s = ".#./..#/###"
    ei = EnhancedImage(pattern=s)
    assert(ei.size == 3)
    tiles = list(ei.generateTiles())
    assert(len(tiles) == 1)
    assert(tiles[0] == s)
    r = EnhancedImage.fromTiles_Class(tiles)
    print(r.pattern)
    assert(r.pattern == s)

    s = "#..#/..../..../#..#"
    ei = EnhancedImage(pattern=s)
    assert(ei.size == 4)
    tiles = list(ei.generateTiles())
    assert(len(tiles) == 4)
    assert(set(tiles) == set([
        "#./..", ".#/..", "../#.", "../.#",
    ]))
    r = EnhancedImage.fromTiles_Class(tiles)
    assert(r.pattern == s)  


def y2017d21(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d21.txt"
    print("2017 day 21:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    y2017d21_tests()
    print(f"Tests passing")

    base_img = EnhancedImage.fromLines(lineList)

    # mapping of index to number of rounds of enhance
    all_imgs: list[EnhancedImage] = [base_img]

    while True:
        try:
            a = all_imgs[18]
            break
        except IndexError:
            print(f"Enhancing, total rounds prior =", len(all_imgs))
            all_imgs.append(all_imgs[-1].enhance())
            continue
    
    Part_1_Answer = sum(all_imgs[5].mapOntoPixels(lambda x: 1 if x == '#' else 0))
    Part_2_Answer = sum(all_imgs[18].mapOntoPixels(lambda x: 1 if x == '#' else 0))

    return (Part_1_Answer, Part_2_Answer)