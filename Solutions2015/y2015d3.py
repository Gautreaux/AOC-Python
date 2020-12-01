from AOC_Lib.boundedInt import BoundedInt
from AOC_Lib.point import Point2

# sample variant for single line inputs
def y2015d3(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d3.txt"
    print("2015 day 3:")

    Part_1_Answer = None
    Part_2_Answer = None

    with open(inputPath) as f:
        line = f.readline().strip()

    transforms = {  '^' : Point2( 0,  1),
                    'v' : Point2( 0, -1),
                    '>' : Point2( 1,  0),
                    '<' : Point2(-1,  0)}

    posSet = set()
    currentPoint = Point2(0,0)
    posSet.add(currentPoint)

    for c in line:
        # move
        currentPoint += transforms[c]

        if currentPoint not in posSet:
            posSet.add(currentPoint)

    Part_1_Answer = len(posSet)

    pt2Set = set()
    currentPoints = [Point2(0,0), Point2(0,0)]
    pt2Set.add(currentPoints[0])
    parity = BoundedInt(2)

    for c in line:
        currentPoints[parity.asInt()] += transforms[c]

        if currentPoints[parity.asInt()] not in pt2Set:
            pt2Set.add(currentPoints[parity.asInt()])
        
        parity += 1

    Part_2_Answer = len(pt2Set)

    return (Part_1_Answer, Part_2_Answer)

# TODO - include variant with auto pattern detection