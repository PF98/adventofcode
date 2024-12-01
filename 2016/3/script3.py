from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"


def getPossible(triangles):
    cnt = 0
    for triangle in triangles:
        t = sorted(triangle)
        
        if sum(t[:2]) > t[2]:
            cnt += 1
    return cnt


with open(FILE_NAME) as file:
    
    data = [line.strip() for line in file]


triangles = [[int(n) for n in line.split(" ") if len(n.strip()) > 0] for line in data]
cnt = getPossible(triangles)

print("Part One: In your puzzle input, how many of the listed triangles are possible?")
print(cnt)


newTriangles = reduce(lambda a,b: a+b, (list(zip(*t)) for t in zip(triangles[:-2:3], triangles[1:-1:3], triangles[2::3])))
#print(newTriangles)
cnt = getPossible(newTriangles)


print()
print("Part Two: In your puzzle input, and instead reading by columns, how many of the listed triangles are possible?")
print(cnt)
