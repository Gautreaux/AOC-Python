
#return true iff the intIn has two, matching, adjacent characters
def hasTwoAdjacent(intIn):
    i = str(intIn)

    for ii in range(0,len(i)-1):
        if(i[ii] == i[ii+1]):
            return True
    return False

#return true iff the characters of the intIn are non-decreasing
def isIncreasing(intIn):
    i = str(intIn)

    for ii in range(0,len(i)-1):
        if(i[ii] > i[ii+1]):
            return False
    return True

#return true iff the int in is a valid (part 1) value
def isValidValue(intIn):
    if(len(str(intIn)) != 6):
        return False
    #no need to check range
    if(not(hasTwoAdjacent(intIn))):
        return False
    return isIncreasing(intIn)

#return true iff the int satisfies the part 2 constraint:
#there are a set of duplicate characters that are only 2 long
def meetsPart2(intIn):
    i = str(intIn)

    #check the middle portion for two characters meeting the criteria
    for ii in range(1, len(i)-2):
        if(i[ii] == i[ii+1] and i[ii] != i[ii-1] and i[ii] != i[ii+2]):
            return True
        
    #check the beginning to see if it satisfies
    if(i[0] == i[1] and i[0] != i[2]):
        return True
    
    #check the end part to see if it satisfies
    lastIndex = len(i)-1
    if(i[lastIndex-1] == i[lastIndex] and i[lastIndex-2] != i[lastIndex]):
        return True
    
    #no conditions could be meet, terminate
    return False

#return true iff the int meets the validation criteria for part 2
def isValidValue2(intIn):
    if(len(str(intIn)) != 6):
        return False
    #no need to check range
    if(not(hasTwoAdjacent(intIn))):
        return False
    if(not(meetsPart2(intIn))):
        return False
    return isIncreasing(intIn)

def y2019d4(inputStr = None):
    if(inputStr == None):
        inputStr = "272091-815432"
    print("2019 day 4:")

    #input handeling
    inputStr = inputStr.strip()
    dash = inputStr.find("-")
    lb = int(inputStr[0:dash])
    ub = int(inputStr[dash+1:])

    i = lb
    validCount = 0
    validCount2 = 0

    #loop over all values in the range
    while(i <= ub):
        if(isValidValue(i)):
            validCount+=1
        if(isValidValue2(i)):
            validCount2+=1
        i+=1

    print("The valid count (part 1) is " + str(validCount))
    print("The valid count (part 2) is " + str(validCount2))
    print("===========")

    #part 2 
    #353 not correct
    #808 not correct
    #829 not correct