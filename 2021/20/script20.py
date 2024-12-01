from functools import reduce
import re
import math
from PIL import Image

#FILE_NAME = "mexample"
#FILE_NAME = "example"
FILE_NAME = "input"


STEPS1 = 2
STEPS2 = 50


class Bounds:
    class Bound:
        def __init__(self):
            self.low = None
            self.high = None
            
        def use(self, v):
            if self.low is None or v < self.low:
                self.low = v
            if self.high is None or v > self.high:
                self.high = v
                
        def within(self, v):
            return self.low <= v <= self.high
                
        def getRange(self, inc):
            return range(self.low - inc, (self.high + inc) + 1)
        
        def length(self):
            return (self.high - self.low + 1)
        
        def __str__(self):
            return f"({self.low} -> {self.high})"
        
        def __repr__(self):
            return self.__str__()
            
            
    def __init__(self):
        self.x = self.Bound()
        self.y = self.Bound()
        
    def use(self, x, y):
        self.x.use(x)
        self.y.use(y)
        
    def within(self, x, y):
        return self.x.within(x) and self.y.within(y)
    
    def length(self, inc):
        return (self.x.length() + inc, self.y.length() + inc)
    
    def __str__(self):
        return f"x: {self.x}, y: {self.y}"
    
    def __repr__(self):
        return self.__str__()
    
class SparseMatrix:
    OFF = (0,0,0)
    ON = (255,255,255)
    def __init__(self, inverse = False):
        self.matrix = set()
        self.bounds = Bounds()
        self.inverse = inverse
        # invert if self.inverse for every boolean condition
        # a ^ 0 = a
        # a ^ 1 = ~a
    
    def rangeX(self, inc = 0):
        return self.bounds.x.getRange(inc)
    def rangeY(self, inc = 0):
        return self.bounds.y.getRange(inc)
    
    def put(self, x, y, value):
        # value = True and inverse
        # OR
        # value = False and not inverse
        # => save
        if value ^ self.inverse:
            self.matrix.add((x,y))
            self.bounds.use(x, y)
        
    def has(self, x, y):
        return ((x,y) in self.matrix) ^ self.inverse
    
    def draw(self, inc = 0):
        return "\n".join("".join("#" if self.has(x,y) else "." for x in self.rangeX(inc)) for y in self.rangeY(inc))
    
    def getImage(self, inc = 0):
        img = Image.new("RGB", self.bounds.length(inc), color=self.OFF if not self.inverse else self.ON)

        for yi,y in enumerate(self.rangeY(inc)):
            for xi,x in enumerate(self.rangeX(inc)):
                img.putpixel((xi,yi), self.ON if self.has(x,y) else self.OFF)
                
        return img
    
    def count(self):
        return len(self.matrix) * (-1 if self.inverse else 1)

def applyEnhancement(matrix, algStr, amount):    
    for _ in range(amount):
        # matrix is NOT inverse: newMatrix will only be inverse if 0 in algStr produces a lit pixel
        if not matrix.inverse:
            inverse = algStr[0]
        # matrix is inverse: newMatrix will only NOT be inverse if 511 (last) in algStr produces an off pixel
        else:
            inverse = algStr[-1]
        
        newMatrix = SparseMatrix(inverse)
        newBounds = Bounds()
        
        for y in matrix.rangeY(1):
            for x in matrix.rangeX(1):
                val = 0
                for j in range(-1, 1+1):
                    for i in range(-1, 1+1):
                        # i: direction of x,
                        # j: direction of y
                        val *= 2
                        if matrix.has(x+i, y+j):
                            val += 1
                
                newMatrix.put(x, y, algStr[val])
                    
        matrix = newMatrix
        #print("\n\n")
        #print(matrix.draw(2))
        #print(matrix.count())
        #print(matrix.bounds)
    return matrix


with open(FILE_NAME) as file:
    scanners = []
    
    data = [line.strip() for line in file]
    
    algStr = [ch == "#" for ch in data[0]]
    
    
    
    matrix = SparseMatrix()
    for y,line in enumerate(data[2:]):
        for x,ch in enumerate(line):
            if ch == "#":
                matrix.put(x,y, True)
    
    matrix = applyEnhancement(matrix, algStr, STEPS1)
    
    
    
    
    print("Part One: Start with the original input image and apply the image enhancement algorithm twice, being careful to account for the infinite size of the images. How many pixels are lit in the resulting image?")
    print(matrix.count())
    #print(matrix.draw())
    
    
    matrix = applyEnhancement(matrix, algStr, STEPS2 - STEPS1)
    
    
    print()
    print("Part Two: Start again with the original input image and apply the image enhancement algorithm 50 times. How many pixels are lit in the resulting image?")
    print(matrix.count())
    img = matrix.getImage()
    img.save("out.png")
    #print(matrix.draw())
