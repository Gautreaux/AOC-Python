from collections import defaultdict
from dataclasses import dataclass, field
import functools
import itertools
from typing import Optional


from AOC_Lib.SolutionBase import SolutionBase, Answer_T


@dataclass
class File:
    name: str
    size: int
    parent: "Directory"


@dataclass
class Directory:
    name: str
    files: list[File] = field(default_factory=list, hash=False, compare=False)
    directories: list["Directory"] = field(
        default_factory=list, hash=False, compare=False
    )
    parent: Optional["Directory"] = field(default=None, hash=False, compare=False)

    _size: int = field(default=0, init=False)

    def add_sub_dir(self, name: str) -> "Directory":

        for d in self.directories:
            if d.name == name:
                return d

        new_dir = Directory(name, parent=self)
        self.directories.append(new_dir)
        return new_dir

    def add_file(self, name: str, size: int) -> File:
        for f in self.files:
            if f.name == name:
                return f
        new_file = File(name, size, self)
        self.files.append(new_file)
        return new_file

    @property
    def size(self):
        if self._size:
            return self._size
        self._size = sum(
            map(lambda x: x.size, itertools.chain(self.files, self.directories))
        )  # type: ignore
        return self._size

    def iter_dirs(self):
        yield self
        for d in self.directories:
            for dd in d.iter_dirs():
                yield dd


class Solution_2022_07(SolutionBase):
    """https://adventofcode.com/2022/day/7"""

    def __post_init__(self):
        """Runs Once After `__init__`"""

        root = Directory("/")
        active_dir: Directory = root

        for line in self.input_str_list(include_empty_lines=False):
            if line.startswith("$ ls"):
                continue
            elif line.startswith("$ cd"):
                _, __, tail = line.rpartition(" ")

                if tail == "..":
                    assert active_dir.parent is not None
                    active_dir = active_dir.parent
                elif tail == "/":
                    pass
                else:
                    active_dir = active_dir.add_sub_dir(tail)
            elif line.startswith("dir"):
                _, name = line.split(" ")
                active_dir.add_sub_dir(name)
            else:
                file_sz, file_name = line.split(" ")
                active_dir.add_file(file_name, int(file_sz))

        self.root = root

    def _part_1_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_1_answer`"""

        return sum(
            filter(lambda x: x <= 100000, map(lambda x: x.size, self.root.iter_dirs()))
        )

    def _part_2_hook(self) -> Optional[Answer_T]:
        """Called once and return value is taken as `part_2_answer`"""

        TOTAL_SPACE_AVAILABLE = 70000000
        TOTAL_SPACE_NEEDED = 30000000

        total_used = self.root.size
        free_space = TOTAL_SPACE_AVAILABLE - total_used

        assert total_used < TOTAL_SPACE_AVAILABLE

        space_to_free = TOTAL_SPACE_NEEDED - free_space

        best_guess: Directory = self.root
        amount_freed: int = self.root.size

        for d in self.root.iter_dirs():
            if d.size < space_to_free:
                continue
            if d.size < amount_freed:
                best_guess = d
                amount_freed = d.size
        return amount_freed
