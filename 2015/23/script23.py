from functools import reduce
import re
import math
from collections import defaultdict

FILE_NAME = "example"
FILE_NAME = "input"





class Instruction:
    TOKEN_TRANSPOSITION = {
        "str": lambda t: t,
        "int": lambda t: int(t)
    }

    def __init__(self, name, regex, tokenTypes):
        self.name = name
        self.regex = regex
        self.tokenTypes = tokenTypes
    
    def match(self, instr):
        match = re.match(self.regex, instr)
        return match is not None
        
    def getTokens(self, instr):
        # match should have been called first
        match = re.match(self.regex, instr)
        tokens = [self.TOKEN_TRANSPOSITION[typ](match.group(i+1)) for i,typ in enumerate(self.tokenTypes)]
        return tokens
        
    def updateStatusAndPC(self, pc, status, tokens):
        pass


STR = "([a-zA-Z]+)"
NUM = "([+-]\d+)"

class Half(Instruction):
    def __init__(self):
        super().__init__("hlf", f"hlf {STR}", ["str"])
        
    def updateStatusAndPC(self, pc, status, tokens):
        r, = tokens
        status[r] //= 2
        
        return pc + 1
    
class Triple(Instruction):
    def __init__(self):
        super().__init__("tpl", f"tpl {STR}", ["str"])
        
    def updateStatusAndPC(self, pc, status, tokens):
        r, = tokens
        status[r] *= 3
        
        return pc + 1
    
class Increment(Instruction):
    def __init__(self):
        super().__init__("inc", f"inc {STR}", ["str"])
        
    def updateStatusAndPC(self, pc, status, tokens):
        r, = tokens
        status[r] += 1
        
        return pc + 1
    
class Jump(Instruction):
    def __init__(self):
        super().__init__("jmp", f"jmp {NUM}", ["int"])
        
    def updateStatusAndPC(self, pc, status, tokens):
        offset, = tokens
        
        return pc + offset
    
class JumpIfEven(Instruction):
    def __init__(self):
        super().__init__("jie", f"jie {STR}, {NUM}", ["str", "int"])
        
    def updateStatusAndPC(self, pc, status, tokens):
        r,offset = tokens
        
        if status[r] % 2 == 0:
            return pc + offset
        else:
            return pc + 1
    
class JumpIfOne(Instruction):
    def __init__(self):
        super().__init__("jio", f"jio {STR}, {NUM}", ["str", "int"])
        
    def updateStatusAndPC(self, pc, status, tokens):
        r,offset = tokens
        
        if status[r] == 1:
            return pc + offset
        else:
            return pc + 1

class Computer:
    def __init__(self):
        self.status = None
        self.pc = None
        self.instrTypes = None
        self.program = None
        
    def loadInstructionTypes(self, instructions):
        self.instrTypes = list(instructions)
        
    def resetStatus(self):
        self.status = defaultdict(lambda: 0)
        
    def loadProgram(self, program):
        self.program = program
        self.resetStatus()
        self.pc = 0
        
    def executeProgram(self):
        cnt = 0
        while 0 <= self.pc < len(self.program):
            print(f"\nStep {cnt}")
            # fetch
            instruction = self.program[self.pc]
            print(f"    fetch: fetched '{instruction}' with pc {self.pc}")
            
            # decode
            selectedType = None
            for instrType in self.instrTypes:
                if instrType.match(instruction):
                    selectedType = instrType
                    break
            
            tokens = selectedType.getTokens(instruction)
            print(f"    decode: decoded to '{selectedType.name}' with tokens {tokens}")
            
            # execute
            self.pc = selectedType.updateStatusAndPC(self.pc, self.status, tokens)
            print(f"    execute: executed and pc ← {self.pc}")
            
            cnt += 1
        print("\nFinished")
        
    def getRegister(self, name):
        return self.status[name]
    
    def setRegister(self, name, value):
        self.status[name] = value

with open(FILE_NAME) as file:
    program = [line.strip() for line in file]
    
    
computer = Computer()

instructions = [Half(), Triple(), Increment(), Jump(), JumpIfEven(), JumpIfOne()]

computer.loadInstructionTypes(instructions)
computer.loadProgram(program)

computer.executeProgram()
out = computer.getRegister("b")

print("Part One: What is the value in register b when the program in your puzzle input is finished executing?")
print(out)


computer.loadProgram(program)
computer.setRegister("a", 1)
computer.executeProgram()
out = computer.getRegister("b")


print()
print("Part Two: what is the value in register b after the program is finished executing if register a starts as 1 instead?")
print(out)
