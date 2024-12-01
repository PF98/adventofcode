FILE_NAME = "example"
FILE_NAME = "input"

import itertools

freeCols = None
freeRows = set()

rows = []
with open(FILE_NAME) as file:
    for line in file:
        line = line.strip()
        if freeCols == None:
            freeCols = set(range(len(line)))
        
        for i,c in enumerate(line):
            if c == "#":
                freeCols.discard(i)
        
        if all(c == "." for c in line):
            freeRows.add(len(rows))
        rows.append(line)

def calc(delta):
    galaxies = []
    dr = 0
    for r,row in enumerate(rows):
        if r in freeRows:
            dr += (delta-1)
        dc = 0
        for c,cell in enumerate(row):
            if c in freeCols:
                dc += (delta-1)
            
            if cell == "#":
                galaxies.append((r+dr, c+dc))

    return sum(sum(abs(e1-e2) for e1,e2 in zip(a,b)) for a,b in itertools.combinations(galaxies, 2))

print("Part One:")
print(calc(2))



print()
print("Part Two:")
print(calc(1000000))
