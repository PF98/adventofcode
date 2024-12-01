FILE_NAME = "example"
FILE_NAME = "input"

from functools import reduce
import math

DIGITS = ["=", "-", "0", "1", "2"]

BASE = 5

def parseSNAFU(s):
    return reduce(lambda a,b: BASE*a + b, (DIGITS.index(l) - 2 for l in s))

def getSNAFU(n):
    digits = math.ceil(math.log(n, BASE))
    
    based = []
    
    # add 2 to every one of the digits
    n += 2 * (BASE ** digits - 1) // (BASE - 1)
    
    # convert in base 5
    while n:
        n, d = divmod(n, BASE)
        based.append(d)
    
    # add 2 to every digit with position past "digits"
    based[digits:] = (b + 2 for b in based[digits:])
    
    return "".join(DIGITS[b] for b in reversed(based))

with open(FILE_NAME) as file:
    s = sum(parseSNAFU(line.strip()) for line in file)
    #print(s)
    
    
    print("Part One: The Elves are starting to get cold. What SNAFU number do you supply to Bob's console?")
    print(getSNAFU(s))
    
