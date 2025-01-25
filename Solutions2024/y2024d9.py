# from AOC_Lib.name import *
from dataclasses import dataclass, replace
from typing import Iterator
from collections import deque
from itertools import chain


@dataclass
class DiskBlock:
    block_id: int
    file_id: int


@dataclass
class DiskFile:
    file_id: int
    start_location: int
    blocks_len: int

    def generate_blocks(self) -> Iterator[DiskBlock]:
        for i in range(self.blocks_len):
            yield DiskBlock(self.start_location + i, self.file_id)

    @staticmethod
    def files_from_dense_map(densemap: str) -> 'list[DiskFile]':
        files: list[DiskFile] = []
        current_location: int = 0
        next_file_id: int = 0

        for i, c in enumerate(densemap):
            if i % 2 == 0:
                # this is a disk
                files.append(DiskFile(next_file_id, current_location, int(c)))
                next_file_id += 1
            else:
                # this is a free space
                current_location += files[-1].blocks_len + int(c)
        return files


def compact_files(files: list[DiskFile]) -> list[DiskBlock]:
    """Compact the files"""

    # should already be true, but good to check
    files = sorted(files, key=lambda f: f.start_location)

    blocks_to_place: deque[DiskBlock] = deque(
        chain.from_iterable(f.generate_blocks() for f in files)
    )

    placed: list[DiskBlock] = []

    while blocks_to_place:
        next_cell = len(placed)
        if blocks_to_place[0].block_id == next_cell:
            placed.append(blocks_to_place.popleft())
        else:
            back = blocks_to_place.pop()
            back.block_id = next_cell
            placed.append(back)

    return placed


def compact_files_smart(files: list[DiskFile]) -> list[DiskFile]:
    """Compact the files smarter"""
    # should already be true, but good to check
    to_move = sorted(files, key=lambda f: f.start_location)

    new_disk: list[DiskFile] = list(files)

    while to_move:
        assert len(new_disk) == len(files)
        current = to_move.pop()

        # Somehow caching this would help alot
        for i in range(len(new_disk) - 1):
            lower = new_disk[i]
            upper = new_disk[i + 1]

            assert lower.start_location < upper.start_location, f"{lower} {upper}"

            if lower.start_location >= current.start_location:
                # Already scanned to far, so nothing to do
                break

            free_space = upper.start_location - (
                lower.start_location + lower.blocks_len
            )

            if free_space >= current.blocks_len:
                # print(f'Moving {current} between {lower} and {upper}')
                new_new_disk = new_disk[: i + 1]
                new_new_disk.append(
                    replace(
                        current,
                        start_location=(lower.start_location + lower.blocks_len),
                    )
                )
                new_new_disk.extend(f for f in new_disk[i + 1 :] if f != current)
                new_disk = new_new_disk
                # print(new_disk)
                break

    # Should alredy be sorted
    new_disk.sort(key=lambda f: f.start_location)

    return new_disk


def calculate_checksum(disk: list[DiskBlock] | list[DiskFile]) -> int:
    """Calculate the checksum of the disk"""

    # Type hint that this has been coerced to DiskBlock
    disk_db: list[DiskBlock]

    if not disk:
        raise IndexError("Disk is empty")
    if isinstance(disk[0], DiskFile):
        disk_db = list(chain.from_iterable(f.generate_blocks() for f in disk)) # type: ignore
    else:
        disk_db = disk # type: ignore

    check_sum = 0
    for d in disk_db:
        check_sum += d.block_id * d.file_id
    return check_sum


def print_disk(disk: list[DiskBlock] | list[DiskFile]):
    """Print the disk block to the console"""
    if not disk:
        raise IndexError("Disk is empty")
    if isinstance(disk[0], DiskFile):
        disk = list(chain.from_iterable(f.generate_blocks() for f in disk))
    for d in disk:
        assert d.file_id < 10

    # Print the disk
    t = 0
    blk = 0
    while t < len(disk):
        if disk[t].block_id == blk:
            print(disk[t].file_id, end="")
            blk += 1
            t += 1
            continue
        elif disk[t].block_id < blk:
            try:
                assert False, "Blocks are out of order"
            except:
                print("\n\n\nDisk:", disk)
                raise
        else:
            print(".", end="")
            blk += 1


def _assert_sample_passes():
    sample_short = "12345"
    files_short = DiskFile.files_from_dense_map(sample_short)
    assert len(files_short) == 3
    assert files_short[0] == DiskFile(0, 0, 1)
    assert files_short[1] == DiskFile(1, 3, 3)
    assert files_short[2] == DiskFile(2, 10, 5)

    sample = "2333133121414131402"
    files = DiskFile.files_from_dense_map(sample)
    assert len(files) == 10
    disk = compact_files(files)
    checksum = calculate_checksum(disk)

    try:
        assert checksum == 1928, f"Checksum was {checksum}"
    except:
        print_disk(disk)
        raise

    disk_smart = compact_files_smart(files)
    checksum_smart = calculate_checksum(disk_smart)

    try:
        assert checksum_smart == 2858, f"Checksum was {checksum_smart}"
    except:
        print_disk(disk_smart)
        raise


def y2024d9(inputPath=None):
    if inputPath == None:
        inputPath = "Input2024/d9.txt"
    print("2024 day 9:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    _assert_sample_passes()

    files = DiskFile.files_from_dense_map(lineList[-1])

    disk = compact_files(files)
    disk_2 = compact_files_smart(files)

    Part_1_Answer = calculate_checksum(disk)  # 6378826667552
    Part_2_Answer = calculate_checksum(disk_2)

    return (Part_1_Answer, Part_2_Answer)
