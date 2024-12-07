FILE_NAME = "example"
FILE_NAME = "input"

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


start = next((r,l.index("^")) for r,l in enumerate(lines) if "^" in l)
direction = 0
pos = start

visited = {}

while True:
    nr,nc = DIRECTIONS[direction](*pos)
    
    while 0 <= nr < H and 0 <= nc < W and lines[nr][nc] == "#":
        direction += 1
        direction %= len(DIRECTIONS)
        
        nr,nc = DIRECTIONS[direction](*pos)
    
    if pos not in visited:
        visited[pos] = set()
    visited[pos].add(direction)
    
    if not (0 <= nr < H) or not (0 <= nc < W):
        break
    
    pos = (nr,nc)
        



print("Part One:")
print(len(visited))



def check_loop(lines, pos, direction, visited, obstacles):
    new_visited = {}
    
    o_r,o_c = DIRECTIONS[direction](*pos)
    if not (0 <= o_r < H) or not (0 <= o_c < W) or (o_r, o_c) in obstacles or (o_r, o_c) in visited:
        return None
    
    while True:
        nr,nc = DIRECTIONS[direction](*pos)
        
        while 0 <= nr < H and 0 <= nc < W and (lines[nr][nc] == "#" or (nr == o_r and nc == o_c)):
            direction += 1
            direction %= len(DIRECTIONS)
            
            nr,nc = DIRECTIONS[direction](*pos)
            
        if not (0 <= nr < H) or not (0 <= nc < W):
            return None
        
        if pos in visited and direction in visited[pos]:
            return (o_r, o_c)
        if pos in new_visited and direction in new_visited[pos]:
            return (o_r, o_c)
        
        if pos not in new_visited:
            new_visited[pos] = set()
        new_visited[pos].add(direction)
        
        pos = (nr,nc)

tot = 0
obstacles = set()

pos = start
direction = 0

visited = {}

while True:
    nr,nc = DIRECTIONS[direction](*pos)
    
    while 0 <= nr < H and 0 <= nc < W and lines[nr][nc] == "#":
        direction += 1
        direction %= len(DIRECTIONS)
            
        nr,nc = DIRECTIONS[direction](*pos)
        
    if not (0 <= nr < H) or not (0 <= nc < W):
        break
    
    obst = check_loop(lines, pos, direction, visited, obstacles)
    if obst is not None:
        obstacles.add(obst)
        
    if pos not in visited:
        visited[pos] = set()
    visited[pos].add(direction)
    
    pos = (nr,nc)





print()
print("Part Two:")
print(len(obstacles))
