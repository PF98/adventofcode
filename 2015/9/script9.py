from functools import reduce
import re
import math

FILE_NAME = "example"
#FILE_NAME = "input"

def findPath(matrix, objective, start = None, used = []):
    if len(matrix) == len(used):
        return (start,), 0
    
    
    shortest = None
    minPath = None
    for node in range(len(matrix)):
        if node in used or node == start:
            continue
        
        
        path, dist = findPath(matrix, objective, node, [*used, node])
        
        if start is not None:
            dist += matrix[start][node]
            #print(path)
            path = (start, *path)
        
        if shortest is None or objective(dist, shortest):
            minPath = path
            shortest = dist
    
    return minPath, shortest

with open(FILE_NAME) as file:
    # note: input only has 8 nodes and is a complete graph
    data = [line.strip() for line in file]
    
    size = math.ceil(math.sqrt(2 * len(data)))
    
    matrix = [[0] * size for _ in range(size)]
    
    places = {}
    placesNames = []
    placeCnt = 0
    
    for path in data:
        lhs,rhs = path.split(" = ")
        fr,to = lhs.split(" to ")
        dist = int(rhs)
        
        for p in [fr,to]:
            if p not in places:
                places[p] = placeCnt
                placeCnt += 1
                placesNames.append(p)
        
        matrix[places[fr]][places[to]] = dist
        matrix[places[to]][places[fr]] = dist
    
    
    
    
    path,dist = findPath(matrix, lambda dist, oldDist: dist < oldDist)
    
    print("Part One: What is the distance of the shortest route?")
    print(" -> ".join(placesNames[p] for p in path), end="")
    print(f" = {dist}")
    
    
    
    
    
    path,dist = findPath(matrix, lambda dist, oldDist: dist > oldDist)
    
    print()
    print("Part Two: What is the distance of the longest route?")
    print(" -> ".join(placesNames[p] for p in path), end="")
    print(f" = {dist}")
    
