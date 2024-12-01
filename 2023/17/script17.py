FILE_NAME = "example1"
FILE_NAME = "example2_1"
FILE_NAME = "example2_2"
FILE_NAME = "input"


with open(FILE_NAME) as file:
    field = [list(map(int, line.strip())) for line in file]

W = len(field[0])
H = len(field)


def dijkstra(field, start, end, lmin, lmax):
    H = len(field)
    W = len(field[0])
    
    visited = [[set() for _ in range(W)] for _ in range(H)]
    # the starting node has always been visited
    visited[start[0]][start[1]].update(range(4))
    
    #nodes = [(0, *start, None)]
    nodes = {(*start, None): 0}

    #breakpoint()
    while nodes:
        #print(len(nodes), end="\r")
        
        #print(nodes)
        #outs = [[] for _ in range(H)]
        #for d in range(4):
            #for r in range(H):
                #for c in range(W):
                    #if d in visited[r][c]:
                        #outs[r].append("###")
                    #elif (r,c,d) in nodes:
                        #outs[r].append(f"{nodes[(r,c,d)]:^3}")
                    #else:
                        #outs[r].append(f"~{field[r][c]}~")
                #outs[r].append(" | ")
        
        
        #print("-+-" + "-".join("---" if e != " | " else "-+-" for e in outs[0]))
        #print(f" |{'right (>)'.center(W*4+1)} | {'up (^)'.center(W*4+1)} | {'left (<)'.center(W*4+1)} | {'down (v)'.center(W*4+1)} | ")
        #print("-+-" + "-".join("---" if e != " | " else "-+-" for e in outs[0]))
        #for ol in outs:
            #print(" | " + " ".join(ol))
            #print("-+-" + "-".join("---" if e != " | " else "-+-" for e in ol))
        #exit()
        
        minv = None
        mink = None
        for k,v in nodes.items():
            if minv is None or v < minv:
                mink = k
                minv = v
        del nodes[mink]
        #print(mink, minv, nodes)
        
        r, c, direc = mink
        visited[r][c].add(direc)
        
        dist = minv
        
        
        #print(f"active: {(r, c) = }, {direc = }, {dist = } | targeting {end = }")
        #input()
        
        
        # found the end:
        if (r,c) == end:
            return dist
            
        
        # direc is not left or right: we can go left or right up to 3 blocks
        if direc != 0 and direc != 2:
            # go left
            newDist = dist + sum(field[r][c-i] for i in range(1, min(lmin, 1+c)))
            for l in range(lmin, 1 + min(lmax, c)):
                newDist += field[r][c-l]
                if 2 in visited[r][c-l]:
                    continue
                           
                k = (r, c-l, 2)
                if k not in nodes or nodes[k] > newDist:
                    nodes[k] = newDist
            
            # go right
            newDist = dist + sum(field[r][c+i] for i in range(1, min(lmin, W-c)))
            for l in range(lmin, 1 + min(lmax, W-c-1)):
                newDist += field[r][c+l]
                if 0 in visited[r][c+l]:
                    continue
                
                k = (r, c+l, 0)
                if k not in nodes or nodes[k] > newDist:
                    nodes[k] = newDist
            
        
        # direc is not up or down: we can go up or down up to 3 blocks
        if direc != 1 and direc != 3:
            # go up
            newDist = dist + sum(field[r-i][c] for i in range(1, min(lmin, 1+r)))
            for l in range(lmin, 1 + min(lmax, r)):
                newDist += field[r-l][c]
                if 1 in visited[r-l][c]:
                    continue
                
                k = (r-l, c, 1)
                if k not in nodes or nodes[k] > newDist:
                    nodes[k] = newDist
            
            # go down
            newDist = dist + sum(field[r+i][c] for i in range(1, min(lmin, H-r)))
            for l in range(lmin, 1 + min(lmax, H-r-1)):
                newDist += field[r+l][c]
                if 3 in visited[r+l][c]:
                    continue
                
                k = (r+l, c, 3)
                if k not in nodes or nodes[k] > newDist:
                    nodes[k] = newDist
            
        

if not FILE_NAME.startswith("example2"):
    # distance, r, c, direction (0: right, 1: up, 2: left, 3: down)
    d = dijkstra(field, (0,0), (H-1,W-1), 1, 3)

    print("Part One:")
    print(d)

if not FILE_NAME.startswith("example1"):
    d = dijkstra(field, (0,0), (H-1,W-1), 4, 10)
    
    print()
    print("Part Two:")
    print(d)
