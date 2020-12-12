
from argparse import ArgumentParser
from importlib import import_module
from inspect import getmembers
from os import path, remove

from inputDownloader import getInputForDateCode
from readmeFormatter import formatReadme
from solutionTesting import solutionDict
from Templates.templateConverter import convertTemplate
from Util.Util import *
from Util.FileUtil import allFilesInDirByType
from Util.IntelliParseTesting import testAllIntelliParse

class FunctionImportError(RuntimeError):
    pass

DAY_NOT_SOLVED = 1
GENERIC_ERROR = 2

#TODO - this still isnt working correctly
def runAll():
    '''Run over all days, print to console'''
    # TODO - multi process and/or cache results
    # ^ this is importante because some of these take a long flucking time

    yearsDict = {}

    for dateCode in genElapsedDateCodes():
        (y, d) = splitDateCode(dateCode)
        if y not in yearsDict:
            yearsDict[y] = {}
        if d in yearsDict[y]:
            raise ValueError(f"dateCode {dateCode} appeared twice in output")
        try:
            a = runDay(dateCode, False)
        except FunctionImportError:
            a = DAY_NOT_SOLVED
        except:
            a = GENERIC_ERROR
        yearsDict[y][d] = a

    # time to print and check

    #print headers:
    print("     | 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2")
    print("year | 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5")
    print("-----+--------------------------------------------------")

    years = list(yearsDict)
    years.sort()
    for year in years:
        print(f" {year} |", end="")
        assert(min(year) >= 1 and max(year) <= 25)
        for day in range(1,26):
            try:
                t = yearsDict[year][day]
            except KeyError:
                print(" ?", end="")
                continue
            if t == DAY_NOT_SOLVED:
                print(" -", end="")
            elif t == GENERIC_ERROR:
                print(" E", end="")
            else:
                # the solution actually completed
                # t = (part 1 answer, part 2 answer)
                dc = f"y{year}d{day}"
                if dc not in solutionDict:
                    print(" !", end="")
                    continue
                sol = solutionDict[dc]

                if sol == dc:
                    print(" *", end="")
                else:
                    print(" X", end="")
        print("") # newline

    print("Legend:")
    print("? - Unknown Error")
    print("- - Not yet solved")
    print("E - expection occurred in solution")
    print("! - Solution not provided in solution dict")
    print("* - all points earned")
    print("X - one or both answers do not match solution dict")

    raise NotImplementedError

#TODO - add extra parameter(s) for more arguments to the day
#TODO - make this ^ a command line argument
def runDay(dateCode:str, genTemplateIfNotPresent=True):
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
            raise FunctionImportError(f"DateCode {dateCode} not solved and template generation is false")
    
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
    parser.add_argument('-a', action='store_true', help=runAll.__doc__)
    parser.add_argument('-d', nargs=1, help=runDay.__doc__)
    parser.add_argument('-p', action='store_true', help=testAllIntelliParse.__doc__)
    parser.add_argument('-t', action='store_true', help=testDownload.__doc__)
    parser.add_argument('-r', action='store_true', help=formatReadme.__doc__)

    args = parser.parse_args()

    if args.a is True:
        runAll()        
    # elif args.p is not None:
    #     testAllIntelliParse()
    elif args.t is True:
        testDownload()
    else: # a particular day
        if args.d is not None:
            dateCode = args.d[0]
            assert(isValidDateCode(dateCode))
            (part1Answer, part2Answer) = runDay(dateCode)
        else:
            dateCode = getLastDateCode()
            print(f"Last dateCode resolved to {dateCode}")
            (part1Answer, part2Answer) = runDay(dateCode)
        
        print(f"Answer for day {dateCode}:")
        print(f"Part 1: {part1Answer}")
        print(f"Part 2: {part2Answer}")