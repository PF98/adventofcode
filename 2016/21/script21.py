from functools import reduce
import re

FILE_NAME = "example"
FILE_NAME = "input"

START = "abcde"
START = "abcdefgh"


class Instruction:
    TOKEN_TRANSPOSITION = {
        "str": lambda t: t,
        "int": lambda t: int(t)
    }

    def __init__(self, name, regex, tokenTypes):
        self.name = name
        self.regex = regex
        self.tokenTypes = tokenTypes
        
    def match(self, string):
        match = re.match(self.regex, string)
        if match is None:
            return False
        
        return tuple(self.TOKEN_TRANSPOSITION[typ](match.group(i+1)) for i,typ in enumerate(self.tokenTypes))
        
    def apply(self, string, params):
        pass
    
    def reverse(self, s, params):
        return self.apply(s, params)

class SwapPosition(Instruction):
    def __init__(self):
        super().__init__("swap position", "swap position (\d+) with position (\d+)", ("int", "int"))
        
    # same as reverse
    def apply(self, s, params):
        s = list(s)
        X,Y = params
        (s[X], s[Y]) = (s[Y], s[X])
        
        return [s]
        
        
class SwapLetter(Instruction):
    def __init__(self):
        super().__init__("swap letter", "swap letter ([a-z]+) with letter ([a-z]+)", ("str", "str"))
    
    # same as reverse
    def apply(self, s, params):
        s = list(s)
        X,Y = params
        Xi = s.index(X)
        Yi = s.index(Y)
        
        (s[Xi], s[Yi]) = (s[Yi], s[Xi])
        
        return [s]
        
    
        
class Rotate(Instruction):
    def __init__(self):
        super().__init__("rotate", "rotate (left|right) (\d+) steps?", ("str", "int"))
    
    def apply(self, s, params):
        s = list(s)
        direction,X = params
        
        if direction == "left":
            s[:] = s[X:] + s[:X]
        elif direction == "right":
            s[:] = s[-X:] + s[:-X]
        else:
            raise Exception(f"instruction Rotate: invalid direction {direction}")
        
        return [s]
        #(s[X], s[Y]) = (s[Y], s[X])
        
    def reverse(self, s, params):
        direction,X = params
        direction = ("left" if direction == "right" else ("right" if direction == "left" else direction))
        
        return self.apply(s, (direction, X))
        

class RotatePosition(Instruction):
    def __init__(self):
        super().__init__("rotate position", "rotate based on position of letter ([a-z]+)", ("str",))
    
    def apply(self, s, params):
        s = list(s)
        X, = params
        
        ind = s.index(X)
        n = (1 + ind + (1 if ind >= 4 else 0)) % len(s)
        
        # rotate right by n steps
        s[:] = s[-n:] + s[:-n]
        
        return [s]
        
    def reverse(self, s, params):
        s = list(s)
        X, = params
        
        oks = []
        ss = []
        # max rotation steps: 1 + length of s + eventually 1 more if ind >= 4
        for i in range(1+len(s)+1):
            s = s[1:] + s[:1] # rotate left once
            
            ind = s.index(X)
            n = (1 + ind + (1 if ind >= 4 else 0))
            
            #print(f"  rotations: {i+1}")
            #print(f"  s: {''.join(s)}")
            #print(f"  n: {n}")
            
            if i+1 == n:
                oks.append(n)
                ss.append(s)
                
        #print(oks)
        #print(ss)
        return ss
        
class Reverse(Instruction):
    def __init__(self):
        super().__init__("reverse", "reverse positions (\d+) through (\d+)", ("int", "int"))
    
    # same as reverse
    def apply(self, s, params):
        s = list(s)
        X,Y = params
        
        s[X:Y+1] = reversed(s[X:Y+1])
        
        return [s]
        
class Move(Instruction):
    def __init__(self):
        super().__init__("move", "move position (\d+) to position (\d+)", ("int", "int"))
    
    def apply(self, s, params):
        s = list(s)
        X,Y = params
        
        if X < Y:
            s[X:Y+1] = s[X+1:Y+1] + [s[X]]
        elif X > Y:
            s[Y:X+1] = [s[X]] + s[Y:X]
        else:
            raise Exception(f"instruction Move: invalid parameters X == Y (X: {X}, Y: {Y})")
        
        return [s]
        
    def reverse(self, s, params):
        X,Y = params
        
        return self.apply(s, tuple(reversed(params)))
        

def match(line, instrs):
    for instr in instrs:
        out = instr.match(line)
        if out is False:
            continue
        
        return instr, out
    return False


def execute(program, instrs, s, reverse = False):
    #print(s)
    ss = [list(s)]
    for line in (program if not reverse else reversed(program)):
        #print(line)
        out = match(line, instrs)
        if out is False:
            raise Exception("no matches")
        
        instr, params = out
        
        newss = []
        for s in ss:
            if not reverse:
                instrss = instr.apply(s, params)
            else:
                instrss = instr.reverse(s, params)
            #print(f"{''.join(s)} -> {instrss}")
            newss.extend(instrss)
        
        ss = newss
        
        
        #print(f"  -> {','.join(T + ''.join(s) + T for s in ss)}")
        #input()
    return ss


T = '"'

with open(FILE_NAME) as file:
    program = [line.strip() for line in file]



instrs = [SwapPosition(), SwapLetter(), Rotate(), RotatePosition(), Reverse(), Move()]

#execute(program, instrs, "deabc")
#print("\n\n")


scrambled = execute(program, instrs, START)

print("Part One: Given the list of scrambling operations in your puzzle input, what is the result of scrambling abcdefgh?")
print(','.join(T + ''.join(s) + T for s in scrambled))


unscrambled = execute(program, instrs, "fbgdceah", reverse = True)

print()
print("Part Two: What is the un-scrambled version of the scrambled password fbgdceah?")
print(', '.join(T + ''.join(s) + T for s in unscrambled))
