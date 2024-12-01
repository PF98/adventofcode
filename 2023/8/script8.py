FILE_NAME = "example1_1"
FILE_NAME = "example1_2"
FILE_NAME = "example2"
FILE_NAME = "input"

import math
from functools import reduce

def lcm(*args):
    try:
        return math.lcm(*args)
    except:
        return math.prod(args) // reduce(math.gcd, args)
    
    

with open(FILE_NAME) as file:
    lst = [line.strip() for line in file]

directions,_,*lst = lst
graph = {}

for e in lst:
    fr,to = e.split(" = ")
    graph[fr] = tuple(to[1:-1].split(", "))
    
if not FILE_NAME.startswith("example2"):
    node = "AAA"
    c = 0
    while node != "ZZZ":
        for i,d in enumerate(directions, start=1):
            node = graph[node][0 if d == "L" else 1]
            if node == "ZZZ":
                break
        
        c += i
    
    print("Part One:")
    print(c)


if not FILE_NAME.startswith("example1"):
    # starts with all nodes ending in "A"
    nodes = [node for node in graph if node[-1] == "A"]
    
    periods = []
    
    for node in nodes:
        prev = [node]
        ends = []
        periodStart = None
        period = None
            
        c = 0
        while True:
            for i,d in enumerate(directions, start=1):
                node = graph[node][0 if d == "L" else 1]
                    
                if node[-1] == "Z":
                    ends.append(c + i)
            
            c += i
            # periodic
            if node in prev:
                period = len(prev) - (periodStart := prev.index(node))
                break
            
            prev.append(node)
        
        
        periods.append(period)
        
        #allEnds.append([])
        #for end in ends:
            #if end < (periodStart - 1) * len(directions):
                #allEnds[-1].append((end, None))
            #else:
                #allEnds[-1].append((end, period))
        
        
    # empirical observation: every starting point only ends up on only one 
    # ending value, immediately before starting the periodic loop again
    superPeriod = lcm(*periods)
    
    
    print()
    print("Part Two:")
    print(superPeriod * len(directions))
