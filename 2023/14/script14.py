FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    field = [list(line.strip()) for line in file]
    
mfield = [row[:] for row in field]
moved = True
while moved:
    moved = False
    
    for r,row in enumerate(mfield):
        if r == 0:
            continue
        for c in range(len(row)):
            if row[c] == "O" and mfield[r-1][c] == ".":
                mfield[r-1][c] = "O"
                row[c] = "."
                moved = True
tot = sum(row.count("O") * (len(mfield) - r) for r,row in enumerate(mfield))

print("Part One:")
print(tot)

def cycle(field):
    H = len(field)
    W = len(field[0])
    
    
    # north
    moved = True
    while moved:
        moved = False
        for r,row in enumerate(field):
            if r == 0:
                continue
            for c in range(W):
                if row[c] == "O" and field[r-1][c] == ".":
                    field[r-1][c] = "O"
                    row[c] = "."
                    moved = True
    
    # west
    moved = True
    while moved:
        moved = False
        for c in range(1, W):
            for r in range(H):
                if field[r][c] == "O" and field[r][c-1] == ".":
                    field[r][c-1] = "O"
                    field[r][c] = "."
                    moved = True
    # south
    moved = True
    while moved:
        moved = False
        for r,row in enumerate(field[:-1]):
            for c in range(W):
                if row[c] == "O" and field[r+1][c] == ".":
                    field[r+1][c] = "O"
                    row[c] = "."
                    moved = True
        
    # east
    moved = True
    while moved:
        moved = False
        for c in range(W-1):
            for r in range(H):
                if field[r][c] == "O" and field[r][c+1] == ".":
                    field[r][c+1] = "O"
                    field[r][c] = "."
                    moved = True
    
    return field


def getNumber(field):
    out = 0
    for row in field:
        for cell in row:
            if cell == "#":
                continue
            
            out <<= 1
            if cell == "O":
                out += 1
    return out

N = 1000000000

tot = 0

prevnumbers = [0]
prevouts = [0]
for i in range(N):
    newfield = cycle([row[:] for row in field])
    newnum = getNumber(newfield)
    
    
    
    #print("\n".join(map("".join, newfield)))
    #print(i)
    #print(sum(row.count("O") * (len(newfield) - r) for r,row in enumerate(newfield)))
    #print(f"{newnum = }, {newnum in prevnumbers = }, {prevnumbers.index(newnum) if newnum in prevnumbers else ''}")
    #input()
    
    if newnum in prevnumbers:
        periodstart = prevnumbers.index(newnum)
        period = i+1 - periodstart
        
        finalindex = periodstart + (N - periodstart) % period
        
        tot = prevouts[finalindex]
        break
    
    prevnumbers.append(newnum)
    prevouts.append(sum(row.count("O") * (len(newfield) - r) for r,row in enumerate(newfield)))
    
    field = newfield


print()
print("Part Two:")
print(tot)
