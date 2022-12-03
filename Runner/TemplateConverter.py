
from pathlib import Path

from AOC_Lib.SolutionBase import DateCode
from .SolutionLoader import date_code_to_solution_file_path


TEMPLATE_FILE_PATH = "Templates/template.pyt"


def create_from_template(date_code : DateCode) -> None:
    """For a given year date, populate the template and get it started"""

    template_path = Path(TEMPLATE_FILE_PATH)

    if not template_path.exists():
        raise RuntimeError("Could not find template file")

    target_path = Path(date_code_to_solution_file_path(date_code))
    target_path = target_path.absolute()

    if target_path.exists():
        raise RuntimeError(f"A solution already exists at path {target_path}")

    with open(TEMPLATE_FILE_PATH, 'r') as in_file:
        template_str = in_file.read()
    
    to_export = template_str.format(
        year=str(date_code.year),
        day=str(date_code.day),
        full_day=f"{date_code.day:02}",
    )

    with open(target_path, 'w') as out_file:
        out_file.write(to_export)
