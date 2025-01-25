
from argparse import ArgumentParser
from os import system, name
from time import time


from AOC_Lib.SolutionBase import DateCode
from Runner.InputDownloader import test_downloader
from Runner.ReadmeFormatter import format_readme
from Runner.SolutionRunner import run_date_code
from Runner.SolutionTesting import test_all_days_multiprocessed
from Runner.Util import getLastDateCode


if __name__ == "__main__":
    parser = ArgumentParser(description="Run an advent of code trial(s). Runs the most recent day unless otherwise specified.")
    parser.add_argument('-a', action='store_true', help="Run all (cached)")
    parser.add_argument('-d', nargs=2, help="Load and run the date code")
    # parser.add_argument('-p', action='store_true', help=testAllIntelliParse.__doc__)
    parser.add_argument('-t', action='store_true', help="test to see if downloader is working")
    parser.add_argument('-r', action='store_true', help="run the readme formatter")
    parser.add_argument('-c', action='store_true', help="clear console before running")
    parser.add_argument('-u', action='store_true', help="append the new template to legacy code.")

    args = parser.parse_args()
     

    if args.c is True:
        # Clear console before running
        system('cls' if name == 'nt' else 'clear')
    elif args.t is True:
        # Test Downloader
        print("Testing Downloader")
        if test_downloader:
            print("Downloader is working")
        else:
            print("Downloader failed")
    elif args.r is True:
        format_readme()
    elif args.a:
        print("Running on all days (this may take some time)")
        start_time = time()
        test_all_days_multiprocessed()
        end_time = time()

        print("Took {} seconds".format(round(end_time-start_time, 1000)))
    else: 
        do_uplift = bool(args.u)

        # Run a particular day
        if args.d is not None:
            assert len(args.d) >= 2
            dateCode = DateCode(int(args.d[0]), int(args.d[1]))
            (part1Answer, part2Answer) = run_date_code(dateCode, uplift_if_legacy=do_uplift)
        else:
            dateCode = getLastDateCode()
            print(f"Last dateCode resolved to {dateCode}")
            (part1Answer, part2Answer) = run_date_code(dateCode, uplift_if_legacy=do_uplift)
        
        print(f"Answer for day {dateCode}:")
        print(f"Part 1: {part1Answer}")
        print(f"Part 2: {part2Answer}")
