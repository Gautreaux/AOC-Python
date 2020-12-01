# from AOC_Lib.name import *

raise RuntimeError("Must remove excess provided templates first")

# ================================================================

# sample variant for reading data from an input file, line by line
def y%{year}d%{day}(inputPath = None):
    if(inputPath == None):
        inputPath = "Input%{year}/d%{day}.txt"
    print("%{year} day %{day}:")

    Part_1_Answer = None
    Part_2_Answer = None

    with open(inputPath) as f:
        for line in f:
            print(line)
        
    return (Part_1_Answer, Part_2_Answer)

# ================================================================

# sample variant for reading data with a distinct starting code
Y%{year}D%{day}_DEFAULT_VALUE = "TODO" # TODO - provide the default starting value
def y%{year}d%{day}(inputValue = Y%{year}D%{day}_DEFAULT_VALUE):
    Part_1_Answer = None
    Part_2_Answer = None

    with open(inputPath) as f:
        for line in f:
            print(line)
        
    return (Part_1_Answer, Part_2_Answer)

# ================================================================

# TODO - include variant with auto pattern detection