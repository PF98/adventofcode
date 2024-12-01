from functools import reduce
import re
import math
import hashlib

FILE_NAME = "example"
FILE_NAME = "input"

DIRECTIONS = [
    (
        "U",
        lambda x,y,w,h: y > 0,
        lambda x,y: (x, y-1)
    ),
    (
        "D",
        lambda x,y,w,h: y < h-1,
        lambda x,y: (x, y+1)
    ),
    (
        "L",
        lambda x,y,w,h: x > 0,
        lambda x,y: (x-1, y)
    ),
    (
        "R",
        lambda x,y,w,h: x < w-1,
        lambda x,y: (x+1, y)
    ),
]

def bfsMaze(w, h, start, end, pwd):
    # list of tuples: start (tuple x,y) and path (string)
    unvisited = [(start, "")]
    depth = 0;
    
    first = None
    longest = None
    
    while unvisited:
        print(f"depth = {len(unvisited[0][1])}, unvisited: {len(unvisited)}")
        newUnvisited = []
        for pos, path in unvisited:
            if pos == end:
                if first is None:
                    first = path
                
                if longest is None or len(path) > longest:
                    longest = len(path)
                continue
            
            x,y = pos
            
            dirs = hashlib.md5(f"{pwd}{path}".encode()).hexdigest()
            for i,(L, cond, move) in enumerate(DIRECTIONS):
                if dirs[i] < "b" or not cond(x,y,w,h):
                    continue
                
                # from b to f and movable
                newUnvisited.append((move(x,y), path + L));
        
        unvisited = newUnvisited;
        #print(unvisited)
        #print(longest)
        #input()
    return first, longest

with open(FILE_NAME) as file:
    pwd = file.readline().strip()

#pwd = "ihgpwlah"
#pwd = "kglvqrro"

out = bfsMaze(4, 4, (0,0), (3,3), pwd)
    

print("Part One: What is the first time you can press the button to get a capsule?")
print(out)


#print()
#print("Part Two: With this new disc, and counting again starting from time=0 with the configuration in your puzzle input, what is the first time you can press the button to get another capsule?")
#print(calcDiscs(data))
