from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"


TOTAL = 25
TOTAL = 150


def find(containers, amount, used = 0):
    #print(f"in with amount={amount}, used={used}")
    ways = []
    
    if amount == 0:
        #print("out with 1")
        return [[]]
    
    for i,c in enumerate(containers[used:]):
        u = i + used
        
        # containers has been sorted from smallest to biggest
        if amount < c:
            break
        
        newWays = find(containers, amount - c, u + 1)
        
        ways += ([c] + nw for nw in newWays)
    #print(f"out with {cnt}")
    return ways



with open(FILE_NAME) as file:
    containers = [int(line) for line in file]
    
    #containers.sort(reverse=True)
    containers.sort()
    #print(containers)
    
    ways = find(containers, TOTAL)
    
    print("Part One: Filling all containers entirely, how many different combinations of containers can exactly fit all 150 liters of eggnog?")
    print(len(ways))
    
    minWays = min(len(w) for w in ways)
    
    print()
    print("Part Two: Find the minimum number of containers that can exactly fit all 150 liters of eggnog. How many different ways can you fill that number of containers and still hold exactly 150 litres?")
    print(sum(1 for w in ways if len(w) == minWays))
