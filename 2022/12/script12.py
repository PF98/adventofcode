FILE_NAME = "example"
FILE_NAME = "input"

import heapq

CHANGE_COORD = [
    (
        lambda x,y,w,h: y<h-1,
        lambda x,y: (x, y+1),
    ),
    (
        lambda x,y,w,h: y>0,
        lambda x,y: (x, y-1),
    ),
    (
        lambda x,y,w,h: x>0,
        lambda x,y: (x-1, y),
    ),
    (
        lambda x,y,w,h: x<w-1,
        lambda x,y: (x+1, y),
    ),
]

def dijkstra(area, start, end):
    w = len(area[0])
    h = len(area)
    
    dist = [[None] * w for _ in range(h)]
    prev = [[None] * w for _ in range(h)]
    
    
    dist[start[1]][start[0]] = 0
    
    unvisited = [[True] * w for _ in range(h)]
    unvisitedCount = w*h;
    
    unvheap = [(dist[start[1]][start[0]], start)]
    
    while len(unvheap) > 0:
        #print()
        #print("="*100)
        #print(len(unvheap), "->", unvheap)
        #print("visited:")
        #print("\n".join("".join("." if v else "x" for v in r) for r in unvisited))
        #print()
        
        (nodeDist, node) = heapq.heappop(unvheap)
        #print("\nStepping: ")
        #print(f"extracted node {node}, with nodeDist = {nodeDist}")
        
        # if we find that a node has a better distance, we don't remove its entry from the heap, we
        # just add a new one to its left in the heap: the later one will then be ignored
        if not unvisited[node[1]][node[0]]:
            continue
        
        unvisited[node[1]][node[0]] = False
        unvisitedCount -= 1
        
        nodeHeight = area[node[1]][node[0]]
        for cond,func in CHANGE_COORD:
            if cond(node[0], node[1], w, h):
                nx,ny = func(node[0], node[1])
                #print(f" -> reached node {(nx,ny)}:", end=" ")
                if not unvisited[ny][nx] or (area[ny][nx] - nodeHeight > 1):
                    #print("already visited" if not unvisited[ny][nx] else f"jump too high (\"{chr(ord('a')+nodeHeight)}\" -> \"{chr(ord('a')+area[ny][nx])}\" - {area[ny][nx] - nodeHeight} jump)")
                    continue
                
                newDist = nodeDist + 1
                if dist[ny][nx] is None or newDist < dist[ny][nx]:
                    dist[ny][nx] = newDist
                    prev[ny][nx] = node
                    heapq.heappush(unvheap, (dist[ny][nx], (nx,ny)))
                    #print(f"pushed node, with distance {dist[ny][nx]}")
                else:
                    #print(f"not pushed, because {newDist=}, while {dist[ny][nx]=}")
                    pass
    
    return dist, prev


def dijkstra2(area, start, end):
    def print(*args, **kwargs):
        pass
    w = len(area[0])
    h = len(area)
    
    dist = [[None] * w for _ in range(h)]
    prev = [[None] * w for _ in range(h)]
    
    
    dist[end[1]][end[0]] = 0
    
    unvisited = [[True] * w for _ in range(h)]
    unvisitedCount = w*h;
    
    unvheap = [(dist[end[1]][end[0]], end)]
    
    while len(unvheap) > 0:
        print()
        print("="*100)
        print(len(unvheap), "->", unvheap)
        print("visited:")
        print("\n".join("".join("." if v else "x" for v in r) for r in unvisited))
        print()
        
        (nodeDist, node) = heapq.heappop(unvheap)
        print(f"extracted node {node}, with nodeDist = {nodeDist}")
        
        # if we find that a node has a better distance, we don't remove its entry from the heap, we
        # just add a new one to its left in the heap: the later one will then be ignored
        if not unvisited[node[1]][node[0]]:
            continue
        
        unvisited[node[1]][node[0]] = False
        unvisitedCount -= 1
        
        nodeHeight = area[node[1]][node[0]]
        for cond,func in CHANGE_COORD:
            if cond(node[0], node[1], w, h):
                nx,ny = func(node[0], node[1])
                print(f" -> reached node {(nx,ny)}, {nodeHeight=}, {area[ny][nx]=}:", end=" ")
                if not unvisited[ny][nx] or (nodeHeight - area[ny][nx] > 1):
                    print("already visited" if not unvisited[ny][nx] else f"jump too high (\"{chr(ord('a')+nodeHeight)}\" -> \"{chr(ord('a')+area[ny][nx])}\" - {nodeHeight - area[ny][nx]} jump)")
                    continue
                
                newDist = nodeDist + 1
                if dist[ny][nx] is None or newDist < dist[ny][nx]:
                    dist[ny][nx] = newDist
                    prev[ny][nx] = node
                    heapq.heappush(unvheap, (dist[ny][nx], (nx,ny)))
                    print(f"pushed node, with distance {dist[ny][nx]}")
                else:
                    print(f"not pushed, because {newDist=}, while {dist[ny][nx]=}")
                    pass
    
    return dist, prev

