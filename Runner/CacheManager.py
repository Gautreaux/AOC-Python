
import atexit
from modulefinder import ModuleFinder
from .Util import isValidDateCode, splitDateCode
from .FileUtil import getAllSubDirectories  
from os import getcwd, path
import pickle
from time import time as nowTime
from typing import Any, Final, List, Optional, Tuple, Union

from main import FunctionImportError, runDay

_DATECODE_CACHE_PATH : Final = "dateCodeCache.cacheData"
_DATECODE_CACHE : '_DateCodeCache' = None

SolutionType = Union[Tuple[int, int], 'SolutionNotStarted', FunctionImportError, RuntimeError]

class ModuleFinderException(Exception):
    pass

class SolutionNotStarted(Exception):
    def __str__(self) -> str:
        return "Solution not Started"

def runDayWrapper(key: str) -> SolutionType:
    # run the actual datecode item
    try:
        answers = runDay(key, False)
    except FileNotFoundError:
        # the solution has not been started
        answers = SolutionNotStarted
    except FunctionImportError:
        # the function could not be imported,
        #   but the file exists
        answers = FunctionImportError
    except Exception:
        # the solution running threw an exception
        answers = RuntimeError
    return answers


# class for interacting with the datecode cache
class _DateCodeCache():
    def __init__(self) -> None:
        assert(_DATECODE_CACHE is None)
        self.loadCache()
        self.lastSaveTime = nowTime()
    

    def saveCache(self, window=(1*60*1000)):
        '''save the cache if more than window time has elapsed'''
        # default window 1 min
        if (self.lastSaveTime + window) < nowTime():
            with open(_DATECODE_CACHE_PATH, 'wb') as cacheFile:
                pickle.dump(self.cacheData, cacheFile)

    def loadCache(self):
        # data cache ordered {dateCode, (cacheTime (Part_1_Answer, Part_2_Answer))}
        #self.cacheData : Dict[str, Tuple(int, Tuple(int, int))]
        try:
            with open(_DATECODE_CACHE_PATH, 'rb') as cacheFile:
                self.cacheData = pickle.load(cacheFile)
        except FileNotFoundError:
            print("DateCode cache was not found, creating new cache")
            self.cacheData = {}

    def __getitem__(self, key: str) -> SolutionType:
        '''get the item, re-evaluating/re-caching if necessary'''
        # returns None if solution not implemented
        # returns exception if one occurs
        if self.isCacheValid(key):
            return self.getCacheValue(key)
        
        answers = runDayWrapper(key)
        self[key] = answers # update the storage
        return answers

    def __setitem__(self, key : str, answers : SolutionType) -> None:
        self.cacheData[key] = (nowTime(), answers)
        self.saveCache() # if more than window, trigger autosave
        
    def getCacheValue(self, key: str) -> Any:
        '''return the item without re-evaluating if out of date'''
        # returns none if the items is not cached
        #   note - a solution could exist and it simply hasn't been cached yet
        if key in self.cacheData:
            return self.cacheData[key][1]
        else:
            return None

    def getCacheTime(self, key: str) -> Optional[int]:
        '''returns the time the cache entry was created for the key'''
        # similar semantics to getCacheValue
        if key in self.cacheData:
            return self.cacheData[key][0]
        else:
            return None

    def isCacheValid(self, key: str) -> bool:
        cacheTime = self.getCacheTime(key)
        if cacheTime is None:
            return False

        try:
            modTime = getDateCodeLastModified(key)
        except FileNotFoundError:
            # solution probably does not exist
            return False
        return modTime < cacheTime

def _cleanup():
    if _DATECODE_CACHE is not None:
        _DATECODE_CACHE.saveCache(0)

atexit.register(_cleanup)

def getAllPyFilesForDay(dateCode : str) -> List[str]:
    '''Get a list of all local files required for running a particular datecode'''
    
    # TODO - Testing (some problem exists somewhere)
    # This should work once https://bugs.python.org/issue40350 fixed?
    #   "import math" seems to break things?
    #   dateCode = "y2019d11" # this will cause an error

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
            # print(dir(mod))
            files.append(mod.__file__)

    # Quickfix for the error with running on math
    while None in files:
        files.remove(None)

    return files

def getDateCodeLastModified(dateCode: str) -> int:
    '''For a datecode, get the possible last modified unix time'''
    try:
        return max(map(path.getmtime, getAllPyFilesForDay(dateCode)))
    except ModuleFinderException:
        return int(1 << 34)


def cacheInterface(function) -> Any:
    global _DATECODE_CACHE
    if _DATECODE_CACHE is None:
        _DATECODE_CACHE = _DateCodeCache()
    return function()


def getDateCodeCachedSolution(dateCode: str) -> int:
    '''Return the cached value of the dateCode'''
    return cacheInterface(lambda : _DATECODE_CACHE.getCacheValue(dateCode))

def getDateCodeCurrentSolution(dateCode: str) -> int:
    '''Return the solution for the date code, updating the cache if necessary'''
    return cacheInterface(lambda : _DATECODE_CACHE[dateCode])

def getDateCodeCacheTime(dateCode: str) -> int:
    '''Return the the time the solution was cached'''
    return cacheInterface(lambda : _DATECODE_CACHE.getCacheTime(dateCode))

def isCacheValid(dateCode: str) -> int:
    return cacheInterface(lambda : _DATECODE_CACHE.isCacheValid(dateCode))

def cacheKnownAnswer(datecode: str, answer: SolutionType) -> None:
    # for use with multiprocessing
    def f():
        _DATECODE_CACHE[datecode] = answer
    return cacheInterface(f)



if __name__ == "__main__":
    print(getAllPyFilesForDay("y2020d12"))
    print(getDateCodeLastModified("y2020d12"))
    print(getDateCodeCachedSolution("y2020d12"))
    print(getDateCodeCacheTime("y2020d12"))