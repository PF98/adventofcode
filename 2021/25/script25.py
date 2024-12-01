from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    data = [line.strip() for line in file]


h = len(data)
w = len(data[0])
matrix = {}
for y,line in enumerate(data):
    for x,cell in enumerate(line):
        if cell != '.':
            matrix[x,y] = cell 


print(f"matrice {h}x{w}")

cnt = 0
out = None
while True:
    cnt += 1
    #print(f"step {cnt}")
    changed = False
    
    newMatrix = {}
    for pos, ch in matrix.items():
        x,y = pos
        if ch == ">":
            nx = (x + 1) % w
            ny = y
        else:
            nx,ny = x,y
        
        if (nx,ny) in matrix:
            newMatrix[x,y] = ch
        else:
            changed = True
            newMatrix[nx,ny] = ch
            
            
    matrix = newMatrix
    
    newMatrix = {}
    for pos, ch in matrix.items():
        x,y = pos
        if ch == "v":
            nx = x
            ny = (y + 1) % h
        else:
            nx,ny = x,y
        
        if (nx,ny) in matrix:
            newMatrix[x,y] = ch
        else:
            changed = True
            newMatrix[nx,ny] = ch
    
    
    
    matrix = newMatrix

    
    #print("\n".join("".join(matrix[x,y] if (x,y) in matrix else "." for x in range(w)) for y in range(h)))
    
    #input()
    if not changed:
        out = cnt
        break
        
print("Part One: Find somewhere safe to land your submarine. What is the first step on which no sea cucumbers move?")
print(cnt)

#print()
#print("Part Two: What is the smallest model number accepted by MONAD?")
#print(mem_z[0][0])
