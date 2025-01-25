# generic utility functions

from datetime import datetime
import pytz
from typing import Generator

from AOC_Lib.SolutionBase import DateCode


def getLastDateCode() -> str:
    """Return the dayCode of the last day that was released"""
    tz_NY = pytz.timezone("America/New_York")
    datetime_NY = datetime.now(tz_NY)

    if datetime_NY.month != 12:
        return DateCode(datetime_NY.year - 1, 25)
    elif datetime_NY.day > 25:
        return DateCode(datetime_NY.year, 25)
    else:
        return DateCode(datetime_NY.year, datetime_NY.day)


def genElapsedDateCodes() -> Generator[DateCode, None, None]:
    """'Generator of all released dateCodes"""
    START_DATE_CODE = DateCode(year=2015, day=1)
    last_date_code = getLastDateCode()

    for year in range(START_DATE_CODE.year, last_date_code.year + 1):
        for day in range(
            1, 26 if year != last_date_code.year else last_date_code.day + 1
        ):
            yield DateCode(year=year, day=day)


def listElapsedYears() -> list[int]:
    """Generate a list of all years, sorted ascending"""

    l = list(set(map(lambda x: x.year, genElapsedDateCodes())))
    l.sort()
    return l
