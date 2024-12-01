FILE_NAME = "example"
FILE_NAME = "input"

import re
import math
from collections import defaultdict

width = None
with open(FILE_NAME) as file:
    numbers = []
    symbols = []
    for line in file:
        numbers.append([(int(m[0]), m.start(), m.end() - 1) for m in re.finditer("[0-9]+", line)])
        symbols.append({m.start(): m[0] for m in re.finditer("[^0-9.]", line.strip())})
        
        width = len(line.strip())
        

tot = 0    

symneigh = defaultdict(list)

for r,row in enumerate(numbers):
    for num, start, end in row:
        found = False
        # check in the previous row
        if r > 0:
            for c in range(start - 1, 2 + end):
                if c in symbols[r-1]:
                    found = True
                    if symbols[r-1][c] == "*":
                        symneigh[(r-1, c)].append(num)
        
        if r < len(numbers)-1:
            for c in range(start - 1, 2 + end):
                if c in symbols[r+1]:
                    found = True
                    if symbols[r+1][c] == "*":
                        symneigh[(r+1, c)].append(num)
        
        for c in (start-1, end+1):
            if c in symbols[r]:
                found = True
                if symbols[r][c] == "*":
                    symneigh[(r, c)].append(num)
        
        if found:
            tot += num
        #print(f"{num = }, {start = }, {end = } not matching")
            
    
    
    
print("Part One:")
print(tot)


print()
print("Part Two:")
print(sum(math.prod(neigh) for (r,c),neigh in symneigh.items() if len(neigh) == 2))
