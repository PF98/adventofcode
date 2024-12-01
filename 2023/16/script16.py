FILE_NAME = "example"
FILE_NAME = "input"

from collections import defaultdict

class Field(list):
    def __init__(self, arg):
        super().__init__(arg)
        self.w = len(self)
        self.h = len(self[0])

with open(FILE_NAME) as file:
    field = Field(line.strip() for line in file)


def move(pos, direc, field):
    newPos = None
    if direc == 0: # right
        newPos = (pos[0], pos[1] + 1)
    elif direc == 1: # up
        newPos = (pos[0] - 1, pos[1])
    elif direc == 2: # left
        newPos = (pos[0], pos[1] - 1)
    elif direc == 3: # down
        newPos = (pos[0] + 1, pos[1])
    
    
    r,c = newPos
    if not (0 <= r < field.h) or not (0 <= c < field.w):
        return None
    
    
    cell = field[r][c]
    
    if cell == ".":
        return newPos, (direc,)
    elif cell == "|":
        # hits the flat side
        if direc == 0 or direc == 2:
            return newPos, (1, 3) # exits up and down
        # hits the transparent side
        else:
            return newPos, (direc,)
    elif cell == "-":
        # hits the flat side
        if direc == 1 or direc == 3:
            return newPos, (0, 2) # exits left and right
        # hits the transparent side
        else:
            return newPos, (direc,)
    elif cell == "/":
        if direc == 0 or direc == 2: # from left or right: turn to the left
            return newPos, ((direc + 1) % 4, )
        else: # from up or down: turn to the right
            return newPos, ((direc - 1) % 4, )
    elif cell == "\\":
        if direc == 0 or direc == 2: # from left or right: turn to the right
            return newPos, ((direc - 1) % 4, )
        else: # from left or right: turn to the left
            return newPos, ((direc + 1) % 4, )

direction = 0 # right
position = (0, -1) # entering from the top left

beams = [(position, direction)]
visited = defaultdict(set)

while beams:
    pos, direc = beams.pop()
    
    out = move(pos, direc, field)
    if out is None:
        continue
    
    newPos, newDirecs = out
    
    for newDirec in newDirecs:
        if newDirec not in visited[newPos]:
            visited[newPos].add(newDirec)
            beams.append((newPos, newDirec))
    
    
            
    
print("Part One:")
print(len(visited))


startingTiles = [
    # top row looking down
    *( ((-1, c), 3) for c in range(field.w) ),
    # bottom row looking up
    *( ((field.h, c), 1) for c in range(field.w) ),
    # left column looking right
    *( ((r, -1), 0) for r in range(field.h) ),
    # right column looking left
    *( ((r, field.w), 2) for r in range(field.h) ),
]

maxv = 0
i = 0
for position,direction in startingTiles:
    
    beams = [(position, direction)]
    visited = defaultdict(set)

    while beams:
        pos, direc = beams.pop()
        
        out = move(pos, direc, field)
        if out is None:
            continue
        
        newPos, newDirecs = out
        
        for newDirec in newDirecs:
            if newDirec not in visited[newPos]:
                visited[newPos].add(newDirec)
                beams.append((newPos, newDirec))

    maxv = max(maxv, len(visited))
    
    #print(f"{(i := i + 1)}/{len(startingTiles)}, {len(visited) = }")

print()
print("Part Two:")
print(maxv)
