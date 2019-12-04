
def hasTwoAdjacent(intIn):
    i = str(intIn)

    for ii in range(0,len(i)-1):
        if(i[ii] == i[ii+1]):
            return True
    return False

def isIncreasing(intIn):
    i = str(intIn)

    for ii in range(0,len(i)-1):
        if(i[ii] > i[ii+1]):
            return False
    return True

def isValidValue(intIn):
    if(len(str(intIn)) != 6):
        return False
    #no need to check range
    if(not(hasTwoAdjacent(intIn))):
        return False
    return isIncreasing(intIn)

def y2019d4(inputStr = None):
    if(inputStr == None):
        inputStr = "272091-815432"
    print("2019 day 4:")

    inputStr = inputStr.strip()
    dash = inputStr.find("-")
    lb = int(inputStr[0:dash])
    ub = int(inputStr[dash+1:])

    i = lb
    validCount = 0
    while(i <= ub):
        if(isValidValue(i)):
            validCount+=1
        i+=1

    print("The valid count (part 1) is " + str(validCount))
    print("===========")