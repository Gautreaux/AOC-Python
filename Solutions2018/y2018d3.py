# from AOC_Lib.name import *

from collections import Counter, namedtuple
import itertools
from typing import Generator

Claim_T = namedtuple("Claim_T", "claim_id up_left width height")

def generateClaimedSquares(claim: Claim_T) -> Generator[tuple[int, int], None, None]:
    """Generate all the points inside the claim"""
    for y_offset in range(claim.height):
        for x_offset in range(claim.width):
            yield (
                claim.up_left[0] + x_offset,
                claim.up_left[1] + y_offset,
            )


def y2018d3(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2018/d3.txt"
    print("2018 day 3:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    claims = []

    for line in lineList:
        clam_id, _, ul, hw = line.split(" ")
        
        clam_id = int(clam_id[1:])
        ul = tuple(map(int, ul[:-1].split(",")))
        hw = tuple(map(int, hw.split("x")))

        claims.append(Claim_T(clam_id, ul, hw[0], hw[1]))

    all_claimed_squares_generator = itertools.chain.from_iterable(map(generateClaimedSquares, claims))

    claims_count = Counter(all_claimed_squares_generator)

    Part_1_Answer = sum(1 for c in claims_count.values() if c >= 2)

    for c in claims:
        has_overlapping = False
        for p in generateClaimedSquares(c):
            if claims_count[p] >= 2:
                has_overlapping = True
                break
        
        if has_overlapping:
            continue
        else:
            # check that there is exactly one answer
            assert(Part_2_Answer == None)
            Part_2_Answer = c.claim_id
            # continue     

    return (Part_1_Answer, Part_2_Answer)