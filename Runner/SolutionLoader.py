"""Loads and runs Solutions"""

from importlib import import_module
import os

from AOC_Lib.SolutionBase import DateCode


class FunctionImportError(RuntimeError):
    """Raised when a function fails to load properly"""


def date_code_to_solution_file_path(date_code: DateCode) -> str:
    """Return the file path for the solution for the datecode"""
    return f"Solutions{date_code.year}/y{date_code.year}d{date_code.day}.py"


def date_code_to_input_file_path(date_code: DateCode) -> str:
    """Return the file path for the input for the datecode"""
    return f"Input{date_code.year}/d{date_code.day}.txt"


def date_code_to_solution_module_name(date_code: DateCode) -> str:
    """Return the module name for the solution for the datecode"""
    return f"Solutions{date_code.year}.y{date_code.year}d{date_code.day}"


def does_module_exist_for_date_code(date_code: DateCode) -> True:
    """Return `True` iff the module exists for the datecode"""
    return os.path.exists(date_code_to_solution_file_path(date_code))


def load_solution_by_date_code(date_code: DateCode):
    """Loads the module for the solution for the given date code"""

    if not does_module_exist_for_date_code(date_code):
        raise FunctionImportError(f"Could not find a solution for {date_code}")

    module = import_module(date_code_to_solution_module_name(date_code))

    return module
