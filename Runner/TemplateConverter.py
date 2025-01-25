from pathlib import Path

from AOC_Lib.SolutionBase import DateCode
from .SolutionLoader import date_code_to_solution_file_path


TEMPLATE_FILE_PATH = "Templates/template.pyt"


def _template_common(date_code) -> str:
    """Common logic for interacting with templates"""

    template_path = Path(TEMPLATE_FILE_PATH)

    if not template_path.exists():
        raise RuntimeError("Could not find template file")

    with open(TEMPLATE_FILE_PATH, "r") as in_file:
        template_str = in_file.read()

    return template_str.format(
        year=str(date_code.year),
        day=str(date_code.day),
        full_day=f"{date_code.day:02}",
    )


def create_from_template(date_code: DateCode) -> None:
    """For a given year date, populate the template and get it started"""

    target_path = Path(date_code_to_solution_file_path(date_code))
    target_path = target_path.absolute()

    if target_path.exists():
        raise RuntimeError(f"A solution already exists at path {target_path}")

    with open(target_path, "w") as out_file:
        out_file.write(_template_common(date_code))


def append_template(date_code: DateCode) -> None:
    """Update by applying the new template if using the functional method"""

    target_path = Path(date_code_to_solution_file_path(date_code))
    target_path = target_path.absolute()

    if not target_path.exists():
        raise RuntimeError(f"A solution does not exist at path {target_path}")

    with open(target_path, "a") as out_file:
        out_file.write("\n\n# ==================\n\n")
        out_file.write(_template_common(date_code))
