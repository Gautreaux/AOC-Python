# from AOC_Lib.name import *

def y2017d19(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2017/d19.txt"
    print("2017 day 19:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)
    
    # find the entry point
    start_x = None
    for start_x, c in enumerate(lineList[0]):
        if c == '|':
            break
    
    current_x = start_x
    current_y = 0
    current_transform = (0,1)

    letters = []

    # This is probably all gabage

    while True:
        assert(current_x >= 0)
        assert(current_y >= 0)
        current = lineList[current_y][current_x]

        if current == ' ':
            # off the path, terminate
            break
        elif (ord(current) >= ord('A')) and (ord(current) <= ord('Z')):
            # this is a letter
            letters.append(current)
        elif current == "+":
            # this is a turn
            if current_transform[0] == 0:
                # the new must be an x
                candidate_transforms = [(1,0),(-1,0)]
            else:
                # the new must be a y:
                candidate_transforms = [(0,1),(0,-1)]
            new_transform = False
            for c_x,c_y in candidate_transforms:
                n_x = current_x + c_x
                n_y = current_y + c_y
                if n_x < 0 or n_y  < 0:
                    continue
                if n_y >= len(lineList):
                    continue
                if n_x >= len(lineList[n_y]):
                    continue
                if lineList[n_y][n_x] == " ":
                    continue
                current_transform = (c_x, c_y)
                new_transform = True
                break
            if new_transform == False:
                raise RuntimeError("Could not resolve the new transform direction")
        elif current == "-" or current == "|":
            pass
        else:
            raise RuntimeError("Something weird happened: `{}`".format(current))
        current_x += current_transform[0]
        current_y += current_transform[1]

    assert(len(letters) > 0)
    Part_1_Answer = "".join(letters)

    return (Part_1_Answer, Part_2_Answer)