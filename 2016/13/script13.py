from functools import reduce
import re
import os
import time

FILE_NAME = "example"
FILE_NAME = "input"

START = (1,1)

DEST = (7,4)
DEST = (31,39)


def printMap(start, dest, visited = [], current = []):
    os.system("clear")
    xm,ym = (max(c) for c in zip(start, dest, *visited, *current))
    print("╔" + "═" * (xm+1) + "╗")
    for r in range(ym+1):
        print("║", end="")
        for c in range(xm+1):
            pos = (c, r)
            ch = " "
            if pos == start:
                ch = "S"
            elif pos == dest:
                ch = "D"
            elif isWall(pos, num):
                ch = "█"
            elif pos in current:
                ch = "O"
            elif pos in visited:
                ch = "░"
            print(ch, end="")
        print("║")
    print("╚" + "═" * (xm+1) + "╝")




cache = {}
def isWall(pos, num):
    if pos in cache:
        return cache[pos]
    
    x,y = pos
    # x*x + 3*x + 2*x*y + y + y*y
    #cache[pos] = (bin(x*x + 3*x + 2*x*y + y + y*y + num).count("1") % 2 != 0)
    cache[pos] = (bin(x * (x + 3 + 2*y) + y * (y + 1) + num).count("1") % 2 != 0)
    return cache[pos]


DIRECTIONS = [
    # left
    (
        lambda x,y: x > 0,
        lambda x,y: (x-1, y)
    ),
    # up
    (
        lambda x,y: y > 0,
        lambda x,y: (x, y-1)
    ),
    # right
    (
        lambda x,y: True,
        lambda x,y: (x+1, y)
    ),
    # down
    (
        lambda x,y: True,
        lambda x,y: (x, y+1)
    )
]
def bfs(start, dest, num, numberOfSteps):
    positions = {start} # set
    depth = 0
    visited = set()
    destDepth = None
    count2 = None
    
    while positions:
        printMap(start, dest, visited, positions)
        print(f"depth = {depth}, len: {len(positions)}")
        print(f"visited: {len(visited)}")
        #print(f"visited: {visited}")
        print(f"positions: {len(positions)}")
        #print(f"positions: {positions}")
        #input()
        time.sleep(0.1)
                
        newPositions = set()
        for pos in positions:
            visited.add(pos)
            if pos == dest:
                destDepth = depth
            
            for cond,func in DIRECTIONS:
                if not cond(*pos):
                    continue
                newPos = func(*pos)
                if not isWall(newPos, num) and newPos not in visited:
                    newPositions.add(newPos)
        
        if depth == numberOfSteps:
            count2 = len(visited)

        
        if destDepth is not None and count2 is not None:
            break
        
        positions = newPositions
        depth += 1
        
    return destDepth, count2


with open(FILE_NAME) as file:
    num = int(file.readline())



printMap(START, DEST)

depth, count = bfs(START, DEST, num, 50)



print("Part One: What is the fewest number of steps required for you to reach 31,39?")
print(depth)


print()
print("Part Two: How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?")
print(count)
