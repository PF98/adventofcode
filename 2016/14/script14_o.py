from functools import reduce
from collections import deque
import re
import hashlib

FILE_NAME = "example"
#FILE_NAME = "input"


with open(FILE_NAME) as file:
    salt = file.readline().strip()

i = 0;
prev = {}
prevCount = 0
done = False
outs = []
allCandidates = deque()
while True:
    string = f"{salt}{i}"
    res = hashlib.md5(string.encode()).hexdigest()
    
    #print()
    #print(f"{i:05}) {res}")
    #print(f"    prev: {{{prevCount}}} -> {prev}")
    #print(f"    allCandidates: {allCandidates}")
    
    # search for triples and quintuples (if necessary)
    firstTriple = None
    quintuples = set()
    for j,c in enumerate(res[:-2]):
        if firstTriple is None and c == res[j+1] == res[j+2]:
            firstTriple = c
            if prevCount == 0:
                break
            
        if prevCount > 0 and j <= len(res) - 5:
            chs = set(res[j:j+5]);
            if len(chs) == 1:
                for ch in chs:
                    if ch in prev:
                        quintuples.add(ch)
    
    #print(f"    firstTriple: {firstTriple}")
    #print(f"    quintuples : {quintuples}")
    
    #if firstTriple is not None or quintuples:
        #input()
    
    # check all of the quintuples found, if one ends the program
    # ch is always in prev, it's checked when it's added
    for ch in quintuples:
        #print(f"{i:05}) {res}")
        #print(f"       prev[ch]: {prev[ch]}")
        #print(f"    -> quintuple '{ch}' matched with ids {prev[ch]}")
        while prev[ch]:
            outs.append((prev[ch].pop(0), ch))
            prevCount -= 1
        
        outs.sort() # keep in ascending order
        
        # empty, can be removed
        if not prev[ch]:
            del prev[ch]
            
        #print(f"       outs is now {len(outs)} elements long. last is {outs[-1]}")
        #input()
        
    
    toDel = None
    if allCandidates and allCandidates[0][0] <= i - 1000:
        ind, ch, res = allCandidates.popleft()
        if len(outs) > 64 and ind > outs[-1][0]:
            print(f"exiting on index {i}")
            break
        if ch in prev and prev[ch][0] == ind:
            #print(f"    (discarded triple '{ch}' from id {ind})")
            prev[ch].pop(0)
            prevCount -= 1
            if not prev:
                del prev[ch]
        #else:
            #print(f"    (not discarded triple '{ch}' from id {ind})")
        #input()
        
    if toDel is not None:
        del prev[toDel]
    
    if firstTriple is not None:
        if firstTriple not in prev:
            prev[firstTriple] = []
        prev[firstTriple].append(i)
        prevCount += 1
        #print(f" incremented prevCount to {prevCount}")
        
        allCandidates.append((i, firstTriple, res))

    
    
    #input()
    i += 1

print("\n\n\n")
print(outs[:64])
print("\n\n\n")
print(outs[63][0])
#print("".join(c for i,c in outs[:64]))

#print("Part One: What is the fewest number of steps required for you to reach 31,39?")
#print(depth)


#print()
#print("Part Two: How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?")
#print(count)
