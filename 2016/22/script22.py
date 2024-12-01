from functools import reduce
import re

FILE_NAME = "example"
FILE_NAME = "input"

DIRECTIONS = [
    (
        lambda x,y,w,h: y > 0,
        lambda x,y: (x, y-1)
    ),
    (
        lambda x,y,w,h: y < h-1,
        lambda x,y: (x, y+1)
    ),
    (
        lambda x,y,w,h: x > 0,
        lambda x,y: (x-1, y)
    ),
    (
        lambda x,y,w,h: x < w-1,
        lambda x,y: (x+1, y)
    ),
]
class Node:
    def __init__(self, t):
        x,y,size,used,avail,perc = t
        self.pos = (x,y)
        self.size = size
        self.used = used
        self.avail = avail
        self.perc = perc
        
    def __repr__(self):
        x,y = self.pos
        for cond, move in DIRECTIONS:
            if cond(x,y, maxx, maxy):
                nx,ny = move(x,y)
                if 0 < matrix[ny][nx].used < self.avail:
                    return "O"
                
        for cond, move in DIRECTIONS:
            if cond(x,y, maxx, maxy):
                nx,ny = move(x,y)
                if 0 < self.used < matrix[ny][nx].avail :
                    return "*"
                
        
        return "_" if self.used == 0 else "."
        return f"({self.used:3}/{self.size:3})"
    
def isViable(A, B):
    return 0 < A.used <= B.avail

regex = r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%"
with open(FILE_NAME) as file:
    data = [line.strip() for line in file]

maxx = None
maxy = None
lst = []
for line in data[2:]:
    match = re.match(regex, line)
    t = tuple(int(match.group(i+1)) for i in range(6))
    #print(t)
    x,y,*_ = t
    maxx = max(maxx, x) if maxx is not None else x;
    maxy = max(maxy, y) if maxy is not None else y;
    
    lst.append(Node(t))

cnt = 0
for i, A in enumerate(lst):
    for B in lst[i+1:]:
        if isViable(A,B):
            cnt += 1
        if isViable(B,A):
            cnt += 1
        
        
        
print("Part One: How many viable pairs of nodes are there?")
print(cnt)


matrix = [[None] * (maxx+1) for _ in range(maxy+1)]
for N in lst:
    x,y = N.pos
    matrix[y][x] = N
print("\n".join(" ".join(str(n) for n in r) for r in matrix))


def nodeToChar(node, x, y):
    if x == maxx and y == 0:
        return "G"
    
    if x == 0 and y == 0:
        return "O"
    
    if node.used == 0:
        return "_"
    
    return "."
print("-"*(2*len(matrix)-1))
print("\n".join(" ".join(nodeToChar(n, x, y) for x,n in enumerate(r)) for y,r in enumerate(matrix)))
print("-"*(2*len(matrix)-1))

print("\n".join(" ".join(f"{n.perc:2d}" for x,n in enumerate(r)) for y,r in enumerate(matrix)))
print("-"*(2*len(matrix)-1))
print("\n".join(" ".join("#" if n.perc > 80 else "+" if n.perc > 70 else "." for x,n in enumerate(r)) for y,r in enumerate(matrix)))

end = (maxx, 0)
start = (0,0)

#unscrambled = execute(program, instrs, "fbgdceah", reverse = True)

#print()
#print("Part Two: What is the un-scrambled version of the scrambled password fbgdceah?")
#print(', '.join(T + ''.join(s) + T for s in unscrambled))
