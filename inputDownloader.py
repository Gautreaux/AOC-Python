
import requests
from os import path

from inputSecrets import SESSION_KEY
from Util.Util import *

def getInputForDateCode(dateCode:str, savePath=None) -> bool:
    '''Download the input for a dateCode, true if success, false if in error'''

    assert(isValidDateCode(dateCode))
    year, day = splitDateCode(dateCode)

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    filePath = f"Input{year}/d{day}.txt" if savePath is None else savePath

    if path.exists(filePath):
        raise FileExistsError(filePath)

    r = requests.get(url, cookies={'session':SESSION_KEY})    
    # print(r.status_code)

    if r.status_code == 200:
        open(filePath, 'wb').write(r.content)
    return r.status_code == 200


if __name__ == "__main__":
    getInputForDateCode("y2015d4")