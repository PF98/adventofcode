from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    
    data = file.readline().strip().split(", ")
    

direc = 0
x = 0
y = 0
rep = None
visited = set([(0,0)])
for instr in data:
    rot = instr[0]
    num = int(instr[1:])
    
    #print(instr)
    #print(direc)
    #print(x,y)
    
    #print()
    
    direc = (direc + (1 if rot == "R" else -1)) % 4
    
    
    for _ in range(num):
        # up
        if direc == 0:
            y += 1
        # right
        elif direc == 1:
            x += 1
        # down
        elif direc == 2:
            y -= 1
        # left
        else:
            x -= 1
        
        if rep is None and (x,y) in visited:
            rep = (x,y)
        visited.add((x, y))
        
        
            
print("Part One: How many blocks away is Easter Bunny HQ?")
print(abs(x) + abs(y))

print()
print("Part Two: How many blocks away is the first location you visit twice?")
print(abs(rep[0]) + abs(rep[1]))
