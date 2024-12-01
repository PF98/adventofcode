from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"

def findPath(matrix, objective, depth = 0, start = None, used = [], actualStart = None):
    #print(f"{'  ' * depth}with start = {start} and actualStart = {actualStart}...")
    if len(matrix) == len(used):
        #print(f"{'  ' * depth}return path = {(start,)}, {0}")
        return (start,), matrix[start][actualStart]
    
    
    shortest = None
    minPath = None
    for node in range(len(matrix)):
        if node in used or node == start:
            continue
        
        if start is None:
            actualStart = node
        path, dist = findPath(matrix, objective, depth+1, node, [*used, node], actualStart)
        if start is not None:
            dist += matrix[start][node]
            #print(path)
            path = (start, *path)
        
        if shortest is None or objective(dist, shortest):
            minPath = path
            shortest = dist
    
    #print(f"{'  ' * depth}return path = {minPath}, {shortest}")
    return minPath, shortest

with open(FILE_NAME) as file:
    # note: input only has 8 nodes and is a complete graph
    data = [line.strip() for line in file]
    
    size = math.ceil(math.sqrt(len(data)))
    
    matrix = [[0] * size for _ in range(size)]
    
    people = {}
    peopleNames = []
    peopleCnt = 0
    
    for path in data:
        m = re.match("([A-Za-z]+) would (gain|lose) (\d+) happiness units by sitting next to ([A-Za-z]+).", path)
        
        fr = m.group(1)
        to = m.group(4)
        
        direction = 1 if m.group(2) == "gain" else -1
        dist = direction * int(m.group(3))
        
        
        for p in [fr,to]:
            if p not in people:
                people[p] = peopleCnt
                peopleCnt += 1
                peopleNames.append(p)
        
        matrix[people[fr]][people[to]] += dist
        matrix[people[to]][people[fr]] += dist
    
    #print("\n".join(str(l) for l in matrix))
    
    
    path,dist = findPath(matrix, lambda dist, oldDist: dist > oldDist)
    print(path)
    
    print("Part One: What is the total change in happiness for the optimal seating arrangement of the actual guest list?")
    print(" -> ".join(peopleNames[p] for p in path), end="")
    print(f" = {dist}")
    
    
    
    matrix = [row + [0] for row in matrix] + [[0] * len(matrix[0])]
    peopleNames.append("You")
    #print("\n".join(str(l) for l in matrix))
    
    path,dist = findPath(matrix, lambda dist, oldDist: dist > oldDist)
    print()
    print("Part Two: What is the total change in happiness for the optimal seating arrangement that actually includes yourself?")
    print(" -> ".join(peopleNames[p] for p in path), end="")
    print(f" = {dist}")
    
