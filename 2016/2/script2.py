from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

CHARS = {
    "U": lambda x,y: (x,y-1),
    "D": lambda x,y: (x,y+1),
    "R": lambda x,y: (x+1,y),
    "L": lambda x,y: (x-1,y),
}

with open(FILE_NAME) as file:
    
    steps = [line.strip() for line in file]


nums = [str(s+1) for s in range(9)]
nums = [nums[i:i+3] for i in range(0,9,3)]
print(nums)



out = []
x,y = 1,1
for line in steps:
    for ch in line:
        nx,ny = CHARS[ch](x,y)
        if 0 <= nx < 3 and 0 <= ny < 3:
            x,y = nx,ny
    out.append(nums[y][x])

print("Part One: What is the bathroom code?")
print("".join(out))

nums2 = [[None, None, "1", None, None], [None, *(str(n) for n in range(2,5)), None], [*(str(n) for n in range(5, 10))], [None, *(chr(i + ord("A")) for i in range(3)), None], [None, None, "D", None, None]]
#print(nums2)
out = []
x,y = 0,2
for line in steps:
    for ch in line:
        nx,ny = CHARS[ch](x,y)
        if 0 <= nx < 5 and 0 <= ny < 5 and nums2[ny][nx] is not None:
            x,y = nx,ny
    out.append(nums2[y][x])

print("Part Two: Using the same instructions in your puzzle input, what is the correct bathroom code?")
print("".join(out))
