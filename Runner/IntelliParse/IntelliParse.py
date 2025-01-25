# given a multi-lin input will attempt to extract a regex pattern for the line
from AOC_Lib.charSets import *
from collections import Counter
from typing import Tuple, List


def asRegexChar(c):
    if c in ALPHABET_BOTH or c in CHARSET_DIGITS:
        return c

    escapeList = ["]", "-"]

    if c in escapeList:
        return "\\" + c
    return c


def resolveLetterCharset(charset) -> str:
    """Resolve the charset given that all inputs are letters a-z or A-Z"""
    # TODO - perhaps some more distinct processing
    #   is it all letters or just a subset?
    hasUppercase = False
    hasLowercase = False

    for c in charset:
        if c in ALPHABET_UPPER:
            hasUppercase = True
        if c in ALPHABET_LOWER:  # elif should be ok?
            hasLowercase = True

    if hasUppercase is True and hasLowercase is False:
        return REGEX_ALPHABET_UPPER
    elif hasUppercase is False and hasLowercase is True:
        return REGEX_ALPHABET_LOWER
    elif hasLowercase is True and hasUppercase is True:
        return REGEX_ALPHABET_BOTH

    # Should be unreachable (both are false)
    print(charset)
    raise RuntimeError("In find letters set, no letters found?")


def resolveDigitCharset(charset) -> str:
    """Determine digit coverage, i.e. is octal, decimal, binary?"""
    raise NotImplementedError()


def resolveAlphaNumericCharset(charset) -> str:
    """Determine the alphanumberic representation"""
    # either (a-z + 0-9) or hexadecimal?
    raise NotImplementedError()


def resolveSpecialCharset(char) -> str:
    # this means the group is somethign like "!!%#$%%^%/"
    #   no letters, no numbers
    # just enumerate them all i guess
    #   otherwise, there are some special cases? like: [NSEW] [^><v]?
    partialString = ""
    for c in partialString:
        partialString += asRegexChar(c)
    return partialString


def getREGEXCharset(charSet) -> str:
    """Need to detect the charset associated with strings"""

    hasLetter = False
    hasNumber = False
    hasNonLetterNumber = False

    for c in charSet:
        if c in ALPHABET_BOTH:
            hasLetter = True
        if c in CHARSET_DIGITS:
            hasNumber = True
        # inefficient but whatever
        if c not in ALPHABET_BOTH and c not in CHARSET_DIGITS:
            hasNonLetterNumber = True

    def NotImplementedWrapper():
        raise NotImplementedError()

    def RuntimeErrorWrapper():
        raise RuntimeError()

    # what to do in each of the eight cases
    #   use keyError to allow falling through
    behaviors = {
        (False, False, False): (lambda _: RuntimeErrorWrapper()),  # nothing?
        # only non-letters-numbers
        (False, False, True): (lambda _: resolveSpecialCharset(charSet)),
        (False, True, False): (lambda _: resolveDigitCharset(charSet)),  # only numbers
        # (False, True, True) : (lambda _: NotImplementedWrapper()),
        (True, False, False): (lambda _: resolveLetterCharset(charSet)),  # only letters
        # (True, False, True) : (lambda _: NotImplementedWrapper()),
        # only letters and numbers
        (True, True, False): (lambda _: resolveAlphaNumericCharset(charSet)),
        # (True, True, True) : (lambda _: NotImplementedWrapper()),
    }

    stateTuple = (hasLetter, hasNumber, hasNonLetterNumber)

    try:
        return behaviors[stateTuple]()
    except KeyError:
        pass

    # not sure how to proceed on mixed charsets
    raise NotImplementedError()

    # check returned set against charset before returning?


def IntelliParseSubstringList(strList: List[str]) -> str:
    strCount = len(strList)

    # generator for iterating over all characters in the input
    def charsetGenerator():
        for l in strList:
            for c in l:
                yield c

    totalChars = sum(map(lambda _: 1, charsetGenerator()))

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
            print(
                f"Found new probable delimiter {c} with {probableDelimiters[c]} per line"
            )

    # thourough delimeters check
    for s in strList:
        for delimiter in probableDelimiters:
            t = sum(map(lambda x: 1 if x == delimiter else 0, s))
            if t != probableDelimiters[delimiter]:
                # remove the delimiter from consideration
                probableDelimiters.pop(delimiter, None)
                print(f"Removed delimiter {delimiter} from consideration")

    if len(probableDelimiters) == 0:
        # no probable delimiters, do search for advanced delimiter

        # check if a delimiter appears in all lines at some position

        # see if there is a charset split somewhere
        # ex: "aaaa111111"

        # if found, add to probable delimiters
        raise NotImplementedError()

    if len(probableDelimiters) == 0:
        # no more delimiters, treat this string as a capture group
        # return most specific capture group for the input
        return getREGEXCharset(CharSet)

    # split on a delimiter and recurse on each portion

    print(CharSet)

    raise NotImplementedError()


def IntelliParse(filePath: str) -> Tuple[str, str]:
    """Run intelliparse on the filepath and return matching regex and description"""
    # may return (None, str) if the input is believed to be regex impossible

    lineList = []  # list containing all the lines
    lineCount = 0  # count of total lines

    try:
        with open(filePath) as f:
            for line in f:
                lineList.append(line.strip())
                lineCount += 1
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
