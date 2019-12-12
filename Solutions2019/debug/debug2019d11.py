


def __reHash(xValue, yValue):
    return hash((xValue, yValue))

def validateVisitList(visitList, checkRehash = True):
    #params - check rehash controls if the rehash should be done
    #   this may require re-implementing how the rehash is computed
    #returns
    #   true - all checks passed
    #   false - some checks failed
    #       in this case, some information may be printed to the console

    try:
        print("Validating the visit list of length: " + str(len(visitList)))

        rehashError = 0 #track the number of rehashErrors
        hashCollisionErrors = 0 #track the number of hashes that are assigned to multiple values
        hashDuplicationErrors = 0 #track hte number of items that hash into two distinct values

        hashMap = {}

        for element in visitList:
            #check the hashes directly
            elementPair = (element[0], element[1])

            if(checkRehash and __reHash(element[0], element[1]) != element[2]):
                rehashError += 1
                if(rehashError < 10):
                    print("Rehash failed for " + str(elementPair) + ". Provided hash: " + str(element[2]) + ". Rehash value: " + str(__reHash(element[0], element[1])))
                    if(rehashError == 9):
                        print("\t>=10 rehash errors occurred, no more will be printed.")

            #check that each hash has exactly one xy pair mapped to it
            #check the x,y values for a hash colision
            if(element[2] not in hashMap):
                hashMap[element[2]] = elementPair
            else:
                thisPair = hashMap[element[2]]
                if(thisPair == elementPair):
                    pass
                else:
                    hashCollisionErrors+=1
                    if(hashCollisionErrors < 10):
                        print("Hash collision occurred on hash value " + str(element[2]) + ". FirstHash: "+str(thisPair) + ". ThisHash: "+str(elementPair))
                        if(hashCollisionErrors == 9):
                            print("\t>=10 hash collision errors occurred, no more will be printed.")


            #another check - verify that each x,y hashes to the same value
            yDict = {} #map x,y pairs to their hashed 
            xValue = element[0]
            yValue = element[1]

            if(yValue not in yDict):
                yDict[yValue] = {}
            
            if(xValue not in yDict[yValue]):
                yDict[yValue][xValue] = element[2]
            else:
                thisHash = yDict[yValue][xValue]
                if(thisHash == element[2]):
                    pass
                else:
                    hashDuplicationErrors+=1
                    if(hashDuplicationErrors < 10):
                        print("Hash duplication error occurred on point " + str(elementPair) + ". Original Value: " + thisHash + ". This Value: " + element[2])
                        if(hashDuplicationErrors == 9):
                            print("\t>=10 hash duplication errors occurred, no more will be printed.")
            

        if(rehashError+hashCollisionErrors+hashDuplicationErrors == 0):
            return True
        else:
            print("Validation summary:")
            if(checkRehash):
                print("\tTotal Rehash Errors: " + str(rehashError))
            print("\tTotal Hash Collision Errors: " + str(hashCollisionErrors))
            print("\tTotal Hash Duplication Errors: " + str(hashDuplicationErrors))


    except Exception as e:
        print("While validating the visit list, and exception occurred: " + str(e))
    
    return False