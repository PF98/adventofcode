from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

CHANGE_COORD = [
    {
        "condition": lambda i,j,w,h: j>0,
        "coords": lambda i,j: (i, j-1)
    },
    {
        "condition": lambda i,j,w,h: j<w-1,
        "coords": lambda i,j: (i, j+1)
    },
    {
        "condition": lambda i,j,w,h: i>0,
        "coords": lambda i,j: (i-1, j)
    },
    {
        "condition": lambda i,j,w,h: i<h-1,
        "coords": lambda i,j: (i+1, j)
    },
]

with open(FILE_NAME) as file:
    hmap = [[int(n) for n in line if n != "\n"] for line in file]
    
    h = len(hmap)
    w = len(hmap[0]) 
    
    #print("\n".join("".join(str(l) for l in line) for line in hmap))
    
    
    count1 = 0
    minimums = []
    
    for i,row in enumerate(hmap):
        for j,num in enumerate(row):
            if j > 0 and row[j-1] <= num:
                continue
            if j < w - 1 and row[j+1] <= num:
                continue
            if i > 0 and hmap[i-1][j] <= num:
                continue
            if i < h-1 and hmap[i+1][j] <= num:
                continue
            
            count1 += 1 + num
            minimums.append((i,j));
            #print(f"({j},{i}) -> {num}")
    
    biggestBaisins = [0] * 3
    for low in minimums:
        unvisited = [low]
        visited = [[False] * w for _ in range(h)]
        visited[low[0]][low[1]] = True
        
        size = 0
        while len(unvisited) > 0:
            i,j = unvisited.pop()
            num = hmap[i][j]
            
            
            size += 1
            #print(f"  {i},{j}")
            for obj in CHANGE_COORD:
                cond = obj["condition"]
                func = obj["coords"]
                
                if cond(i, j, w, h):
                    ni,nj = func(i, j)
                    if not visited[ni][nj] and num <= hmap[ni][nj] < 9:
                        #print(f"  -> adding {ni},{nj} [{hmap[ni][nj]}]")
                        unvisited.append((ni,nj))
                        visited[ni][nj] = True
            
        
        #print(f"{low}: {size}")
        if size > biggestBaisins[0]:
            biggestBaisins[0] = size
            biggestBaisins.sort()
    
    
    print("Part One: What is the sum of the risk levels of all low points on your heightmap?")
    print(count1)
    
    print()
    print("Part Two: What do you get if you multiply together the sizes of the three largest basins?")
    print(reduce(lambda a,b : a*b, biggestBaisins, 1))
    

    
    
