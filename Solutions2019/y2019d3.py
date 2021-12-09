
def isVertical(segment):
    return segment.start[0] == segment.end[0]

def isHorizontal(segment):
    return segment.start[1] == segment.end[1]

def getSegmentCollision(Seg1, Seg2):
    if(isVertical(Seg1) and isHorizontal(Seg2)):
        #calculate the intersection
        if(Seg2.start[0] <= Seg1.start[0] and Seg2.end[0] >= Seg1.start[0]) and (Seg1.start[1] >= Seg2.start[1] and Seg1.end[1] <= Seg2.start[1]):
            return (Seg1.start[0], Seg2.start[1])
    elif(isVertical(Seg1) and isVertical(Seg2)):
        #calculate the intersection
        if(Seg1.start[0] == Seg2.start[0]):
            #share the x coordinate
            if(Seg1.start[0] <= Seg2.start[0] and Seg1.end[0] >= Seg2.start[0]):
                #there is some overlapping region
                print("Need to finish horizontal region overlap checking")
            elif(Seg1.start[0] <= Seg2.end[0] and Seg1.end[0] >= Seg2.end[0]):
                #there is some overlapping region
                print("Need to finish horizontal region overlap checking")
            else:
                #there is no overlapping region
                return None
    elif(isHorizontal(Seg1) and isHorizontal(Seg2)):
        if(Seg1.start[1] == Seg2.start[1]):
            #segments share the y coordinate
            #can do this by converting to vertical then checking that way
            #return getSegmentCollision(rotate90(Seg1), rotate90(Seg2))
            print("Not fully implemented horizontal segment collision")
    elif(isHorizontal(Seg1) and isVertical(Seg2)):
        return getSegmentCollision(Seg2, Seg1)
    else:
        print("Found one or more non-proper segments")
    return None
    

class Segment:
    def __init__(self, startPair, endPair):
        #can assume the the start is above/left of the ending point
        if(startPair[0] > endPair[0]):
            self.start = endPair
            self.end = startPair
        elif(endPair[1] > startPair[1]):
            self.start = endPair
            self.end = startPair
        else:
            self.start = startPair
            self.end = endPair
        self.actualStart = startPair
    #TODO - overload getting by []

def manhattanDistance(pair1, pair2):
    return abs(pair1[0]-pair2[0]) + abs(pair1[1]-pair2[1])

def y2019d3(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2019/d3.txt"
    print("2019 day 3:")

    with open(inputPath) as f:
        myStr = f.readline()
        myStr = myStr.strip()
        myStr += ", "
        #split on commas
        wirePath = []
        while(myStr.find(",") > 0):
            commaIndex = myStr.find(",")
            wirePath.append(myStr[0:commaIndex])
            myStr = myStr[commaIndex+1:]
        
        segmentList = []

        #now process
        nowX = 0
        nowY = 0
        for movement in wirePath:
            instr = movement[0:1]
            amount = int(movement[1:])

            start = (nowX, nowY)

            if(instr == 'R'):
                nowX += amount
            elif(instr == 'L'):
                nowX -= amount
            elif(instr == 'U'):
                nowY += amount
            else:
                nowY -= amount
            
            end = (nowX, nowY)
            segmentList.append(Segment(start, end))
    
        myStr2 = f.readline()
        myStr2 = myStr2.strip()
        myStr2 += ", "
        
        #now parse the second wire
        wirePath = []
        while(myStr2.find(",") > 0):
            commaIndex = myStr2.find(",")
            wirePath.append(myStr2[0:commaIndex])
            myStr2 = myStr2[commaIndex+1:]

        #and process
        nowX = 0
        nowY = 0
        closestIntersection = float("inf")
        closestIntersectionLocation = None

        #part 2
        closestStepIntersection = float("inf")
        netPathDistance = 0 #total distance by wire two

        for movement in wirePath:
            instr = movement[0:1]
            amount = int(movement[1:])

            start = (nowX, nowY)

            if(instr == 'R'):
                nowX += amount
            elif(instr == 'L'):
                nowX -= amount
            elif(instr == 'U'):
                nowY += amount
            else:
                nowY -= amount
            
            end = (nowX, nowY)

            sTemp = Segment(start, end)

            for segment in segmentList:
                res = getSegmentCollision(segment, sTemp)
                if(res != None):
                    distance = manhattanDistance(res, (0,0))
                    if(distance == 0):
                        continue
                    elif distance < closestIntersection:
                        closestIntersection = distance
                        closestIntersectionLocation = res

            #part 2 loop
            pathLength = 0
            for segment in segmentList:
                res = getSegmentCollision(segment, sTemp)
                if(res != None):
                    if(res[0] == 0 and res[1] == 0):
                        pathLength += manhattanDistance(segment.start, segment.end)
                        continue
                    
                    thisDistance = manhattanDistance(start, res) + netPathDistance #for wire two
                    thisDistance += manhattanDistance(segment.actualStart, res) + pathLength #for wire one
                
                    if(thisDistance < closestStepIntersection):
                        closestStepIntersection = thisDistance
                        #break #cant do better than this

                pathLength += manhattanDistance(segment.start, segment.end)

            netPathDistance += amount
    
    print("The closest intersection (part 1) is at distance "+ str(closestIntersection))
    print("The closest path intersection (part 2) is at distance "+ str(closestStepIntersection))
    print("===========")

    return (closestIntersection, closestStepIntersection)


#84 is not correct