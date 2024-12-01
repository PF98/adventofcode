from functools import reduce
import re
import math


FILE_NAME = "example"
FILE_NAME = "input"

MAX = 9
MAX = 2**32-1


class Ranges:
    def __init__(self, a, b):
        self.ranges = [(a,b)]
        
    def remove(self, r):
        newRanges = []
        for i, rng in enumerate(self.ranges):
            newRanges.extend(Ranges.singleRemove(r, rng))
        self.ranges = newRanges
        
    def getFirst(self):
        return self.ranges[0][0]
    
    def getLength(self):
        return sum((b-a+1) for a,b in self.ranges)
    
    def singleRemove(r, rng):
        l,h = r
        a,b = rng
        
        out = []
        
        # no intersection
        #       a---b  |  a---b
        # l---h        |        l---h
        if h < a or l > b:
            return [rng]
        
        # a---b
        #    l---h
        # a-2        (2: l-1)
        if b >= l and a < l:
            out.append((a,l-1))
            
        #    a---b
        # l---h
        #      1-b   (1: h+1)
        if a <= h and b > h:
            out.append((h+1, b))
            
        # a---------b |    a---b
        #    l---h    | l---------h
        # a-2     1-b |      
        # nothing -> ok
        
        return out
    
    
with open(FILE_NAME) as file:
    data = [tuple(int(n) for n in line.split("-")) for line in file]

#print(data)

r = Ranges(0, MAX)
for d in data:
    r.remove(d)

#print(r.ranges)

print("Part One: what is the lowest-valued IP that is not blocked?")
print(r.getFirst())

    
print()
print("Part Two: How many IPs are allowed by the blacklist?")
print(r.getLength())
