FILE_NAME = "example1_1"
FILE_NAME = "example1_2"
FILE_NAME = "example2_1"
FILE_NAME = "example2_2"
FILE_NAME = "example2_3"
FILE_NAME = "example2_4"
FILE_NAME = "input"

import time

REPLACES = {
    "|": "║",
    "-": "═",
    "L": "╚",
    "J": "╝",
    "7": "╗",
    "F": "╔",
    "S": "█",
    "!": "▓",
    "?": "▒",
    "I": "I",
    "i": "i",
}
    
#def printField(f):
    #print("┌" + "─" * len(f[0]) + "┐")
    #print("\n".join("│" + "".join(REPLACES[e] if e in REPLACES else " " for e in row) + "│" for row in f))
    #print("└" + "─" * len(f[0]) + "┘")

    


CAN_MOVE_FUNCS = {
    "u": lambda r,c,w,h: r > 0,
    "d": lambda r,c,w,h: r < h-1,
    "l": lambda r,c,w,h: c > 0,
    "r": lambda r,c,w,h: c < w-1,
}
MOVE_FUNCS = {
    "u": lambda r,c: (r-1,c),
    "d": lambda r,c: (r+1,c),
    "l": lambda r,c: (r,c-1),
    "r": lambda r,c: (r,c+1),
}
LINKS = {
    "|": ("u", "d"),
    "-": ("l", "r"),
    "L": ("u", "r"),
    "J": ("u", "l"),
    "7": ("l", "d"),
    "F": ("r", "d"),
}
OPPOSITE = {
    "u": "d",
    "d": "u",
    "l": "r",
    "r": "l",
}

start = None
field = []
with open(FILE_NAME) as file:
    for line in file:
        line = line.strip()
        if start is None:
            try:
                start = (len(field), line.index("S"))
            except ValueError:
                pass
            
        field.append(list(line))

W = len(field[0])
H = len(field)

# PART ONE
if not FILE_NAME.startswith("example2"):
    nodes = []
    # valid neighbours of start:
    for movedir,canMove in CAN_MOVE_FUNCS.items():
        if not canMove(*start, W, H): 
            continue
        
        nr,nc = MOVE_FUNCS[movedir](*start)
        neigh = field[nr][nc]
        
        if neigh in LINKS and OPPOSITE[movedir] in LINKS[neigh]:
            nodes.append((nr,nc))
    
    prevNodes = [start, start]

    cnt = 1
    while True:
        if nodes[0] == nodes[1]:
            break
        
        newNodes = []
        # step one forward
        for (r,c),(pr,pc) in zip(nodes, prevNodes):
            links = LINKS[field[r][c]]
            for l in links:
                newnode = MOVE_FUNCS[l](r,c)
                if newnode == (pr,pc):
                    continue
                
                newNodes.append(newnode)
                break
            
        prevNodes,nodes = nodes,newNodes
        cnt += 1

    print("Part One:")
    print(cnt)



# PART TWO
if not FILE_NAME.startswith("example1"):
    # double the cells: the odd indices mean an actual cell, the ones with at 
    # least an even coordinate are the "inbetween" ones
    doubledField = [["."]*(2*W+1) for _ in range(2*H+1)]

    r,c = start
    doubledField[2*r+1][2*c+1] = "!"

    node = None        
    # valid neighbour of start:
    for movedir,canMove in CAN_MOVE_FUNCS.items():
        if not canMove(*start, W, H): 
            continue
        
        nr,nc = MOVE_FUNCS[movedir](*start)
        neigh = field[nr][nc]
        
        if neigh in LINKS and OPPOSITE[movedir] in LINKS[neigh]:
            node = (nr,nc)
            break


    prevNode = start

    while True:
        r,c = node
        pr,pc = prevNode
        doubledField[r + pr + 1][c + pc + 1] = "?" # ?: in-between nodes
        if node == start:
            break
        
        doubledField[2*r + 1][2*c + 1] = "!" # !: actual nodes
        
        # step one forward, travelling through the main chain
        newNode = None
        links = LINKS[field[r][c]]
        for l in links:
            newNode = MOVE_FUNCS[l](r,c)
            if newNode == (pr,pc):
                continue
            
            break
        
        prevNode,node = node,newNode

    # searching for the first ? that is the link between two nodes with a vertical 
    # pipe (|). it must be in an even non-zero and non-(2H) row (between the odd 
    # actual nodes) and in an odd column
    floodNodes = set()
    for r in range(2, 2*H, 2):
        for c in range(1, 2*W+1, 2):
            if doubledField[r][c] != "?":
                continue
            
            floodNodes.add((r,c+1))
            break
        if floodNodes:
            break

    cnt = 0
    # flood:
    while floodNodes:
        r,c = floodNodes.pop()
        if (r % 2 == 1) and (c % 2 == 1):
            cnt += 1
            doubledField[r][c] = "I"
        else:
            doubledField[r][c] = "i"
        
        for movedir,canMove in CAN_MOVE_FUNCS.items():
            if not canMove(r, c, 2*W+1, 2*H+1): 
                continue
            
            nr,nc = MOVE_FUNCS[movedir](r,c)
            
            if doubledField[nr][nc] == ".":
                floodNodes.add((nr,nc))
            
    print()
    print("Part Two:")
    print(cnt)
