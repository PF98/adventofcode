from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"


WEIGHT = 100

CLASSES = ["children", "cats", "samoyeds", "pomeranians", "akitas", "vizslas", "goldfish", "trees", "cars", "perfumes"]
AMOUNTS = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1
}

def eq(machine, sue):
    return sue == machine
def gt(machine, sue):
    return sue > machine
def lt(machine, sue):
    return sue < machine


CHECKS = {
    "children": eq,
    "cats": gt,
    "samoyeds": eq,
    "pomeranians": lt,
    "akitas": eq,
    "vizslas": eq,
    "goldfish": lt,
    "trees": gt,
    "cars": eq,
    "perfumes": eq
}


with open(FILE_NAME) as file:
    
    sueNum1 = None
    sueNum2 = None
    
    for line in file:
        
        lhs, rhs = line.strip().split(": ", 1)
        
        m = re.match("Sue (\d+)", lhs)
        n = int(m.group(1))
        
        
        groups = [g.split(": ") for g in rhs.split(", ")]
        
        ok1 = all(int(am) == AMOUNTS[name] for name,am in groups)
        
        if ok1:
            sueNum1 = n
            
        ok2 = all(CHECKS[name](AMOUNTS[name], int(am)) for name,am in groups)
        
        if ok2:
            sueNum2 = n
        
            
    print("Part One: What is the number of the Sue that got you the gift?")
    print(sueNum1)
    
    print()
    print("Part Two: What is the number of the real Aunt Sue?")
    print(sueNum2)
    
