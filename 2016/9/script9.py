from functools import reduce
import re

FILE_NAME = "example"
FILE_NAME = "input"

DECOMPRESSION_MARKER = "\((\d+)x(\d+)\)"


def decompress(code, depth = 0):
    #print(f"{'¦   ' * depth}called on {code}")
    matchesiter = re.finditer(DECOMPRESSION_MARKER, code)
    
    usedUpTo = 0
    totalLen = len(code)
    for match in matchesiter:
        pos,end = match.span()
        l = int(match.group(1))
        rep = int(match.group(2))
        
        matchLen = len(match.group(0))
        
        if pos < usedUpTo:
            continue
        
        usedUpTo = end + l
        totalLen -= matchLen + l
        
        totalLen += rep * decompress(code[end:end + l], depth + 1)
    
    #print(f"{'¦   ' * depth}<- returning {totalLen}")
    return totalLen





with open(FILE_NAME) as file:
    code = file.readline().strip()



#code = "ADVENT"
#code = "A(1x5)BC"
#code = "(3x3)XYZ"
#code = "A(2x2)BCD(2x2)EFG"
#code = "(6x1)(1x3)A"
#code = "X(8x2)(3x3)ABCY"

matchesiter = re.finditer(DECOMPRESSION_MARKER, code)

usedUpTo = 0
totalLen = len(code)
for match in matchesiter:
    pos,end = match.span()
    l = int(match.group(1))
    rep = int(match.group(2))
    
    matchLen = len(match.group(0))
    
    if pos < usedUpTo:
        continue

    usedUpTo = end + l
    totalLen += l * (rep - 1) - matchLen


print("Part One: What is the decompressed length of the file (your puzzle input)? Don't count whitespace.")
print(totalLen)

#code = "(3x3)XYZ"
#code = "X(8x2)(3x3)ABCY"
#code = "(27x12)(20x12)(13x14)(7x10)(1x12)A"
#code = "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"




out = decompress(code)




print()
print("Part Two: After you swipe your card, what code is the screen trying to display?")
print(out)
