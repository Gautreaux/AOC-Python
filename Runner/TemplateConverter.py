from datetime import date
from .FileUtil import *
from .Util import isValidDateCode, splitDateCode

TEMPLATE_FILE_PATH = "Templates/template.pyt"

def convertTemplate(dateCode : str) -> str:
    """For a given year date, populate the template and get it started"""

    if not isValidDateCode(dateCode):
        raise RuntimeError(f"DateCode '{dateCode}' is not valid")

    (year, day) = splitDateCode(dateCode)
    solutionDir = f"Solutions{year}"
    solutionName = f"{dateCode}.py"

    if isFileInDir(solutionDir, solutionName) is True:
        raise RuntimeError("Cannot instantiate template of existing file")

    with open(TEMPLATE_FILE_PATH, 'r') as inFile:
        with open(f"{solutionDir}/{solutionName}", 'w') as outFile:
            for line in inFile:
                print(line.replace("%{year}", str(year)).replace("%{day}", str(day)),
                        end = "", file=outFile)
