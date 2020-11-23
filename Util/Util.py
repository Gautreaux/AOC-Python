# generic utility functions

from datetime import date, datetime
import pytz
from typing import Tuple

def getLastDateCode() -> str:
    '''Return the dayCode of the last day that was released'''
    tz_NY = pytz.timezone('America/New_York') 
    datetime_NY = datetime.now(tz_NY)

    if datetime_NY.month != 12:
        return f"y{datetime_NY.year-1}d25"
    elif datetime_NY.day > 25:
        return f"y{datetime_NY.year}d25"
    else:
        return f"Y{datetime_NY.year}d{datetime_NY.day}"


def isValidDateCode(dateCode:str) -> bool:
    '''Return true if dateCode is in y<year>d<day> format and numbers are valid'''
    try:
        assert(len(dateCode) in [7,8])
        assert(dateCode[0] == 'y')
        assert(dateCode[5] == 'd')
        (y, d) = splitDateCode(dateCode)
        assert(y in range(2015,2025))
        assert(d in range(1,26))
    except:
        return False
    return True


def splitDateCode(dateCode:str) -> Tuple[int, int]:
    '''Return the elements of the date code in (year, day), raise error if invalid format'''
    return (int(dateCode[1:5]), int(dateCode[6:]))
    