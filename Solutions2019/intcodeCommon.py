
import copy

class MemoryModule:
    __INITIAL_MEMORY_VALUE__ = 0 #the default value for an item not in memory

    def __init__(self):
        self.memory = {}

    def __getitem__(self, key):
        if(key < 0):
            raise KeyError("Illegal memory address: " + str(key))
        if(key not in self.memory):
            self.memory[key] = MemoryModule.__INITIAL_MEMORY_VALUE__
        return self.memory[key]
    
    def __setitem__(self, key, value):
        if(key < 0):
            raise KeyError("Illegal memory address: " + str(key))
        self.memory[key] = value

class IntProcessor:
    #operates on intcode to produce results
    NOT_STARTED = 0
    RUNNING = 1 #reserved for asynchronous behavior 
    FINISHED = 2

    #a mapping of opcode to parameter count
    PARAMETER_DICT = {1:3,2:3,3:1,4:1,5:2,6:2,7:3,8:3,9:1,99:0}

    #TODO - should define basic functions that handle input (from user) and output (to consloe)
    def __init__(self, program, inputFunction = None, outputFunction = None, cache = False):
        'Initialize the IntComputer'
        #params
        # program - [int]
        #   a list of integers that follows the intcode standard
        # inputFunction - the function (void -> int) that will be providing the input 
        # outputFunction - the function (int -> void) that will be receiving the output
        # cache - (T/F) should this program store a raw version of the program 
        #   this is used for reset to avoid rereading from disk


        if(IntProcessor.__isValidProgram(program)):
            self.memory = program
        else:
            raise ValueError("In IntComputer initialization, program failed preliminary checks.");

        self.inputFunction = inputFunction
        self.outputFunction = outputFunction

        if(cache):
            self.cache = copy.deepcopy(self.memory)
        else:
            self.cache = None

        self.state = IntProcessor.NOT_STARTED

    def loadProgram(self, program):
        #load the new program if it is valid
        #otherwise do nothing 

        if(IntProcessor.__isValidProgram(program)):
            self.memory = program
            if(self.cache != None):
                self.cache = copy.deepcopy(self.memory)

            self.state = IntProcessor.NOT_STARTED
        else:
            raise ValueError("In IntComputer initialization, program failed preliminary checks.");

    def reset(self):
        #reset the memory to its cached state  
        #TODO - this should be tested
        if(self.cache == None):
            raise ValueError("Cannot reset a progam which is not cached.")
    
        self.memory = copy.deepcopy(self.cache)
        self.state = IntProcessor.NOT_STARTED

    def getParameter(self, address, mode):
        #gets a parameter based on its address and mode
        if(mode == 0):
            return self.memory[self.memory[address]]
        elif(mode == 1):
            return self.memory[address]
        elif(mode == 2):
            return self.memory[self.relativeBase+self.memory[address]]
        else:
            raise ValueError("Illegal Parameter mode: " + str(mode))
        
    def writeParameter(self, address, mode, value):
        #writes value to the proper location
        if(mode == 0):
            self.memory[self.memory[address]] = value
        elif(mode == 2):
            self.memory[self.memory[address] + self.relativeBase] = value
        else:
            raise ValueError("Illegal write parameter mode: " + str(mode))

    def run(self, programCounterIn = 0, relativeBaseIn = 0):
        #execute the intcode computer
        #params
        #   programCounterIn (optional) - (int) the initial value of the program counter
        #       default 0
        #   relativeBaseIn (optional) - (int) the initial value of the relative base
        #       default 0
        if(self.state != self.NOT_STARTED):
            raise ValueError("The state was not NOT_STARTED ("+str(self.NOT_STARTED)+")")

        self.state = self.RUNNING

        #setup
        modeList = [None, None, None] #stores the modes for each item
        paramList = [None, None, None] #stores the parameter value for each item

        self.programCounter = programCounterIn
        self.relativeBase = relativeBaseIn

        while True:
            #TODO - this is a shortcut, all should be self.programCounter
            programCounter = self.programCounter
            
            fiveNum = IntProcessor.__get5LenNumber(self.memory[programCounter])
            print(fiveNum)
            operation = int(fiveNum[3:5])

            if(operation not in self.PARAMETER_DICT):
                raise ValueError("Illegal operation: " + str(operation))

            paramRequired = self.PARAMETER_DICT[operation]

            modeList = [None, None, None]
            paramList = [None, None, None]

            for i in range(paramRequired):
                modeList[i] = int(fiveNum[2-i])
                paramList[i] = self.getParameter(programCounter+i+1, modeList[i])
            
            if(operation == 99):
                break
            elif(operation == 1):
                self.writeParameter(programCounter+3, modeList[2], paramList[0]+paramList[1])
            elif(operation == 2):
                self.writeParameter(programCounter+3, modeList[2], paramList[0]*paramList[1])
            elif(operation == 3):
                self.writeParameter(programCounter+1, modeList[0], int(self.inputFunction()))
            elif(operation == 4):
                outputFunction(paramList[0])
            elif(operation == 5):
                if(paramList[0] != 0):
                    self.programCounter = paramList[1]
                    continue
            elif(operation == 6):
                if(paramList[0] == 0):
                    self.programCounter = paramList[1]
                    continue
            elif(operation == 7):
                if(paramList[0] < paramList[1]):
                    writeParameter(programCounter+3, modeList[2], 1)
                else:
                    writeParameter(programCounter+3, modeList[2], 0)
            elif(operation == 8):
                if(paramList[0] == paramList[1]):
                    writeParameter(programCounter+3, modeList[2], 1)
                else:
                    writeParameter(programCounter+3, modeList[2], 0)
            elif(operation == 9):
                self.relativeBase += paramList[0]
            else:
                raise ValueError("Illegal operation: " + str(operation) + " in intcode " + str(fiveNum) + " (Secondary catch, how did you get here?)")

            #update the program counter appropriately
            self.programCounter+=paramRequired+1
            #TODO finish

        self.state = IntProcessor.FINISHED
        return True
        #TODO - what should be returned when done?
    
    def __isValidProgram(program):
        'Return true iff the program is a valid program'
        #TODO - what does this check look like?
        return program != None

    def __get5LenNumber(inputNum):
        'Convert a number to its  length representation'
        inputNum = str(inputNum)
        while(len(inputNum) < 5):
            inputNum = '0'+inputNum
        return inputNum


#TODO - should implement a common read program from file class
def readProgramFromDisk(path):
    #read a program from the disk
    #params
    #   path - the path to the file containing the program
    #       this file should be exactly one line long with the intcode program
    #return
    #   None - something went wrong, and a statement is printed
    #   MemoryModule - the program in memory module representation
    if path == None or path == "":
        raise ValueError("Path '" + str(path) + "' is invalid")
    
    try:
        with open(path, 'r') as f:
            line = f.readline().strip()

            #TODO - what is the proper way to see if EOF reached
            nLine = f.readline()
            if(nLine != ""):
                print("Warning reading program, the program file contained multiple lines.")

            intList = line.replace(" ", "").split(",")

            myProgram = MemoryModule()

            for i in range(len(intList)):
                myProgram[i] = int(intList[0])

    except FileNotFoundError as e:
        print("File Not Error reading program: " + str(e))

    return myProgram
