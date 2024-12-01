from functools import reduce
import re
import math

FILE_NAME = "example1"
FILE_NAME = "example2"
FILE_NAME = "input"

ROWS = 3
ROWS = 10
ROWS = 40
ROWS2 = 400000

def getTile(l,c,r):
    return "^" if l is not r else "."
    # "...", ".^.", "^^^"
    if l == r == "." or l == r == c:
        return "."
    
    if (l == "^") is not (r == "^"):
        return "^"

    return "."

with open(FILE_NAME) as file:
    line0 = [l == "^" for l in file.readline().strip()]

WIDTH = len(line0)

cnt = 0
line = line0
for r in range(ROWS):
    if r > 0:
        line = [(line[i-1] if i > 0 else False) is not (line[i+1] if i < WIDTH-1 else False) for i in range(len(line))]

    cnt += WIDTH - sum(line)
    #print(f"{line} => {c}")
print(cnt)

cnt2 = 0
line = line0
for r in range(ROWS2):
    if r > 0:
        line = [(line[i-1] if i > 0 else False) is not (line[i+1] if i < WIDTH-1 else False) for i in range(len(line))]

    cnt2 += WIDTH - sum(line)
    #print(f"{r: 6d} |{line}| => {c}")
    


print()
print("Part One: Starting with the map in your puzzle input, in a total of 40 rows (including the starting row), how many safe tiles are there?")
print(cnt)


print()
print("Part Two: How many safe tiles are there in a total of 400000 rows?")
print(cnt2)
