from functools import reduce
import re

FILE_NAME = "example"
FILE_NAME = "input"



MATRIX_W = 50
MATRIX_H = 6
#MATRIX_W = 7
#MATRIX_H = 3




class Instruction:
    def __init__(self, name, regex, paramNum):
        self.name = name
        self.regex = regex
        self.paramNum = paramNum
        
    def match(self, string):
        match = re.match(self.regex, string)
        if match is None:
            return False
        
        return tuple(int(match.group(i+1)) for i in range(self.paramNum))
        
    def apply(self, matrix):
        pass


class Rect(Instruction):
    def __init__(self):
        super().__init__("rect", "rect (\d+)x(\d+)", 2)
    
    def apply(self, matrix, params):
        A,B = params
        for y in range(B):
            matrix[y][:A] = [True] * A


class RotateRow(Instruction):
    def __init__(self):
        super().__init__("rotate row", "rotate row y=(\d+) by (\d+)", 2)
    
    def apply(self, matrix, params):
        A,B = params
        row = matrix[A]
        row[:] = (row[-B:] + row[:-B])
        
        
class RotateCol(Instruction):
    def __init__(self):
        super().__init__("rotate column", "rotate column x=(\d+) by (\d+)", 2)
    
    def apply(self, matrix, params):
        A,B = params
        
        col = [row[A] for y,row in enumerate(matrix)]
        col[:] = (col[-B:] + col[:-B])
        
        for y,val in enumerate(col):
            matrix[y][A] = val



def match(line, instrs):
    for instr in instrs:
        out = instr.match(line)
        if out is False:
            continue
        
        return instr, out
    return False


def execute(program, instrs, matrix):
    for line in program:
        out = match(line, instrs)
        if out is False:
            raise Exception()
        
        instr, params = out
        
        instr.apply(matrix, params)
        
    return sum(sum(row) for row in matrix)

with open(FILE_NAME) as file:
    data = [line.strip() for line in file]



matrix = [[False] * MATRIX_W for _ in range(MATRIX_H)]
instrs = [Rect(), RotateRow(), RotateCol()]

cnt = execute(data, instrs, matrix)

print("Part One: after you swipe your card, if the screen did work, how many pixels should be lit?")
print(cnt)




print()
print("Part Two: After you swipe your card, what code is the screen trying to display?")
print("\n".join("".join("█" if p else "░" for p in row) for row in matrix))
