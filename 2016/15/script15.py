from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"


def lcm(a, b):
    return (a*b) // math.gcd(a, b);

def calcDiscs(discs):
    num = reduce(lambda a,b: lcm(a,b), (size for size,_,_ in discs))
    s = None
    for size,curr,p in sorted(discs, reverse=True):
        if s is None:
            s = set(range(size - (curr + p) % size, num, size))
        else:
            s = set(n for n in s if (curr + n + p)%size == 0)
        #print()
        #print(1 in s)
        #print(len(s) if len(s) > 100 else s)
    return(min(s))
#print(min(s))


with open(FILE_NAME) as file:
    data = [line.split(" ") for line in file]

data = [(int(d[3]), int(d[11][:-2]), p+1) for p,d in enumerate(data)]


    

print("Part One: What is the first time you can press the button to get a capsule?")
print(calcDiscs(data))

data.append((11, 0, len(data)+1))

print()
print("Part Two: With this new disc, and counting again starting from time=0 with the configuration in your puzzle input, what is the first time you can press the button to get another capsule?")
print(calcDiscs(data))
