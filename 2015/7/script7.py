from functools import reduce
import re
import random
from enum import Enum
import heapq

FILE_NAME = "example"
FILE_NAME = "input"

WNAME = "[a-z]+"
NUM = "\d+"
TOKEN = f"({WNAME}|{NUM})"

class TokenType(Enum):
    NUMERIC = 1
    SIGNAL_NAME = 2

class Token:
    def __init__(self, typ, value):
        self.typ = typ
        self.value = value


class Signal:
    def __init__(self, name, oper, tokens):
        self.name = name
        self.neededFor = []
        self.requires = []
        self.value = None
        self.oper = oper
        self.tokens = tokens
        self.forced = False
    
    def clone(self):
        s = Signal(self.name, self.oper, [*self.tokens])
        s.neededFor = [*self.neededFor]
        s.requires = [*self.requires]
        s.value = self.value
        return s
        
    def setRequirement(self, name):
        self.requires.append(name)
        
    def setNeededFor(self, name):
        self.neededFor.append(name)
        
    def isSelfDetermining(self):
        return len(self.requires) == 0


    def getValue(self):
        return self.value

    def getDecValue(self):
        return bitsToDec(self.value) if self.value is not None else None

    def force(self, value):
        self.value = value
        self.forced = True
        self.requires = []

    def execute(self, signals, newToken = None, depth = 0):
        #print(f"{'    ' * depth}Called execute on {self.name} with newToken = {newToken} -> ", end = "")
        if len(self.requires) > 0:
            if newToken is None:
                #print("ERROR: still requires something")
                return
            else:
                self.requires.remove(newToken)
                #print("removed newToken, ", end = "")
                
            if len(self.requires) > 0:
                #print(f"still has {len(self.requires)} requirements to fulfill")
                return
        
        # if forced, the value is already set
        if not self.forced:
            # values for each token, should be all doable because self.requires is empty
            val = [getValue(signals, t) for t in self.tokens]
            
            dec = [bitsToDec(v) for v in val]
            
            func = MATCH_OPTIONS[self.oper][2]
            
            self.value = func(val, dec)
            
            #print(f"now calculated value to be {self.getDecValue()}")
        
        for name in self.neededFor:
            signals[name].execute(signals, self.name, depth + 1)
            


    def __str__(self):
        return f"Signal object {{ name: {self.name}, value: {self.getDecValue()}, requires: {self.requires}, needed for: {self.neededFor} }}"
    
    #def __lt__(self, other):
        #l1 = len(self.requires)
        #l2 = len(other.requires)
        
        #return l1 < l2 if l1 != l2 else len(self.neededFor) > len(other.neededFor)
        

# presented as a tuple containing:
# - regex,
# - number of TOKEN matches,
# - function to compute the value of the function given the getValue on the tokens
MATCH_OPTIONS = [
    (
        TOKEN,
        1,
        lambda val, dec: val[0]
    ),
    (
		f"{TOKEN} AND {TOKEN}",
        2,
        lambda val, dec: [1 if reduce(lambda a,b: a and b, bitpos) else 0 for bitpos in zip(*val)]
	),
    (
		f"{TOKEN} OR {TOKEN}",
		2,
        lambda val, dec: [1 if reduce(lambda a,b: a or b, bitpos) else 0 for bitpos in zip(*val)]
	),
    (
		f"NOT {TOKEN}",
		1,
        lambda val, dec: [1 if not bit else 0 for bit in val[0]]
	),
    (
		f"{TOKEN} LSHIFT {TOKEN}",
		2,
        lambda val, dec: val[0][dec[1]:] + [0] * dec[1]
	),
    (
		f"{TOKEN} RSHIFT {TOKEN}",
		2,
        lambda val, dec: [0] * dec[1] + val[0][:-dec[1]]
	),
]


def bitsToDec(bits):
    return reduce(lambda acc,b: acc*2 + b, bits, 0)


def getToken(tokenStr):
    m = re.match(WNAME, tokenStr)
    if m is None:
        return Token(TokenType.NUMERIC, tokenStr)
    else:
        return Token(TokenType.SIGNAL_NAME, tokenStr)


def getValue(signals, token):
    if token.typ == TokenType.NUMERIC:
        return [int(n) for n in f"{int(token.value):016b}"]
    elif token.typ == TokenType.SIGNAL_NAME:
        return signals[token.value].getValue()


with open(FILE_NAME) as file:
    variables = {}
    
    data = [line for line in file]
    
    signals = {}
    signalsNeededFor = {}
    
    
    for line in data:
        expr,var = line.strip().split(" -> ")
        for oper,(regex, ntokens, func) in enumerate(MATCH_OPTIONS):
            m = re.match(f"{regex}$", expr)
            if m is None:
                continue
            
            #print(line)
            #print(m)
            #print(ntokens)
            
            tokens = [getToken(m.group(i+1)) for i in range(ntokens)]
            signal = Signal(var, oper, tokens)
            
            # memorizes in the signal object the other signals which require him
            if var not in signalsNeededFor:
                signalsNeededFor[var] = []
                
            for s in signalsNeededFor[var]:
                signal.setNeededFor(s)
            
            for token in (t for t in tokens if t.typ == TokenType.SIGNAL_NAME):
                signal.setRequirement(token.value)
                
                if token.value not in signalsNeededFor:
                    signalsNeededFor[token.value] = []
                    
                signalsNeededFor[token.value].append(var)
                
                if token.value in signals:
                    signals[token.value].setNeededFor(var)
                
            signals[var] = signal
    
    
    originalSignals = { k: signals[k].clone() for k in signals }

    starts = [s for s in signals.values() if s.isSelfDetermining()]
    
    for signal in starts:
        signal.execute(signals)
        
    print("Part One: what signal is ultimately provided to wire a?")
    print(signals["a"].getDecValue())
    
    
    
    
    
    originalSignals["b"].force(signals["a"].getValue())
    
    
    signals = originalSignals
    starts = [s for s in signals.values() if s.isSelfDetermining()]

    for signal in starts:
        signal.execute(signals)
    
    print()
    print("Part Two:  What new signal is ultimately provided to wire a?")
    print(signals["a"].getDecValue())
    
