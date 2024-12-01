from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

STEPS = 10
STEPS = 100

DIRECTIONS = reduce(lambda a,b : a+b, [[(ai-1, aj-1) for ai in range(0,3) if not (ai-1 == 0 and aj-1 == 0)] for aj in range(0,3)], [])

with open(FILE_NAME) as file:
    grid = [[int(n) for n in line if n != "\n"] for line in file]
    
    size = len(grid)
    
    flashes = 0
    
    #print(f"Before any steps:")
    #print("\n".join("".join(str(l) for l in line) for line in grid))
    #print()
    s = 0
    while True:
        s += 1
        grid = [[n+1 for n in line] for line in grid]
        while True:
            #print(f"...in substep")
            #print("\n".join(",".join(f"{l:2}" for l in line) for line in grid))
            #print()
            changed = False
            for i,row in enumerate(grid):
                for j,num in enumerate(row):
                    if num <= 9:
                        continue
                    
                    if s <= STEPS:
                        flashes += 1
                    grid[i][j] = 0
                    for ai,aj in DIRECTIONS:
                        ni = i+ai
                        nj = j+aj
                        if not 0 <= ni < size or not 0 <= nj < size:
                            continue
                        
                        if grid[ni][nj] == 0:
                            continue
                        
                        grid[ni][nj] += 1
                        changed = True
            
            if not changed:
                break
        
        
        
        if all(all(n == 0 for n in line) for line in grid):
            synch = s
            break
        
        #print(f"After step {s+1}:")
        #print("\n".join("".join(str(l) for l in line) for line in grid))
        #print()
    
    
    print("Part One: How many total flashes are there after 100 steps?")
    print(flashes)
    
    print()
    print("Part Two: What is the first step during which all octopuses flash?")
    print(synch)
    

    
    
