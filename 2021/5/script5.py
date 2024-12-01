from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

class Field:
    def __init__(self, size):
        self.field1 = [[0] * (size+1) for _ in range(size+1)]
        self.field2 = [[0] * (size+1) for _ in range(size+1)]
        
        self.count1 = 0
        self.count2 = 0
        
    def putLine(self, x1,y1,x2,y2):
        if x1 == x2:
            for y in range(min(y1,y2), max(y1,y2) + 1):
                self.put(x1, y, diag=False)
        elif y1 == y2:
            for x in range(min(x1,x2), max(x1,x2) + 1):
                self.put(x, y1, diag=False)
        else:
            for i in range(abs(x1-x2) + 1):
                x = ((x1 + i) if x1 < x2 else (x1 - i))
                y = ((y1 + i) if y1 < y2 else (y1 - i))
                self.put(x, y, diag=True)
                
    
    def put(self, x, y, diag):
        #print(f"({x},{y}), is{('' if diag else ' not')} diag")
        self.field2[y][x] += 1
        if self.field2[y][x] == 2:
            self.count2 += 1
            
        if diag:
            return
        
        self.field1[y][x] += 1
        if self.field1[y][x] == 2:
            self.count1 += 1
        
        
    def print1(self):
        return "\n".join(["".join([str(e) if e > 0 else "." for e in line]) for line in self.field1])
    
    def print2(self):
        return "\n".join(["".join([str(e) if e > 0 else "." for e in line]) for line in self.field2])
    

with open(FILE_NAME) as file:
    data = [[[int(c) for c in coord.split(",")] for coord in line.split(" -> ")] for line in file]
    
    maxSize = max([max([max(coord) for coord in line]) for line in data])
    
    field = Field(maxSize)
    
    
    for [x1,y1],[x2,y2] in data:
        field.putLine(x1, y1, x2, y2)
            
        
        #print(f"{x1},{y1} -> {x2},{y2}")
        #print(field.print2())
        #print("\n\n\n")
        
            
    print("Part One: At how many points do at least two lines overlap?")
    print(field.count1)
    
    print()
    print("Part Two: At how many points do at least two lines overlap?")
    print(field.count2)

    
    
