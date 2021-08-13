# from AOC_Lib.name import *

def y2015d19(inputPath = None):
    if(inputPath == None):
        inputPath = "Input2015/d19.txt"
    print("2015 day 19:")

    Part_1_Answer = None
    Part_2_Answer = None
    lineList = []

    with open(inputPath) as f:
        for line in f:
            line = line.strip()
            lineList.append(line)

    base_molecule = lineList[-1].strip()
    lineList.pop()
    lineList.pop()

    translations = []

    for line in lineList:
        base, _, result = line.partition(" => ")
        translations.append((base, result))
    
    all_molecules = set()

    for base, result in translations:
        next_start = 0
        while next_start < len(base_molecule):
            i = base_molecule.find(base, next_start)

            if i == -1:
                break
            
            l = base_molecule[:i]
            r = base_molecule[(i + len(base)):]
            new_molecule = result.join([l,r])
            all_molecules.add(new_molecule)

            next_start = i + 1

    Part_1_Answer = len(all_molecules)

    return (Part_1_Answer, Part_2_Answer)