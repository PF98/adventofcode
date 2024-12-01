from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"

ON = "#"
OFF = "."

STEPS = 5
STEPS = 100

def printl(l):
    print("\n".join("".join(ON if c else OFF for c in line[1:-1]) for line in l[1:-1]))

with open(FILE_NAME) as file:
    lights = [[False] + [c == ON for c in line.strip()] + [False] for line in file]
    row = [[False] * len(lights[0])]
    lights = row + lights + row
    
    buglights = [[*line] for line in lights]
    buglights[1][1] = True
    buglights[1][-2] = True
    buglights[-2][1] = True
    buglights[-2][-2] = True
    
    #print("Initial state:")
    #printl(lights)
    
    cnt = None
    bugcnt = None
    for n in range(STEPS):
        #neighs = [[0] * len(lights[0]) for _ in range(len(lights))]
        newLights = [[False] * len(lights[0]) for _ in range(len(lights))]
        newBuglights = [[False] * len(buglights[0]) for _ in range(len(buglights))]
        cnt = 0
        bugcnt = 0
        for x in range(1, len(lights) - 1):
            for y in range(1, len(lights) - 1):
                neighbours = 0
                bugneighbours = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if lights[y + j][x + i]:
                            neighbours += 1
                        if buglights[y + j][x + i]:
                            bugneighbours += 1
                            
                
                if lights[y][x]:
                    if 2 <= neighbours <= 3:
                        newLights[y][x] = True
                        cnt += 1
                else:
                    if neighbours == 3:
                        newLights[y][x] = True
                        cnt += 1
                        
                        
                if buglights[y][x]:
                    if 2 <= bugneighbours <= 3:
                        newBuglights[y][x] = True
                        bugcnt += 1
                else:
                    if bugneighbours == 3:
                        newBuglights[y][x] = True
                        bugcnt += 1
                #neighs[y][x] = neighbours
                
        lights = newLights
        buglights = newBuglights
        
        for (x,y) in [(1,1), (1,-2), (-2,1), (-2,-2)]:
            if not buglights[y][x]:
                buglights[y][x] = True
                bugcnt += 1

        #print(f"\nAfter {n+1} steps")
        #printl(buglights)
        
        #print("\n".join("".join(str(n) for n in line[1:-1]) for line in neighs[1:-1]))
        
    print("Part One: In your grid of 100x100 lights, given your initial configuration, how many lights are on after 100 steps?")
    print(cnt)
    
    #minWays = min(len(w) for w in ways)
    
    print()
    print("Part Two: In your grid of 100x100 lights, given your initial configuration, but with the four corners always in the on state, how many lights are on after 100 steps?")
    print(bugcnt)
