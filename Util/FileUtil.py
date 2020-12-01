# libraries for working with the file system

import os


def allFilesInDirByType(searchDir, fileType) -> list:
    '''get all files of the type fileType in the searchDir'''
    # returns full paths relative to search dir
    if(fileType[0] == '.'):
        fileType = fileType[1:]

    if(len(fileType) <= 0):
        #actually, it could be: lets see if this is a long term problem
        raise IndexError(f"The file type cannot be empty")

    return [f for f in [searchDir+'/'+f for f in os.listdir(searchDir)] if
                os.path.isfile(f) and f[-len(fileType):] == fileType]

def isFileInDir(dir:str, file:str) -> bool:
    """Given a dir, see if a file exists"""
    try:
        return file in os.listdir()
    except:
        # Treat a directory not existing as file not present
        return False

def isPathInHeirarchy(path:str) -> bool:
    """Given a path, see if the file exists"""
    k = path.rfind('/')
    return isFileInDir(path[:k], path[k+1:])