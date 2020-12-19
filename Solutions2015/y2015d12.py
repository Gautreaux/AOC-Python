# from AOC_Lib.name import *

import json
from os.path import pardir

def sumNumbers(obj, ignoreProperty = None):
    sum = 0
    if type(obj) == dict:
        for k in obj:
            if ignoreProperty != None and obj[k] == ignoreProperty:
                return 0
            sum += sumNumbers(obj[k], ignoreProperty)
    elif type(obj) == list:
        for e in obj:
            sum += sumNumbers(e, ignoreProperty)
    elif type(obj) == int:
        sum += obj
    elif type(obj) == str:
        pass
    else:
        print(f"Unsupported json type: {type(obj)}")
        print(obj)
        raise TypeError(type(obj))
    return sum


def y2015d12(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d12.txt"
    print("2015 day 12:")

    Part_1_Answer = None
    Part_2_Answer = None

    with open(inputPath) as f:
        j = json.load(f)
    
    #print(j)

    Part_1_Answer = sumNumbers(j)
    Part_2_Answer = sumNumbers(j, "red")

    return (Part_1_Answer, Part_2_Answer)