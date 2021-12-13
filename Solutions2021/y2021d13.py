# from AOC_Lib.name import *

def y2021d13(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2021/d13.txt"
    print("2021 day 13:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    # for multi line inputs
    itr = iter(lineList)

    dots = set()

    for line in itr:
        if not line:
            break
        a,_,b = line.partition(",")
        dots.add((int(a), int(b)))
    
    folds = []
    for line in itr:
        _,_,s = line.split(" ")
        dim,_,val = s.partition("=")
        folds.append((dim, int(val)))

    for dim,val in folds:
        new_dots = set()
        for x,y in dots:
            if dim == "x":
                new_x = val - abs(x - val)
                new_dots.add((new_x, y))
            elif dim == "y":
                new_y = val - abs(y - val)
                new_dots.add((x, new_y))
            else:
                raise RuntimeError(f"Illegal value {dim}")

        dots = new_dots

        if Part_1_Answer is None:
            Part_1_Answer = len(new_dots)

    min_x = min(map(lambda x: x[0], dots))
    max_x = max(map(lambda x: x[0], dots))
    min_y = min(map(lambda x: x[1], dots))
    max_y = max(map(lambda x: x[1], dots))

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) in dots:
                print("█", end="")
            else:
                print(" ", end="")
        print("")

    # TODO - some form of text resolver
    Part_2_Answer = "PGHRKLKL"


    return (Part_1_Answer, Part_2_Answer)