FILE_NAME = "example"
FILE_NAME = "input"

import math

LIMITS = { "red": 12, "green": 13, "blue": 14 }

with open(FILE_NAME) as file:
    games = [line.strip().split(": ") for line in file]

def fits(cs, limits):
    c,color = cs.split(" ")
    return int(c) <= limits[color]

t = 0
for gs,ms in games:
    n = int(gs.split(" ")[1])
    
    if all(all(fits(cs, LIMITS) for cs in ss.split(", ")) for ss in ms.split("; ")):
        t += n
            
    
    
print("Part One:")
print(t)

p = 0
for gs,ms in games:
    n = int(gs.split(" ")[1])
    
    mincounts = {k: 0 for k in LIMITS}
    for ss in ms.split("; "):
        for cs in ss.split(", "):
            c,color = cs.split(" ")
            mincounts[color] = max(mincounts[color], int(c))
    
    p += math.prod(mincounts.values())


print()
print("Part Two:")
print(p)
