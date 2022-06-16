
from multiprocessing import Pool

from AOC_Lib.HexGrid import (
    GRID_VERTICAL, 
    GRID_HORIZONTAL,
    HEX_TRANSFORMS, 
    HEX_STEP_TRANSLATIONS, 
    computeHexDistance, 
    inferGridOrientation,
    manhattanHexDist,
)

def _f_vert(pos):
    return computeHexDistance(pos, GRID_VERTICAL)

def _f_horiz(pos):
    return computeHexDistance(pos, GRID_HORIZONTAL)

def y2017d11(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d11.txt"
    print("2017 day 11:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    hex_grid_type = inferGridOrientation(lineList[0].split(","))
    pos = (0,0)

    all_pos = set()

    assert(len(lineList) == 1) 
    for c in lineList[0].split(","):
        step_type = HEX_STEP_TRANSLATIONS[c]
        step_transform = HEX_TRANSFORMS[step_type]
        pos = (pos[0]+step_transform[0], pos[1]+step_transform[1])
        all_pos.add(pos)
    
    print("Ending pos is: {}, Grid type is: {}".format(
        pos, 'Vertical' if hex_grid_type == GRID_VERTICAL else 'Horizontal'
    ))

    Part_1_Answer = computeHexDistance(pos, hex_grid_type)


    print(f"There are {len(all_pos)} total unique positions")

    # Part_2_Answer = max(map(lambda x: computeHexDistance(x, hex_grid_type), filtered))
    
    # The lazy man's optimization
    with Pool() as p:
        if hex_grid_type == GRID_VERTICAL:
            Part_2_Answer = max(p.map(_f_vert, all_pos))
        else:
            Part_2_Answer = max(p.map(_f_horiz, all_pos))

    return (Part_1_Answer, Part_2_Answer)