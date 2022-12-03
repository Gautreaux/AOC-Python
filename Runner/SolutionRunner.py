
from inspect import getmembers
import subprocess

from AOC_Lib.SolutionBase import DateCode, SolutionBase, AnswerPair_T
from .InputDownloader import check_fetch_input
from .SolutionLoader import (
    does_module_exist_for_date_code,
    date_code_to_input_file_path,
    date_code_to_solution_file_path,
    load_solution_by_date_code, 
    FunctionImportError
)
from .TemplateConverter import create_from_template



def run_date_code(date_code: DateCode, create_if_missing: bool = True) -> AnswerPair_T:
    """Load and run the solution for the date code"""

    check_fetch_input(date_code)

    if not does_module_exist_for_date_code(date_code) and create_if_missing:
        create_from_template(date_code)

        try:
            solution_path = date_code_to_solution_file_path(date_code)
            subprocess.run(['code', '-r', solution_path], shell=True)
        except:
            pass

        # DO input second so it appears on top and you have to look at it
        try:
            input_path = date_code_to_input_file_path(date_code)
            subprocess.run(['code', '-r', input_path], shell=True)
        except:
            pass

    module = load_solution_by_date_code(date_code)

    # Check if the solution is done with new class based method
    if SolutionBase.has_known_solution(date_code):
        return SolutionBase.run_known_solution(date_code)

    print("Fallback to look for legacy function based implementation")

    # this solution uses the legacy variant of a function called `yXXXXdYY`
    #   where XXXX is the year and YY the day 
    #   note: day does not have leading zeros: `1` `2` ... `15` ... `20` ... `25`
    l = getmembers(module)
    to_find = date_code.to_legacy_datecode()
    for e in l:
        if e[0] == to_find:
            return e[1]()

    # should be unreachable
    raise FunctionImportError(f"For dateCode {date_code}: The module imported correctly, but function not found")

