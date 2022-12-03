
import os
from typing import Final, List

from solutionTesting import getCachedSolutionState, ERROR_UKN, SOLUTION_NOT_STARTED, ONE_STAR, TWO_STAR, SOLUTION_INCORRECT, SOLUTION_EXCEPTION, SOLUTION_ANS_NOT_PROVIDED
from .Util import genElapsedDateCodes, getDateCodeAsURL, splitDateCode


AUTO_GEN_FIRST_LINE_PREFIX : Final = "### Solution Coverage"
AUTO_GEN_LAST_LINE_PREFIX : Final = "Last Commit Changed"
assert(AUTO_GEN_FIRST_LINE_PREFIX != AUTO_GEN_LAST_LINE_PREFIX)

characterMap = {
    ERROR_UKN : (':question:', 'Unknown Error'),
    TWO_STAR : (':star:', "Both Completed"),
    ONE_STAR : (':low_brightness:', "One Star Completed"),
    SOLUTION_NOT_STARTED : (':heavy_multiplication_x:', "Solution Not Started"),
    SOLUTION_INCORRECT : (':x:', "Solution Incorrect"),
    SOLUTION_EXCEPTION : (':exclamation:', "Error Running Solution"),
    SOLUTION_ANS_NOT_PROVIDED : (':warning:', "No known answer for solution")
}

def formatTable(table : List[List[str]]) -> str:
    '''Take the table (with table[0] as headers) and format to a markdown table'''
    toReturn = []
    headerRow = ['|']
    separatedRow = ['|']
    for e in table[0]:
        headerRow.append(str(e))
        headerRow.append('|')
        separatedRow.append('-')
        separatedRow.append('|')
    toReturn.append("".join(headerRow))
    toReturn.append("\n")
    toReturn.append("".join(separatedRow))
    toReturn.append("\n")
    for row in table[1:]:
        t = ['|']
        for e in row:
            t.append(str(e))
            t.append('|')
        toReturn.append("".join(t))
        toReturn.append('\n')
    return "".join(toReturn)


def doAutoGen(fileHandle, blockNo : int) -> None:
    # blockNo could be used to add various generation behaviors
    assert(blockNo == 0)

    print(AUTO_GEN_FIRST_LINE_PREFIX, file=fileHandle)
    print("Testing Mode Ongoing\n")

    totalStars = 0
    totalItems = 0

    resultsDict = {}    

    for dateCode in genElapsedDateCodes():
        totalItems += 1
        y,d = splitDateCode(dateCode)
        k = getCachedSolutionState(dateCode)
        if k == ONE_STAR:
            totalStars += 1
        elif k == TWO_STAR:
            totalStars += 2
        resultChar = characterMap[k][0]
        resultContents = f"[{resultChar}]({getDateCodeAsURL(dateCode)})"

        if y not in resultsDict:
            resultsDict[y] = {}

        # store the semi-formatted results in a dict
        if d in resultsDict[y]:
            raise RuntimeError(f"Datecode {dateCode} processed multiple times")
        resultsDict[y][d] = resultContents

    
    # convert dict into a proper table
    years = list(resultsDict)
    years.sort()

    resultsTable = []
    t = [":christmas_tree:"]
    for year in years:
        t.append(year)
    resultsTable.append(t)

    for day in range(1, 26):
        thisRow = [day]
        for j in range(1, len(resultsTable[0])):
            y = resultsTable[0][j]
            if day in resultsDict[y]:
                thisRow.append(resultsDict[y][day])
            else:
                thisRow.append("")
        resultsTable.append(thisRow)

    print(f"{characterMap[TWO_STAR][0]} `{totalStars}` of `{totalItems * 2}`", file=fileHandle)

    print(formatTable(resultsTable), file=fileHandle)

    # build the legend
    legendTable = [[":santa:", "Legend"]]
    for k in characterMap:
        legendTable.append(characterMap[k])
    print(formatTable(legendTable), file=fileHandle)


    print(AUTO_GEN_LAST_LINE_PREFIX, file=fileHandle, end="")
    # TODO - rest of this line
    # would like to include # soltutions modified and number increased/decreased
    print("`NOT_IMPLEMENTED` number of solutions", file=fileHandle)
    print("\n", file=fileHandle) # 2x newline

    return

def formatReadme(path:str="Readme.md" ) -> None:
    '''Format the readme file with auto-generated contents'''

    # get the swap target:
    i = 1
    swpPath = path + ".swp"
    while os.path.exists(swpPath):
        swpPath = path + f".{i}.swp"
        i += 1

    # flag variables
    hasDoneAutoGen : bool = False
    inAutoGen : bool = False
    autoGenBlocks : int = 0

    # use a swap file to preserve the last one if things fail
    try:
        with open(swpPath, 'w') as outFile:
            with open(path, 'r') as inFile:
                for line in inFile:
                    if inAutoGen is True:
                        # skip all lines until we found the end of the auto-generator
                        if line.find(AUTO_GEN_LAST_LINE_PREFIX) != -1:
                            inAutoGen = False
                    else:
                        if line.find(AUTO_GEN_FIRST_LINE_PREFIX) != -1:
                            inAutoGen = True
                            doAutoGen(outFile, autoGenBlocks)
                            autoGenBlocks += 1
                        else:
                            # copy the line to out file
                            print(line, file=outFile, end="")      
    except Exception as e:
        # remove the swp file to prevent clutter
        if os.path.exists(swpPath):
            os.remove(swpPath)
        raise e

    # the file generated correctly, so time to do the swap
    os.remove(path)
    os.rename(swpPath, path)

if __name__ == "__main__":
    formatReadme()