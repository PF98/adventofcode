FILE_NAME = "example1"
FILE_NAME = "example2"
FILE_NAME = "input"

def moveTail(pos, tail):
    #print(f"{pos} -> {tail}")
    # one step at the time: dx,dy can only be -2 <= dx, dy <= 2
    match tuple((t - p) for p,t in zip(pos,tail)):
        case (dx,dy) if abs(dx) <= 1 and abs(dy) <= 1:
            return tail
        
        case (dx,dy) if abs(dx) <= 1 and abs(dy) == 2:
            return (pos[0], pos[1] + dy//2)
                    
        case (dx,dy) if abs(dx) == 2 and abs(dy) <= 1:
            return (pos[0] + dx//2, pos[1])
        
        case (dx,dy) if abs(dx) == 2 and abs(dy) == 2:
            return (pos[0] + dx//2, pos[1] + dy//2)
        
        case d:
            print(pos, tail, d)
            raise Exception(pos, tail, d)
        
def printMap(pos, tail, visited, W, H):
    for y in reversed(range(0,H)):
        for x in range(0,W):
            match (x,y):
                case t if t == pos:
                    c = "H"
                case t if t == tail:
                    c = "T"
                case (0,0):
                    c = "s"
                case t if t in visited:
                    c = "#"
                case _:
                    c = "."
            print(c, end="")
        print()
        
def printMap2(pos, tails, visited, W, H, dx=0,dy=0):
    for y in reversed(range(0,H)):
        for x in range(0,W):
            match (x+dx,y+dy):
                case t if t == pos:
                    c = "H"
                case t if t in tails:
                    c = tails.index(t) + 1
                case (0,0):
                    c = "s"
                case t if t in visited:
                    c = "#"
                case _:
                    c = "."
            print(c, end="")
        print()

with open(FILE_NAME) as file:
    instr = [line.strip().split(" ") for line in file]
    #print(instr)
    
    
    visited = set()
    pos = (0,0)
    tail = (0,0)
    visited.add(tail)
    
    #printMap(pos, tail, visited, 6,5)
    #print()
    
    for direc,num in instr:
        num = int(num)
        #print(f"== {direc} {num} ==")
        #print()
        
        for i in range(num):
            match direc:
                case "L": pos = (pos[0] - 1, pos[1])
                case "R": pos = (pos[0] + 1, pos[1])
                case "U": pos = (pos[0], pos[1] + 1)
                case "D": pos = (pos[0], pos[1] - 1)
            
            tail = moveTail(pos, tail)
            visited.add(tail)
            
            #printMap(pos, tail, visited, 6,5)
            #print()
    
        
    print("Part One: Simulate your complete hypothetical series of motions. How many positions does the tail of the rope visit at least once?")
    print(len(visited))
    
    
    visited = set()
    pos = (0,0)
    tails = [(0,0) for _ in range(9)]
    visited.add(tails[-1])
    
    #printMap2(pos, tails, visited, 26,21, -11, -5)
    #print()
    for direc,num in instr:
        num = int(num)
        #print(f"== {direc} {num} ==")
        #print()
        
        for i in range(num):
            match direc:
                case "L": pos = (pos[0] - 1, pos[1])
                case "R": pos = (pos[0] + 1, pos[1])
                case "U": pos = (pos[0], pos[1] + 1)
                case "D": pos = (pos[0], pos[1] - 1)
            
            newTails = [pos]
            for t in tails:
                newTails.append(moveTail(newTails[-1], t))
            
            tails[:] = newTails[1:]
            visited.add(tails[-1])
            
            #printMap2(pos, tails, visited, 26, 21, -11, -5)
            #print()
    
    print()
    print("Part Two: Simulate your complete series of motions on a larger rope with ten knots. How many positions does the tail of the rope visit at least once?")
    print(len(visited))
    #print(visited)
