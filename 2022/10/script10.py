FILE_NAME = "example"
FILE_NAME = "input"

from functools import reduce
from advent_of_code_ocr import convert_6

CRT_W = 40
CRT_H = 6

class Computer:
    def __init__(self, saveStart, saveInterval):
        self.pc = 0
        self.regX = 1
        self.saveStart = saveStart
        self.savePos = saveStart
        self.saveInterval = saveInterval
        self.saved = []
        
        self.crt = [[False]*CRT_W for _ in range(CRT_H)]
    
    def checkSave(self):
        if self.pc >= self.savePos:
            self.saved.append(self.regX)
            self.savePos += self.saveInterval
    
    def drawCrt(self, num = 1):
        for i in range(num):
            (x,y) = ((self.pc + i) % CRT_W, (self.pc + i) // CRT_W)
            
            self.crt[y][x] = (self.regX - 1 <= x <= self.regX + 1)
    
    def noop(self):
        self.drawCrt()
        self.pc += 1
        self.checkSave()
    
    def addX(self, num):
        self.drawCrt(2)
        self.pc += 2
        self.checkSave()
        self.regX += num

    def getStrengthSum(self, end):
        return sum(p*x for p,x in zip(range(self.saveStart, end+1, self.saveInterval), self.saved))
    
    def printCrt(self):
        return "\n".join("".join("█" if c else "░" for c in row) for row in self.crt)

with open(FILE_NAME) as file:
    lst = [line.strip() for line in file]
    
    c = Computer(20, 40)
    
    for instr in lst:
        match instr.split():
            case ["noop"]:
                c.noop()
            case ["addx", num]:
                c.addX(int(num))
    
    
    
    print("Part One: Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles. What is the sum of these six signal strengths?")
    print(c.getStrengthSum(220))
    
    print()
    print("Part Two: Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?")
    print(c.printCrt())
    print("Converted:")
    print(convert_6(c.printCrt(), fill_pixel="█", empty_pixel="░"))
    
