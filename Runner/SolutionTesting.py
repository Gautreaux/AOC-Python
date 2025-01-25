from enum import Enum, unique
import json
import multiprocessing
import os
import sys
import time


from AOC_Lib.SolutionBase import DateCode
from .SolutionLoader import FunctionImportError, does_module_exist_for_date_code
from .SolutionRunner import run_date_code
from .Util import genElapsedDateCodes


solutions_path = "known_solutions.json"

solutionDict = json.load(open(solutions_path, "r"))


@unique
class TestResult(Enum):
    """A result of a test for a day"""

    ERROR_UKN = -1
    SOLUTION_NOT_STARTED = 0
    ONE_STAR = 1
    TWO_STAR = 2
    SOLUTION_INCORRECT = 3
    SOLUTION_EXCEPTION = 4
    SOLUTION_ANS_NOT_PROVIDED = 5

    @property
    def readme_str(self) -> str:
        if self == TestResult.ERROR_UKN:
            return ":question:"
        elif self == TestResult.TWO_STAR:
            return ":star:"
        elif self == TestResult.ONE_STAR:
            return ":low_brightness:"
        elif self == TestResult.SOLUTION_NOT_STARTED:
            return ":heavy_multiplication_x:"
        elif self == TestResult.SOLUTION_INCORRECT:
            return ":x:"
        elif self == TestResult.SOLUTION_EXCEPTION:
            return ":exclamation:"
        elif self == TestResult.SOLUTION_ANS_NOT_PROVIDED:
            return ":warning:"
        raise RuntimeError(self)

    @property
    def readme_description(self) -> str:
        if self == TestResult.ERROR_UKN:
            return "Unknown Error"
        elif self == TestResult.TWO_STAR:
            return "Both Completed"
        elif self == TestResult.ONE_STAR:
            return "One Star Completed"
        elif self == TestResult.SOLUTION_NOT_STARTED:
            return "Solution Not Started"
        elif self == TestResult.SOLUTION_INCORRECT:
            return "Solution Incorrect"
        elif self == TestResult.SOLUTION_EXCEPTION:
            return "Error Running Solution"
        elif self == TestResult.SOLUTION_ANS_NOT_PROVIDED:
            return "No Known Answer for Solution"
        raise RuntimeError(self)


def check_date_code(date_code: DateCode) -> TestResult:

    if not does_module_exist_for_date_code(date_code):
        return TestResult.SOLUTION_NOT_STARTED

    try:
        answers = run_date_code(date_code, create_if_missing=False)
    except FileNotFoundError:
        # Should be unreachable
        return TestResult.SOLUTION_NOT_STARTED
    except FunctionImportError:
        return TestResult.ERROR_UKN
    except Exception:
        return TestResult.SOLUTION_EXCEPTION

    # we know the answer returned something
    ldc = date_code.to_legacy_datecode()
    if ldc not in solutionDict:
        return TestResult.SOLUTION_ANS_NOT_PROVIDED

    knownAnswers = solutionDict[ldc]

    stars = 0
    try:
        for i in range(2):
            if answers[i] == None:
                continue
            if knownAnswers[i] == answers[i]:
                stars += 1
    except Exception:
        stars = 0

    if date_code.day == 25 and stars == 1:
        stars = 2

    return [TestResult.SOLUTION_INCORRECT, TestResult.ONE_STAR, TestResult.TWO_STAR][
        stars
    ]


def _check_date_code_wrapper(date_code: DateCode) -> tuple[DateCode, TestResult]:
    start_time = time.time()
    r = check_date_code(date_code)
    end_time = time.time()
    return (date_code, r, (end_time - start_time))


def _mute():
    # Mutes std-out
    sys.stdout = open(os.devnull, "w")


def test_all_days() -> dict[DateCode, TestResult]:
    """Test all days WITHOUT MULTIPROCESSING"""

    results = []

    for dc in genElapsedDateCodes():
        x = _check_date_code_wrapper(dc)
        results.append(x)
    print(results)
    return dict(results)


def test_all_days_multiprocessed(
    date_codes: list[DateCode] = list(genElapsedDateCodes()),
) -> dict[DateCode, TestResult]:
    """Test all days, utilizing multiprocessing for performance improvements"""

    # with multiprocessing.Pool(initializer=_mute) as p:
    #     return dict(p.map(_check_date_code_wrapper, genElapsedDateCodes()))

    date_codes = date_codes

    pool = multiprocessing.Pool(initializer=_mute)

    results = []

    for dc, result, elapsed_time_s in pool.imap_unordered(
        _check_date_code_wrapper, date_codes
    ):
        results.append((dc, result))

        elapsed_time_s = round(elapsed_time_s, 4)

        if result != TestResult.TWO_STAR or elapsed_time_s > 10:
            print(
                f"{dc.year:04}.{dc.day:02} - {elapsed_time_s:>010.4}s - {result.name}"
            )

        if len(results) % 10 == 0:
            print(f"{len(results):04} of {len(date_codes)} done")

    return dict(results)
