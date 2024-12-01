FILE_NAME = "example"
FILE_NAME = "input"


with open(FILE_NAME) as file:
    instr = [line.strip().split() for line in file]



def solve(positions, instr):
    rmin = min(t[0] for t in positions)
    cmin = min(t[1] for t in positions)
    rmax = max(t[0] for t in positions)
    cmax = max(t[1] for t in positions)

    rborders = sorted(set(t[0] for t in positions))
    cborders = sorted(set(t[1] for t in positions))

    area = [["."] * (2*len(cborders) - 1) for _ in range(2*len(rborders) - 1)]

    def findSlice(v, borders):
        return 2*borders.index(v)

    r,c = 0,0

    cnt = 0
    for direc,dist in instr:
        if direc == "R":
            for i in range(findSlice(c, cborders), findSlice(c+dist, cborders) + 1):
                area[findSlice(r, rborders)][i] = "#"
            c += dist
        elif direc == "L":
            for i in range(findSlice(c, cborders), findSlice(c-dist, cborders) - 1, -1):
                area[findSlice(r, rborders)][i] = "#"
            c -= dist
        elif direc == "U":
            for i in range(findSlice(r, rborders), findSlice(r-dist, rborders) - 1, -1):
                area[i][findSlice(c, cborders)] = "#"
            r -= dist
        elif direc == "D":
            for i in range(findSlice(r, rborders), findSlice(r+dist, rborders)):
                area[i][findSlice(c, cborders)] = "#"
            r += dist
            
        cnt += dist

            
    
    def flood(area, ri, ci, rborders, cborders):
        nodes = {(ri,ci)}
        
        W = len(area[0])
        H = len(area)
        
        rimax = cimax = -1
        rimin = H
        cimin = W
        
        cnt = 0
        
        while nodes:
            ri,ci = nodes.pop()
            area[ri][ci] = "#"
            
            rowSize = (1 if ri % 2 == 0 else rborders[(ri+1)//2] - rborders[ri//2] - 1)
            colSize = (1 if ci % 2 == 0 else cborders[(ci+1)//2] - cborders[ci//2] - 1)
            cnt += rowSize * colSize
            
            rimin = min(rimin, ri)
            cimin = min(cimin, ci)
            rimax = max(rimax, ri)
            cimax = max(cimax, ci)
            
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    if dr == 0 and dc == 0:
                        continue
                    
                    if not (0 <= ri+dr < H) or not (0 <= ci+dc < W):
                        continue
                    
                    if area[ri+dr][ci+dc] == ".":
                        nodes.add((ri+dr, ci+dc))
        
        if rimin == 0 or cimin == 0 or rimax == H-1 or cimax == W-1:
            return 0
        return cnt
        
    for ri,row in enumerate(area):
        for ci,cell in enumerate(row):
            if cell != ".":
                continue
            
            cnt += flood(area, ri, ci, rborders, cborders)
    return cnt



positions = [(0,0)]
newInstr = []
for direc, dist, _ in instr:
    dist = int(dist)
    
    r,c = positions[-1]
    if direc == "R":
        positions.append((r, c+dist))
    elif direc == "L":
        positions.append((r, c-dist))
    elif direc == "U":
        positions.append((r-dist, c))
    elif direc == "D":
        positions.append((r+dist, c))

    newInstr.append((direc, dist))

print("Part One:")
print(solve(positions, newInstr))





DIRECTIONS = "RDLU"

positions = [(0,0)]
newInstr = []
for _, _, hexnum in instr:
    direc = DIRECTIONS[int(hexnum[-2])]
    dist = int(hexnum[2:-2], 16)

    r,c = positions[-1]
    if direc == "R":
        positions.append((r, c+dist))
    elif direc == "L":
        positions.append((r, c-dist))
    elif direc == "U":
        positions.append((r-dist, c))
    elif direc == "D":
        positions.append((r+dist, c))
    
    newInstr.append((direc, dist))

print()
print("Part Two:")
print(solve(positions, newInstr))
