# given a multi-lin input will attempt to extract a regex pattern for the line
from collections import Counter
from typing import Tuple, List


def IntelliParseSubstringList(strList: List[str]) -> str:
    strCount = len(strList)

    def charsetGenerator():
            for l in strList:
                for c in l:
                    yield c

    totalChars = sum(map(lambda _:1, charsetGenerator()))

    if totalChars == 0:
        # all empty strings input, recursion exit
        return ""

    # collect some metadata about the str

    strLenCommon = len(strList[0])  # int if all strs same length else None
    for s in strList:
        if len(s) != strLenCommon:
            strLenCommon = None
            break
    
    # Get the set of all characters in the input
    CharSet = Counter(charsetGenerator())

    probableDelimiters = {}

    # simple delimiters check
    for c in CharSet:
        if CharSet[c] % strCount == 0:
            probableDelimiters[c] = CharSet[c] // strCount
            print(f"Found new probable delimiter {c} with {probableDelimiters[c]} per line")

    # thourough delimeters check
    for s in strList:
        for delimiter in probableDelimiters:
            t = sum(map(lambda x: 1 if x == delimiter else 0, s))
            if t != probableDelimiters[delimiter]:
                # remove the delimiter from consideration
                probableDelimiters.pop(delimiter, None)
                print(f"Removed delimiter {delimiter} from consideration")

    if len(probableDelimiters) == 0:
        # no probable delimiters, need to find a string to capture the current situation
        pass
        # return most generic specific string that matches all lines?

    # split on a delimiters and recurse on each portion

    print(CharSet)


def IntelliParse(filePath : str) -> Tuple[str, str]:
    """Run intelliparse on the filepath and return matching regex and description"""
    # may return (None, str) if the input is believed to be regex impossible

    lineList = [] # list containing all the lines
    lineCount = 0 # count of total lines

    try:
        with open(filePath) as f:
            for line in f:
                lineList.append(line.strip())
                lineCount +=1 
    except FileNotFoundError as e:
        print(f"IntelliParse failed to find file {filePath}")
        raise e

    if lineCount == 1:
        return (None, "Single Line Input")
    elif lineCount <= 0:
        raise ValueError("Something went wrong. File was empty?")

    res = IntelliParseSubstringList(lineList)

    # check against the input to verify

    
    raise NotImplementedError