
import copy

class MemoryModule:
    __INITIAL_MEMORY_VALUE__ = 0

    def __init__(self):
        self.memory = {}

    def __getitem__(self, key):
        if(key < 0):
            raise KeyError("Illegal memory address: " + str(key))
        if(key not in self.memory):
            self.memory[key] = __INITIAL_MEMORY_VALUE__
        return self.memory[key]
    
    def __setitem__(self, key, value):
        if(key < 0):
            raise KeyError("Illegal memory address: " + str(key))
        self.memory[key] = value

def __isValidProgram(program):
    'Return true iff the program is a valid program'
    #TODO - what does this check look like?
    return program != None

def __get5LenNumber(inputNum):
    inputNum = str(inputNum)
    while(len(inputNum) < 5):
        inputNum = '0'+inputNum
    return inputNum

class IntProcessor:
    #operates on intcode to produce results
    NOT_STARTED = 0
    RUNNING = 1 #reserved for asychronous behavior 
    FINISHED = 2

    #a mapping of opcode to parameter count
    PARAMETER_DICT = {1:3,2:3,3:1,4:1,5:2,6:2,7:3,8:3,9:1,99:0}

    def __init__(self, program, inputFunction = None, outputFunction = None, cache = False):
        'Initialize the IntComputer'
        #params
        # inputFunction - the function that will be providing the input (void -->int)
        # outputFunction - the function that will be receiving the output (int --> void)
        # cache - should this program store a raw version of the program 
        #   this is used for reset


        if(__isValidProgram(program)):
            self.memory = program
        else:
            raise ValueError("In IntComputer initialization, program failed preliminary checks.");

        self.inputFunction = inputFunction
        self.outputFunction = outputFunction

        if(cache):
            self.cache = copy.deepcopy(self.memory)
        else:
            self.cache = None

        self.state = NOT_STARTED



    def loadProgram(self, program):
        #load the new program if it is valid
        #otherwise do nothing 

        if(__isValidProgram(program)):
            self.memory = program
            if(self.cache != None):
                self.cache = copy.deepcopy(self.memory)

            self.state = self.NOT_STARTED
            self.relativeBase = None

    def reset(self):
        #reset the memory to its cached state  
        #TODO - this should be tested
        if(self.cache == None):
            raise ValueError("Cannot reset a progam which is not cached.")
    
        self.memory = copy.deepcopy(self.cache)
        self.state = self.NOT_STARTED

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
        if(self.state != self.NOT_STARTED):
            raise ValueError("The state was not NOT_STARTED (0)")

        self.state = self.RUNNING

        #setup
        modeList = [None, None, None] #stores the modes for each item
        paramList = [None, None, None] #stores the parameter value for each item

        programCounter = programCounterIn

        while True:
            fiveNum = __get5LenNumber(self.memory[programCounter])
            operation = int(fiveNum[3:5])

            if(opcode not in self.PARAMETER_DICT):
                raise ValueError("Illegal opcode: " + str(operation))

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
            #TODO finish

        self.state = self.FINISHED
