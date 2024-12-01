FILE_NAME = "example"
FILE_NAME = "input"

from functools import reduce

    
DISTANCES = [
    # up:
    lambda r,c,row,col: list(reversed(col[:r])),
    # right:
    lambda r,c,row,col: row[c+1:],
    # down:
    lambda r,c,row,col: col[r+1:],
    # left:
    lambda r,c,row,col: list(reversed(row[:c])),
]

with open(FILE_NAME) as file:
    field = [list(int(a) for a in line.strip()) for line in file]
    
    W = len(field[0])
    H = len(field)
    
    
    visible = [[False]*W for _ in range(H)]
    values = [[0]*W for _ in range(H)]
    
    for r,row in enumerate(field):
        for c,cell in enumerate(row):
            if r == 0 or r == H - 1 or c == 0 or c == W - 1:
                visible[r][c] = True
                values[r][c] = 0
                continue
            
            cellcol = list(field[ir][c] for ir in range(H))
            
            dists = []
            viss = []
            for distFunc in DISTANCES:
                sublist = distFunc(r,c,row,cellcol)
                l = len(sublist)
                dist = next((i for i,tree in enumerate(sublist) if cell <= tree), l)
                viss.append(dist == l)
                
                if dist < l:
                    dist += 1
                
                dists.append(dist)

            #print(f"({r},{c}), {dists=}")
            visible[r][c] = any(viss)
            values[r][c] = reduce(lambda a,b: a*b, dists, 1)
        #print()
    
    
    
    print("Part One: Consider your map; how many trees are visible from outside the grid?")
    print(sum(sum(r) for r in visible))
    
    print()
    print("Part Two: Consider each tree on your map. What is the highest scenic score possible for any tree?")
    print(max(max(r) for r in values))
