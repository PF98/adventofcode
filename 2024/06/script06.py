FILE_NAME = "example"
FILE_NAME = "input"

from collections import defaultdict

# find the closest element of lst greater (not rev_dir) or smaller (rev_dir) than v
def find_next(lst, v, rev_dir):
    if not rev_dir:
        for e in lst:
            if e > v:
                return e
    else:
        for e in reversed(lst):
            if e < v:
                return e
    
    # leaves the bounding box
    return None

LONG_DIRECTIONS = [
    lambda obst_r, obst_c, r, c: (lambda o: (o+1, c) if o is not None else None)(find_next(obst_c[c], r, True)), # up
    lambda obst_r, obst_c, r, c: (lambda o: (r, o-1) if o is not None else None)(find_next(obst_r[r], c, False)), # right
    lambda obst_r, obst_c, r, c: (lambda o: (o-1, c) if o is not None else None)(find_next(obst_c[c], r, False)), # down
    lambda obst_r, obst_c, r, c: (lambda o: (r, o+1) if o is not None else None)(find_next(obst_r[r], c, True)), # left
]



DIRECTIONS = [
    lambda r,c: (r-1,c), # up
    lambda r,c: (r,c+1), # right
    lambda r,c: (r+1,c), # down
    lambda r,c: (r,c-1), # left
]

with open(FILE_NAME) as file:
    lines = [line.strip() for line in file]

H = len(lines)
W = len(lines[0])


obst_r = [tuple(c for c,l in enumerate(row) if l == "#") for r,row in enumerate(lines)]
obst_c = [tuple(r for r,row in enumerate(lines) if row[c] == "#") for c in range(W)]



start = next((r,l.index("^")) for r,l in enumerate(lines) if "^" in l)
direction = 0
pos = start

visited = defaultdict(set)

while True:
    nr,nc = DIRECTIONS[direction](*pos)
    
    while 0 <= nr < H and 0 <= nc < W and lines[nr][nc] == "#":
        direction = (direction + 1) % 4
        nr,nc = DIRECTIONS[direction](*pos)
    
    visited[pos].add(direction)
    
    if not (0 <= nr < H) or not (0 <= nc < W):
        break
    
    pos = (nr,nc)

print("Part One:")
print(len(visited))



def check_loop(lines, pos, direction, obstacle):
    visited = defaultdict(set)
    
    o_r, o_c = obstacle
    
    nobst_r = list(obst_r)
    nobst_c = list(obst_c)
    
    nobst_r[o_r] = tuple(sorted(nobst_r[o_r] + (o_c,)))
    nobst_c[o_c] = tuple(sorted(nobst_c[o_c] + (o_r,)))
    
    while True:
        pos = LONG_DIRECTIONS[direction](nobst_r, nobst_c, *pos)
        if pos is None:
            return False
        direction = (direction + 1) % 4
        
        if direction in visited[pos]:
            return True
        visited[pos].add(direction)


tot = 0

pos = start
direction = 0

visited = set()

while True:
    visited.add(pos)
    nr,nc = DIRECTIONS[direction](*pos)
    
    while 0 <= nr < H and 0 <= nc < W and lines[nr][nc] == "#":
        direction = (direction + 1) % 4
        nr,nc = DIRECTIONS[direction](*pos)
    
    if not (0 <= nr < H) or not (0 <= nc < W):
        break
    
    obst = (nr, nc)
    
    # valid obstacle
    if obst not in visited and check_loop(lines, pos, direction, obst):
        tot += 1
    
    pos = obst


print()
print("Part Two:")
print(tot)
