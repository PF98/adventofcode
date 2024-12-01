from functools import reduce
import re
import math
from collections import defaultdict

FILE_NAME = "example"
FILE_NAME = "input"


with open(FILE_NAME) as file:
    line = file.readline().strip()


match = re.match("To continue, please consult the code grid in the manual.  Enter the code at row (\d+), column (\d+).", line)
row = int(match.group(1))
col = int(match.group(2))

#startNum = 20151125
done = False
num = 20151125
#cnt = 1
#periodic = None
for r in range(2, row+col):
    for i in range(r):
        #cnt += 1
        num = (num * 252533) % 33554393
        
        #if periodic is None and num == startNum:
            #periodic = cnt
        
        if row == r-i and col == i+1:
            done = True
            break
    if done:
        break

print("Part One: What code do you give the machine?")
print(num)
