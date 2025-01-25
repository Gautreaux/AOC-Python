import requests
from pathlib import Path
from typing import Optional

from AOC_Lib.SolutionBase import DateCode
from inputSecrets import SESSION_KEY
from .SolutionLoader import date_code_to_input_file_path
from .Util import getLastDateCode


url_base = "http://adventofcode.com/{}/day/{}/input"


def check_fetch_input(date_code: DateCode, overwrite: bool = False):
    """Download the input for the date code if needed
    and always when `overwrite == True`
    """

    file_path = Path(date_code_to_input_file_path(date_code))
    file_path = file_path.absolute()

    if file_path.exists() and overwrite is False:
        return

    print(f"Downloading file for {date_code}")

    url = url_base.format(date_code.year, date_code.day)

    r = requests.get(url, cookies={"session": SESSION_KEY})

    if r.status_code == 200:
        open(file_path, "wb").write(r.content)
    else:
        print(f"Bad Response: {r.status_code}")


def test_downloader(date_code=getLastDateCode()) -> bool:
    """Check if the downloader is working; Return `True` iff successful"""

    url = url_base.format(date_code.year, date_code.day)

    r = requests.get(url, cookies={"session": SESSION_KEY})

    return r.status_code == 200
