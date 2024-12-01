import re

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
    
    def toC(self, tokens, variant, labelindex):
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
    
    def toC(self, tokens, variant, labelindex):
        x,y = tokens
        return [f"{y} = {x};"], None
    
# inc x y
class Increment(Instruction):
    def __init__(self):
        super().__init__("inc", f"inc @", [("str",)])
        
    def updateStatusAndPC(self, pc, status, tokens, variant):
        x, = tokens
        status[x] += 1
        
        return pc + 1

    def toC(self, tokens, variant, labelindex):
        x, = tokens
        return [f"{x} += 1;"], None


# dec x y
class Decrement(Instruction):
    def __init__(self):
        super().__init__("dec", f"dec @", [("str",)])
        
    def updateStatusAndPC(self, pc, status, tokens, variant):
        x, = tokens
        status[x] -= 1
        
        return pc + 1

    def toC(self, tokens, variant, labelindex):
        x, = tokens
        return [f"{x} -= 1;"], None
    
# jnz x y
class JumpNotZero(Instruction):
    def __init__(self):
        super().__init__("jnz", f"jnz @ @", [("str", "int"), ("int", "int")])
        
    def updateStatusAndPC(self, pc, status, tokens, variant):
        x,y = tokens
        
        return pc + y if status[x] != 0 else pc + 1

    def toC(self, tokens, variant, labelindex):
        x,y = tokens
        
        out = []
        if variant == 0:
            out.append(f"if ({x} != 0)")
            out.append(f"    goto l{labelindex};")
        elif variant == 1:
            if x != 0:
                out.append(f"goto l{labelindex};")
            
        return out, y



with open(FILE_NAME) as file:
    program = [line.strip() for line in file]


instructions = [Copy(), Increment(), Decrement(), JumpNotZero()]


out = []
labels = dict((k, []) for k,_ in enumerate(program))
finalLabels = []
labelindex = 0

for i,instruction in enumerate(program):
    #print(instruction)
    #print(labels)
    selectedType = None
    variant = None
    for instrType in instructions:
        variant = instrType.match(instruction)
        if variant is not False:
            selectedType = instrType
            break
    
    
    tokens = selectedType.getTokens(instruction, variant)

    
    lineInC, labelTo = selectedType.toC(tokens, variant, labelindex)
    
    if labelTo is not None:
        to = i+labelTo
        if to in labels:
            labels[to].append(f"l{labelindex}")
        else:
            finalLabels.append(f"l{labelindex}")
        
        labelindex += 1
    out.append(lineInC)


for ls,lines in zip([labels[k] for k in range(len(out))], out):
    #print(ls)
    for l in ls:
        print(f"{l}:")
        
    for l in lines:
        print(l)

for l in finalLabels:
    print(f"{l}:")

#print(out)
#print(labels)
#print(finalLabels)
