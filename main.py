
from argparse import ArgumentParser
from importlib import import_module
from inspect import getmembers
from os import path, remove
from typing import Any

from inputDownloader import getInputForDateCode
from Templates.templateConverter import convertTemplate
from Util.Util import *
from Util.FileUtil import allFilesInDirByType
from Util.IntelliParseTesting import testAllIntelliParse

class FunctionImportError(RuntimeError):
    pass

#TODO - add extra parameter(s) for more arguments to the day
#TODO - make this ^ a command line argument
def runDay(dateCode:str, genTemplateIfNotPresent=True) -> Tuple[Any, Any]:
    '''Return answer for a specific day in 'y<year>d<day>' format.'''

    if isValidDateCode(dateCode) is False:
        raise ValueError(f"Could not resolve the date code {dateCode}")

    (y, d) = splitDateCode(dateCode)

    #check if a solution is present,
    dir = f"Solutions{y}"
    if f"{dir}/{dateCode}.py" not in allFilesInDirByType(dir, '.py'):
        if genTemplateIfNotPresent is True:
            # a solution is not present so we generate a new one
            generateBaseSolution(dateCode)
        else:
            raise FileNotFoundError(f"DateCode {dateCode} not solved and template generation is false")
    
    # a solution is present, now we need to check if function is inside it
    try:
        module = import_module(f"Solutions{y}.{dateCode}")
    except Exception as e:
        raise FunctionImportError(f"For dateCode {dateCode}, the file was found, but the function was missing.")

    # we know the module exists, we just need to find its pointer in the module
    l = getmembers(module)
    for e in l:
        if e[0] == dateCode:
            return e[1]()

    # should be unreachable
    raise FunctionImportError(f"For dateCode {dateCode}: The module imported correctly, but function not found")

def generateBaseSolution(dateCode:str):
    '''Generate a new solution for the provided date code'''
    print(f"Downloading input for datecode {dateCode}")
    if getInputForDateCode(dateCode) is False:
        print(f"Something went wrong downloading the input file")
    print(f"Generating new template file for the provided datecode {dateCode}")
    convertTemplate(dateCode)

def testDownload():
    '''Test the input downloading behavior'''
    print("Testing downloader for ", end="")
    print(getDateCodeAsURL(getLastDateCode()))
    savePath = "testDownload.txt"
    v = getInputForDateCode(getLastDateCode(), savePath)

    if v is True:
        print("Downloader working")
    else:
        print("Downloader failed")
    
    if path.exists(savePath):
        remove(savePath)


if __name__ == "__main__":
    parser = ArgumentParser(description="Run an advent of code trial(s). Runs the most recent day unless otherwise specified.")
    # parser.add_argument('-a', action='store_true', help=runAll.__doc__)
    parser.add_argument('-d', nargs=1, help=runDay.__doc__)
    parser.add_argument('-p', action='store_true', help=testAllIntelliParse.__doc__)
    parser.add_argument('-t', action='store_true', help=testDownload.__doc__)
    parser.add_argument('-r', action='store_true', help="run the readme formatter")

    args = parser.parse_args()
     
    # elif args.p is not None:
    #     testAllIntelliParse()
    if args.t is True:
        testDownload()
    if args.r is True:
        from readmeFormatter import formatReadme
        formatReadme()
    else: # a particular day
        if args.d is not None:
            dateCode = args.d[0]
            assert(isValidDateCode(dateCode))
            (part1Answer, part2Answer) = runDay(dateCode)
        else:
            dateCode = getLastDateCode()
            dateCode = "y2020d20"
            print(f"Last dateCode resolved to {dateCode}")
            (part1Answer, part2Answer) = runDay(dateCode)
        
        print(f"Answer for day {dateCode}:")
        print(f"Part 1: {part1Answer}")
        print(f"Part 2: {part2Answer}")

        # print(str(type(part1Answer)))
        # print(str(type(part2Answer)))