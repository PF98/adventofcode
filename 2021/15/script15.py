from functools import reduce
import re
import math
import heapq
from PIL import Image, ImageDraw

FILE_NAME = "example"
FILE_NAME = "mexample"
FILE_NAME = "input"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def printPath(cave, prev, start, end):
    node = end
    path = [node]
    while node != start:
        node = prev[node[1]][node[0]]
        path.append(node)
    
    for y,row in enumerate(cave):
        for x,cell in enumerate(row):
            print(f"{bcolors.OKCYAN if (x,y) in path else ''}{str(cell)}{bcolors.ENDC if (x,y) in path else ''}", end="")
        print()


CHANGE_COORD = [
    {
        "condition": lambda x,y,w,h: y<h-1,
        "coords": lambda x,y: (x, y+1)
    },
    {
        "condition": lambda x,y,w,h: y>0,
        "coords": lambda x,y: (x, y-1)
    },
    {
        "condition": lambda x,y,w,h: x>0,
        "coords": lambda x,y: (x-1, y)
    },
    {
        "condition": lambda x,y,w,h: x<w-1,
        "coords": lambda x,y: (x+1, y)
    },
]


def dijkstra(cave, start, end):
    w = len(cave[0])
    h = len(cave)
    
    dist = [[None] * w for _ in range(h)]
    prev = [[None] * w for _ in range(h)]
    
    
    dist[start[1]][start[0]] = 0
    
    unvisited = [[True] * w for _ in range(h)]
    unvisitedCount = w*h;
    
    unvheap = [(dist[start[1]][start[0]], start)]
    
    while len(unvheap) > 0:
        #minDist = -1
        #node = None
        #for y,row in enumerate(unvisited):
            #for x,unv in enumerate(row):
                #if not unv:
                    #continue
                #if dist[y][x] >= 0 and (minDist == -1 or dist[y][x] < minDist):
                    #minDist = dist[y][x]
                    #node = (x,y)
        
        (nodeDist, node) = heapq.heappop(unvheap)
        #print("\nStepping: ")
        #print(f"  extracted node {node}, with nodeDist = {nodeDist}")
        
        # if we find that a node has a better distance, we don't remove its entry from the heap, we
        # just add a new one to its left in the heap: the later one will then be ignored
        if not unvisited[node[1]][node[0]]:
            continue
        
        unvisited[node[1]][node[0]] = False
        unvisitedCount -= 1
        
        #if node == end:
            #print(f"reached end with unvisitedCount = {unvisitedCount}")
        
        for obj in CHANGE_COORD:
            cond = obj["condition"]
            func = obj["coords"]
            
            if cond(node[0], node[1], w, h):
                nx,ny = func(node[0], node[1])
                if not unvisited[ny][nx]:
                    continue
                
                newDist = nodeDist + cave[ny][nx]
                if dist[ny][nx] is None or newDist < dist[ny][nx]:
                    dist[ny][nx] = newDist
                    prev[ny][nx] = node
                    heapq.heappush(unvheap, (dist[ny][nx], (nx,ny)))
                    #print(f"    pushed node {(nx,ny)} at distance {dist[ny][nx]}")

    
    #return dist[end[1]][end[0]]
    return dist, prev


with open(FILE_NAME) as file:
    
    
    cave = [[int(n) for n in line if n != "\n"] for line in file]
    #dist = dijkstra(cave, (0,0), (len(cave[-1])-1, len(cave)-1))
    
    start = (0,0)
    end = (len(cave[-1])-1, len(cave)-1)
    dist,prev = dijkstra(cave, start, end)
    
    #printPath(cave, prev, start, end)
    
    
    
    
    w = len(cave[0])
    h = len(cave)
    
    print("Part One: What is the lowest total risk of any path from the top left to the bottom right?")
    print(dist[end[1]][end[0]])
    
    
    
    
    cave2 = [[None] * w * 5 for _ in range(h * 5)]
    
    for y,row in enumerate(cave):
        for x,cell in enumerate(row):
            for i in range(5):
                for j in range(5):
                    num = cell + i + j
                    while num > 9:
                        num -= 9
                        
                    cave2[y + h * j][x + w * i] = num
    
    #print("\n".join("".join(str(n) for n in line) for line in cave2))
    
    
    start = (0,0)
    end = (len(cave2[-1])-1, len(cave2)-1)
    dist2, prev2 = dijkstra(cave2, (0,0), (len(cave2[-1])-1, len(cave2)-1))
    
    print()
    print("Part Two: what is the lowest total risk of any path from the top left to the bottom right?")
    print(dist2[end[1]][end[0]])
    
    #img = Image.new("RGB", tuple(c+1 for c in end), color="black")
    #node = end
    #img.putpixel(node, (255,255,255))
    #while node != start:
        ##print(node)
        #node = prev2[node[1]][node[0]]
        #img.putpixel(node, (255,255,255))
    
    #img.save("img.png")

    #printPath(cave2, prev2, start, end)

    

    

    
# IDEA for dijkstra
# keep dist as a matrix, also unvdist as a sorted list with bisect.insort
# for unvdist removing should be O(n), inserting is O(n) with insort
# if the node had no previous dist[][], then we insert with bisect.insort
# else we remove the previous entry with remove (dist[][], node) and insert
# once again with bisect.insert
