from functools import reduce
import re

FILE_NAME = "example"
FILE_NAME = "input"

SIZE = 1000

with open(FILE_NAME) as file:
    grid = [[False]*SIZE for _ in range(SIZE)]
    grid2 = [[0]*SIZE for _ in range(SIZE)]
    
    for line in file:
        line = line.strip()
        m = re.search("turn on (\d+,\d+) through (\d+,\d+)", line)
        if m is not None:
            x1,y1 = (int(n) for n in m.group(1).split(","))
            x2,y2 = (int(n) for n in m.group(2).split(","))
            
            for y in range(y1, y2+1):
                grid[y][x1:x2+1] = [True] * (x2-x1+1)
                grid2[y][x1:x2+1] = (c+1 for c in grid2[y][x1:x2+1])
        
        m = re.search("turn off (\d+,\d+) through (\d+,\d+)", line)
        if m is not None:
            x1,y1 = (int(n) for n in m.group(1).split(","))
            x2,y2 = (int(n) for n in m.group(2).split(","))
            
            for y in range(y1, y2+1):
                grid[y][x1:x2+1] = [False] * (x2-x1+1)
                grid2[y][x1:x2+1] = (max(c-1,0) for c in grid2[y][x1:x2+1])

        
        
        m = re.search("toggle (\d+,\d+) through (\d+,\d+)", line)
        if m is not None:
            x1,y1 = (int(n) for n in m.group(1).split(","))
            x2,y2 = (int(n) for n in m.group(2).split(","))
            
            for y in range(y1, y2+1):
                grid[y][x1:x2+1] = (not c for c in grid[y][x1:x2+1])
                grid2[y][x1:x2+1] = (c+2 for c in grid2[y][x1:x2+1])

        
        
    
    print("Part One: After following the instructions, how many lights are lit?")
    print(sum(sum(1 for c in l if c) for l in grid))
    
    print()
    print("Part Two: What is the total brightness of all lights combined after following Santa's instructions?")
    print(sum(sum(l) for l in grid2))
    
