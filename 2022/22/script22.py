FILE_NAME = "example"
FILE_NAME = "input"

from itertools import groupby

DELTA_DIRECTION = {
    "R": 1,
    "L": -1,
}

class MyMap:
    def __init__(self, lst):
        self.offsets = [line.rfind(" ") + 1 for line in lst]
        self.lst = [line.strip() for line in lst]
        
    def getCell(self, x, y):
        if not (0 <= y < len(self.lst)) or not (0 <= x - self.offsets[y] < len(self.lst[y])):
            return None
        
        return self.lst[y][x - self.offsets[y]]
    
    def getWrappedLRCell(self, x, y, delta):
        line = self.lst[y]
        
        match delta:
            case -1: # left
                return (self.offsets[y] + len(line) - 1, line[-1])
            case 1: # right
                return (self.offsets[y], line[0])
            
    def getWrappedUDCell(self, x, y, delta):
        newY = None
        match delta:
            case -1: # up
                # default: len(self.lst) - 1, if the map extends all the way down to the end
                newY = next((y + 1 + ri for ri,offs in enumerate(self.offsets[y+1:]) if not (0 <= x - offs < len(self.lst[y + 1 + ri]))), len(self.lst)) - 1
            case 1: # down
                # default: 0, if the map extends all the way up to the start
                newY = next((y - 1 - ri for ri,offs in enumerate(reversed(self.offsets[:y])) if not (0 <= x - offs < len(self.lst[y - 1 - ri]))), -1) + 1
        
        #newY += 1
        
        return (newY, self.lst[newY][x - self.offsets[newY]])

def rotate(mymap, pos, direction, inst):
    direction += DELTA_DIRECTION[inst]
    direction %= 4
    
    return pos, direction


# lr = 1: right, lr = -1: left
def moveLR(mymap, pos, num, lr):
    #print(f"  moving LR by {num=}, {lr=} ({pos=})")
    x, y = pos
    for i in range(num):
        newX = x + lr
        cell = mymap.getCell(newX, y)

        # wrap around
        if cell == None:
            newX, cell = mymap.getWrappedLRCell(x, y, lr)
            
        # wall: return previous
        if cell == "#":
            break
            
        # open space: continue looping
        x = newX
        
    return (x,y)


# ud = 1: up, ud = -1: down
def moveUD(mymap, pos, num, ud):
    x, y = pos
    for i in range(num):
        newY = y + ud
        cell = mymap.getCell(x, newY)
        
        # wrap around
        if cell == None:
            newY, cell = mymap.getWrappedUDCell(x, y, ud)
            
        # wall: return previous
        if cell == "#":
            break
            
        # open space: continue looping
        y = newY
        
    return (x,y)


def move(mymap, pos, direction, num):
    match direction:
        # direction is 0 or 2 (right or left)
        case 0 | 2:
            return moveLR(mymap, pos, num, (1 if direction == 0 else -1)), direction
        # direction is 1 or 3 (down or up)
        case 1 | 3:
            return moveUD(mymap, pos, num, (1 if direction == 1 else -1)), direction
        
    # direction is


with open(FILE_NAME) as file:
    lst = [line[:-1] for line in file]
    
    *lst, _, instr = lst
    
    gb = groupby(instr, key=lambda x: True if '0' <= x <= '9' else False)
    instructions = [int("".join(g)) if k else "".join(g) for k,g in groupby(instr, key=lambda x: True if '0' <= x <= '9' else False)]
    
    
    mymap = MyMap(lst)
    
    pos = (mymap.offsets[0], 0)
    direction = 0 # right
    
    
    for inst in instructions:
        func = None
        match inst:
            case "L" | "R":
                #print(f"rotating to the to the {inst=}")
                func = rotate
                
            case num:
                #print(f"moving by {num=} to the {direction=}")
                func = move
                
        pos, direction = func(mymap, pos, direction, inst)
        #print(f" -> {pos=}, {direction=}")
    
    #print(*pos, direction)
    
    
    row = pos[1] + 1
    col = pos[0] + 1
    
    print("Part One: Follow the path given in the monkeys' notes. What is the final password?")
    print(1000 * row + 4 * col + direction)
    
