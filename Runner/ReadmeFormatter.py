import os
from typing import List


from AOC_Lib.SolutionBase import DateCode
from .SolutionTesting import TestResult, test_all_days_multiprocessed
from .Util import listElapsedYears, genElapsedDateCodes


def formatTable(
    table: List[List[str]],
    headers: List[str],
) -> str:
    """Take the table (with table[0] as headers) and format to a markdown table"""
    toReturn = []

    toReturn.append("|".join(map(str, headers)))
    toReturn.append("|".join(map(lambda _: "-", headers)))

    for row in table:
        if len(row) != len(headers):
            print("Mis matched row. Formatting may be weird")
        toReturn.append("|".join(map(str, row)))

    return "\n".join(toReturn)


def header() -> str:
    """The header for the readme"""

    return """
# Advent of Code
Solutions for [Advent of Code](https://adventofcode.com/) coding competition.

This is attempt 3 at collecting python solutions the the challenges. Began for 2019 challenge; prior solutions were lost or not in python.

"""


def footer() -> str:
    """The footer for the readme"""

    return """\n\n"""


def build_body() -> str:

    results = test_all_days_multiprocessed()

    solutions_headers = [":christmas_tree:"]
    solutions_headers.extend(listElapsedYears())

    solutions_rows = []
    star_count = 0

    valid_days = set(genElapsedDateCodes())

    for day in range(1, 26):
        this_row = [day]

        for year in listElapsedYears():

            dc = DateCode(year=year, day=day)

            if dc not in valid_days:
                this_row.append(" ")
                continue

            try:
                r = results.get(dc)

                if r == TestResult.TWO_STAR:
                    star_count += 2
                if r == TestResult.ONE_STAR:
                    star_count += 1

                this_row.append(
                    f"[{r.readme_str}](http://adventofcode.com/{year}/day/{day})"
                )
            except KeyError:
                print("SHOULD BE UNREACHABLE")
                this_row.append(TestResult.SOLUTION_INCORRECT.readme_str)
        solutions_rows.append(this_row)

    stars_possible = 2 * len(valid_days)

    star_table = formatTable(table=solutions_rows, headers=solutions_headers)

    legend_rows = []

    for x in TestResult:
        legend_rows.append([x.readme_str, x.readme_description])

    legend_table = formatTable(
        headers=[":santa:", "Legend"],
        table=legend_rows,
    )

    return """
### Solution Coverage

:star: `{star_count}` of `{stars_possible}`

{star_table}

{legend_table}    
    """.format(
        star_count=star_count,
        stars_possible=stars_possible,
        star_table=star_table,
        legend_table=legend_table,
    )


def format_readme(readme_path: str = "README.md"):

    readme = """
{header}

---

{body}

---

{footer}

""".format(
        header=header(),
        body=build_body(),
        footer=footer(),
    )
    with open(readme_path, "w") as out_file:
        out_file.write(readme)
