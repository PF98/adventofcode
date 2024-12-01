from functools import reduce
import re
import math
from collections import defaultdict

FILE_NAME = "example"
FILE_NAME = "input"





class Instruction:
    TOKEN_TRANSPOSITION = {
        "str": lambda t: t,
        "int": lambda t: int(t),
    }
    
    TOKEN_REGEX = dict((k, v.replace("\\", r"\\")) for k,v in {
        "str": r"([a-zA-Z]+)",
        "int": r"([+-]?\d+)",
    }.items())

    def __init__(self, name, regex, tokenTypes):
        self.name = name
        self.regexes = []
        for typeList in tokenTypes:
            newRegex = regex
            for typ in typeList:
                newRegex = re.sub(r"([^@]|^)@([^@]|$)", r"\1" + self.TOKEN_REGEX[typ] + r"\2", newRegex, count = 1)
            self.regexes.append(newRegex)
        self.tokenTypes = tokenTypes
    
    def match(self, instr):
        #print(self.regexes)
        for i,regex in enumerate(self.regexes):
            #print(f"  {regex}")
            match = re.match(regex, instr)
            if match is not None:
                return i
            
            #print("    no match")
            
        return False
        
    def getTokens(self, instr, variant):
        # match should have been called first
        match = re.match(self.regexes[variant], instr)
        tokens = [self.TOKEN_TRANSPOSITION[typ](match.group(i+1)) for i,typ in enumerate(self.tokenTypes[variant])]
        return tokens
        
    def updateStatusAndPC(self, pc, status, tokens):
        pass



# cpy x y
class Copy(Instruction):
    def __init__(self):
        super().__init__("cpy", f"cpy @ @", [("str", "str"), ("int", "str")])
        
    def updateStatusAndPC(self, pc, status, tokens, variant):
        x,y = tokens
        
        if variant == 0:
            status[y] = status[x]
        elif variant == 1:
            status[y] = x
        
        return pc + 1
    
# inc x y
class Increment(Instruction):
    def __init__(self):
        super().__init__("inc", f"inc @", [("str",)])
        
    def updateStatusAndPC(self, pc, status, tokens, variant):
        x, = tokens
        status[x] += 1
        
        return pc + 1

# dec x y
class Decrement(Instruction):
    def __init__(self):
        super().__init__("dec", f"dec @", [("str",)])
        
    def updateStatusAndPC(self, pc, status, tokens, variant):
        x, = tokens
        status[x] -= 1
        
        return pc + 1
    
# jnz x y
class JumpNotZero(Instruction):
    def __init__(self):
        super().__init__("jnz", f"jnz @ @", [("str", "int"), ("int", "int")])
        
    def updateStatusAndPC(self, pc, status, tokens, variant):
        x,y = tokens
        
        condition = ((status[x] if variant == 0 else x) != 0)
        return pc + y if condition else pc + 1




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
            #input()
            print(f"Step {cnt}", end="\r")
            # fetch
            instruction = self.program[self.pc]
            #print(f"    fetch: fetched '{instruction}' with pc {self.pc}")
            
            # decode
            selectedType = None
            variant = None
            for instrType in self.instrTypes:
                variant = instrType.match(instruction)
                if variant is not False:
                    selectedType = instrType
                    break
            
            tokens = selectedType.getTokens(instruction, variant)
            #print(f"    decode: decoded to '{selectedType.name}' (variant = {variant}) with tokens {tokens}")
            
            # execute
            self.pc = selectedType.updateStatusAndPC(self.pc, self.status, tokens, variant)
            #print(f"    execute: executed and pc ← {self.pc}")
            
            #print("  {")
            #print("\n".join(f"    {k} => {v}" for k,v in self.status.items()))
            #print("  }")
            #print()
            
            cnt += 1
        print("\nFinished")
        
    def getRegister(self, name):
        return self.status[name]
    
    def setRegister(self, name, value):
        self.status[name] = value

with open(FILE_NAME) as file:
    program = [line.strip() for line in file]
    
    
computer = Computer()

instructions = [Copy(), Increment(), Decrement(), JumpNotZero()]

computer.loadInstructionTypes(instructions)
computer.loadProgram(program)

computer.executeProgram()
out = computer.getRegister("a")

print("Part One: After executing the assembunny code in your puzzle input, what value is left in register a?")
print(out)


#computer.loadProgram(program)
#computer.setRegister("a", 1)
#computer.executeProgram()
#out = computer.getRegister("b")


#print()
#print("Part Two: what is the value in register b after the program is finished executing if register a starts as 1 instead?")
#print(out)
