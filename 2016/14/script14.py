from functools import reduce
from collections import deque
import re
import hashlib

FILE_NAME = "example"
FILE_NAME = "input"

PART2 = False
PART2 = True

def generateHash(string):
    n = 2017 if PART2 else 1
    for _ in range(n):
        string = hashlib.md5(string.encode()).hexdigest()
    
    return string

with open(FILE_NAME) as file:
    salt = file.readline().strip()

i = 0;
futureHashes = {}
cnt = 0
out = None
while True:
    print(f"i = {i}", end="\r")
    string = f"{salt}{i}"
    if i in futureHashes:
        res = futureHashes[i];
        del futureHashes[i];
    else:
        res = generateHash(string)
    
    
    # search for triples and quintuples (if necessary)
    firstTriple = None
    for j,c in enumerate(res[:-2]):
        if firstTriple is None and c == res[j+1] == res[j+2]:
            firstTriple = c
            break
    
    if firstTriple is not None:
        #print(f"  -> hypothesis: {i}, res = {res}, ft = {firstTriple}")
        found = False
        quintuple = firstTriple * 5
        for j in range(i+1, i+1001):
            if j not in futureHashes:
                futureHashes[j] = generateHash(f"{salt}{j}")
            
            if quintuple in futureHashes[j]:
                cnt += 1
                #print(f"found cnt = {cnt} at id {i}")
                if cnt == 64:
                    out = i
                break
            
    if out is not None:
        break
    
    i += 1
#print("".join(c for i,c in outs[:64]))

print("Part One: Given the actual salt in your puzzle input, what index produces your 64th one-time pad key?")
print(out)
#print(depth)


#print()
#print("Part Two: How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?")
#print(count)
