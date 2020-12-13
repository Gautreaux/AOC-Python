

from Util.FileUtil import getAllSubDirectories  
from typing import List
from modulefinder import Module, ModuleFinder
from os import getcwd


def getAllModulesInDay(dateCode : str) -> List[Module]:
    
    # TODO - resolve datecode to file path
    

    itemPath = "Solutions2020/y2020d11.py"
    # itemPath = "Solutions2019/y2019d11.py"

    subDirs = getAllSubDirectories(getcwd())
    print(subDirs)

    finder = ModuleFinder(subDirs)
    finder.run_script(itemPath)

    mm: Module = None
    for name, mod in finder.modules.items():
        print(f"{mod} {mod.__name__} {mod.__path__}")
        mm = mod
        
    print(dir(mm))
        
    finder.report()



if __name__ == "__main__":
    getAllModulesInDay("apple")