def printPrev(area, prev, start, end):
    w = len(area[0])
    h = len(area)
    
    out = [["."]*w for _ in range(h)]
    
    out[start[1]][start[0]] = "S"
    
    old = end
    curr = prev[old[1]][old[0]]
    out[old[1]][old[0]] = "E"

    
    while curr != start:
        diff = tuple(o-c for c,o in zip(curr, old))
        ch = None
        
        match diff:
            case (-1,0):
                ch = "<"
            case (1,0):
                ch = ">"
            case (0,1):
                ch = "v"
            case (0,-1):
                ch = "^"
            case _:
                ch = "#"
        
        
        old = curr
        curr = prev[old[1]][old[0]]
        
        out[old[1]][old[0]] = ch
        #print(curr)
    
    
    print()
    print("\n".join("".join(row) for row in out))
    
    
def printPrev2(area, prev, start, end):
    w = len(area[0])
    h = len(area)
    
    out = [["."]*w for _ in range(h)]
    
    out[end[1]][end[0]] = "E"
    
    old = start
    curr = prev[old[1]][old[0]]
    out[old[1]][old[0]] = "M"

    
    while curr != end:
        diff = tuple(o-c for c,o in zip(curr, old))
        ch = None
        
        match diff:
            case (-1,0):
                ch = "<"
            case (1,0):
                ch = ">"
            case (0,1):
                ch = "v"
            case (0,-1):
                ch = "^"
            case _:
                ch = "#"
        
        
        old = curr
        curr = prev[old[1]][old[0]]
        
        out[old[1]][old[0]] = ch
        #print(curr)
    
    
    print()
    print("\n".join("".join(row) for row in out))



with open(FILE_NAME) as file:
    
    area = []
    
    start = None
    end = None
    
    for i,line in enumerate(file):
        
        row = list(line.strip())
        
        if "S" in row:
            start = (row.index("S"), i)
            row[start[0]] = "a"
        
        if "E" in row:
            end = (row.index("E"), i)
            row[end[0]] = "z"
        
        area.append([ord(l) - ord("a") for l in row])
            
    
    dist,prev = dijkstra(area, start, end)
    
    print("Part One: What is the fewest steps required to move from your current position to the location that should get the best signal?")
    print(dist[end[1]][end[0]])
    printPrev(area, prev, start, end)
    
    
    dist,prev = dijkstra2(area, start, end)
    #print(f"{dist=}")
    #print(f"{prev=}")
    
    minCell = None
    minDist = None
    for r,row in enumerate(area):
        for c,cell in enumerate(row):
            if cell == 0 and dist[r][c] is not None and (minDist is None or dist[r][c] < minDist):
                minCell = (c,r)
                minDist = dist[r][c]
    
    
    print()
    print("Part Two: What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?")
    print(minDist)
    printPrev2(area,prev,minCell,end)
