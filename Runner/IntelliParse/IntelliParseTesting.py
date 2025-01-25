from Util.IntelliParse import IntelliParse

TestDict = {
    "Input2015/d1.txt": None,
    # "Input2015/d2.txt" : "([0-9]*)x([0-9]*)x([0-9]*)",
    "Input2016/d4.txt": "([a-z\-]*)-([0-9]*)\[([a-z]{5})\]",
}


def testAllIntelliParse():
    """Test the intelliparse for a set of known inputs"""
    total = 0
    incorrect_results = []

    for k, v in TestDict.items():
        r, _ = IntelliParse(k)
        total += 1
        if r != v:
            incorrect_results.append((k, v, r))

    if len(incorrect_results) == 0:
        print("All intelliparse test cases resolved successfully")
    else:
        for file, expected, actual in incorrect_results:
            print(f"File {file}:\n\tExpected: {expected}\n\t     Got: {actual}\n\t")
        print(f"Of {total} trials, {len(incorrect_results)} incorrect")
