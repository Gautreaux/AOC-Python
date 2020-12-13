

from Util.Util import isValidDateCode, splitDateCode
import modulefinder
from modulefinder import Module, ModuleFinder
from importlib import import_module
from Util.FileUtil import getAllSubDirectories  
from typing import List

from os import getcwd, path

class ModuleFinderException(Exception):
    pass

def getAllPyFilesForDay(dateCode : str) -> List[str]:
    '''Get a list of all local files required for running a particular datecode'''
    
    # TODO - Testing (some problem exists somewhere)
    # This should work once https://bugs.python.org/issue40350 fixed?
    #   "import math" seems to break things?
    #solutionPath = "Solutions2019/y2019d11.py"    
    # TODO - resolve datecode to file path
    assert(isValidDateCode(dateCode))
    y,d = splitDateCode(dateCode)

    solutionPath = f"Solutions{y}/y{y}d{d}.py"
    
    subDirs = getAllSubDirectories(getcwd())
    
    finder = ModuleFinder(subDirs)
    try:
        finder.run_script(solutionPath)
    except FileNotFoundError:
        raise
    except:
        # it seems to usually work, but in case no, want to log
        print(f"Exception Occurred when running module finder for {dateCode}")
        raise ModuleFinderException

    files = []

    for name, mod in finder.modules.items():
        # print(f"{mod} {mod.__name__} {mod.__path__}")

        if mod.__path__ is None:
            print(dir(mod))
            files.append(mod.__file__)

    return files



if __name__ == "__main__":
    print(getAllPyFilesForDay("y2020d25"))