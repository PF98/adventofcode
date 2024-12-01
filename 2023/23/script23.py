FILE_NAME = "example"
FILE_NAME = "input"

from collections import defaultdict

with open(FILE_NAME) as file:
    field = [line.strip() for line in file]

H = len(field)
W = len(field[0])

start = (0, field[0].index("."))
finish = (H-1, field[-1].index("."))

path = [start]
pathSplits = []

pathLens = []

def printField(field, path):
    print("\n".join("".join("O" if (r,c) in path else cell for c,cell in enumerate(row)) for r,row in enumerate(field)))

# walk along the path, with backtracking
while True:
    (r,c) = path[-1]
    
    
    neighbours = None
    if (r,c) == finish:
        pathLens.append(len(path) - 1)
    
        # backtrack
        if not pathSplits:
            break
        
        ind,neighbours = pathSplits.pop()
        path = path[:ind]
        
    else:
        neighbours = []
        
        if field[r][c] == "^":
            neighbours.append((r-1, c))
        elif field[r][c] == "v":
            neighbours.append((r+1, c))
        elif field[r][c] == ">":
            neighbours.append((r, c+1))
        elif field[r][c] == "<":
            neighbours.append((r, c-1))
        else:
            # up
            if r > 0:
                if field[r-1][c] == "." or field[r-1][c] == "^":
                    neighbours.append((r-1, c))
            # down
            if r < H-1:
                if field[r+1][c] == "." or field[r+1][c] == "v":
                    neighbours.append((r+1, c))
            # right
            if c > 0:
                if field[r][c-1] == "." or field[r][c-1] == "<":
                    neighbours.append((r, c-1))
            # left
            if c < W-1:
                if field[r][c+1] == "." or field[r][c+1] == ">":
                    neighbours.append((r, c+1))
            
            
        # not going back
        if len(path) > 1:
            neighbours = [n for n in neighbours if n != path[-2]]
        
    # one single neighbour: travel to it
    path.append(neighbours[0])
    
    # more neighbours
    if len(neighbours) > 1:
        pathSplits.append((len(path) - 1, neighbours[1:]))
            
    
    #print(f"path = {list(reversed(path))}")
    #print(f"{pathSplits = }")
    #print(f"{neighbours = }")
    #print()
    #print(f"{len(path) = }")
    #print(f"{pathLens = }")
    #print()
    #printField(field, path)
    #input()

#print(pathLens)

print("Part One:")
print(max(pathLens))
    
    
graph = defaultdict(dict)
visitedNeighbours = set()
    
startNode = None
finishNode = None
startLength = None
finishLength = None
    
nodes = [(start, start)]
# walk along the path, with backtracking
while nodes:
    (r0,c0),origin = nodes.pop()
    if (r0,c0) in visitedNeighbours:
        continue
    
    visitedNeighbours.add((r0,c0))
    path = [origin, (r0,c0)]
    # start travelling along the path
    while True:
        r,c = path[-1]
        
        if (r,c) == finish:
            finishNode = path[0]
            finishLength = len(path)-1
            break
        
        neighbours = []
    
        # up
        if r > 0 and field[r-1][c] != "#":
            neighbours.append((r-1, c))
        # down
        if r < H-1 and field[r+1][c] != "#":
            neighbours.append((r+1, c))
        # right
        if c > 0 and field[r][c-1] != "#":
            neighbours.append((r, c-1))
        # left
        if c < W-1 and field[r][c+1] != "#":
            neighbours.append((r, c+1))
            
            
        # not going back
        neighbours = [n for n in neighbours if n != path[-2]]
            
        # one single neighbour: travel to it
        
        # more neighbours: we have gotten to the end
        if len(neighbours) > 1:
            pathlen = len(path) - 1
            if path[0] == start:
                startNode = path[-1]
                startLength = pathlen - 1
                #break
            else:
                graph[path[0]][path[-1]] = pathlen
                graph[path[-1]][path[0]] = pathlen
            
            visitedNeighbours.add(path[-2])
            
            nodes.extend((neigh, path[-1]) for neigh in neighbours)
            break
            
        
    
        path.append(neighbours[0])
    


        
maxLength = 0

start = startNode
finish = finishNode

path = [start]
pathSplits = []
pathLengths = [0]

# walk along the path, with backtracking
while True:
    node = path[-1]
    
    neighbours = None
    if node != finishNode:
        neighbours = [n for n in list(graph[node]) if n not in path]
            
    if node == finishNode or not neighbours:
        maxLength = max(maxLength, pathLengths[-1])
    
        # backtrack
        if not pathSplits:
            break
        
        ind,neighbours = pathSplits.pop()
        path = path[:ind]
        pathLengths = pathLengths[:ind]
    
    # one single neighbour: travel to it
    path.append(neighbours[0])
    pathLengths.append(pathLengths[-1] + graph[path[-2]][path[-1]])
    
    # more neighbours
    if len(neighbours) > 1:
        pathSplits.append((len(path) - 1, neighbours[1:]))
            

    
    
#print(pathLens)
print()
print("Part Two:")
print(maxLength + startLength + finishLength)


