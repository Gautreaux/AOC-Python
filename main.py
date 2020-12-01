
from argparse import ArgumentParser
from importlib import import_module
from inspect import getmembers

from Templates.templateConverter import convertTemplate
from Util.Util import *
from Util.FileUtil import allFilesInDirByType

def runAll():
    '''Run over all days'''
    raise NotImplementedError

#TODO - add extra parameter(s) for more arguments to the day
#TODO - make this ^ a command line argument
def runDay(dateCode:str):
    '''Return answer for a specific day in 'y<year>d<day>' format.'''

    if isValidDateCode(dateCode) is False:
        raise ValueError(f"Could not resolve the date code {dateCode}")

    (y, d) = splitDateCode(dateCode)

    #check if a solution is present,
    dir = f"Solutions{y}"
    if f"{dir}/{dateCode}.py" not in allFilesInDirByType(dir, '.py'):
        # a solution is not present so we generate a new one
        generateBaseSolution(dateCode)
    
    # a solution is present, now we need to check if function is inside it
    try:
        module = import_module(f"Solutions{y}.{dateCode}")
    except Exception as e:
        print(f"For dateCode {dateCode}, the file was found, but the function was missing.")
        raise e

    # we know the module exists, we just need to find its pointer in the module
    l = getmembers(module)
    for e in l:
        if e[0] == dateCode:
            return e[1]()

    raise ValueError(f"For dateCode {dateCode}: The module imported correctly, but function not found")

def generateBaseSolution(dateCode:str):
    '''Generate a new solution for the provided date code'''
    print(f"Generating new template file for the provided datecode {dateCode}")
    convertTemplate(dateCode)


if __name__ == "__main__":
    parser = ArgumentParser(description="Run an advent of code trial(s). Runs the most recent day unless otherwise specified.")
    parser.add_argument('-a', action='store_true', help=runAll.__doc__)
    parser.add_argument('-d', nargs=1, help=runDay.__doc__)

    args = parser.parse_args()

    if args.a is True:
        runAll()
        
    if args.d is not None:
        dateCode = args.d[0]
        (part1Answer, part2Answer) = runDay(dateCode)
    else:
        dateCode = getLastDateCode()
        print(f"Last dateCode resolved to {dateCode}")
        (part1Answer, part2Answer) = runDay(dateCode)
    
    print(f"For day {dateCode}:")
    print(f"Part 1: {part1Answer}")
    print(f"Part 2: {part2Answer}")