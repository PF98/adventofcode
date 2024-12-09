FILE_NAME = "example"
FILE_NAME = "input"
#FILE_NAME = "test"

import heapq

with open(FILE_NAME) as file:
    data = [int(v) for v in file.readline().strip()]

filesystem = []

for i,length in enumerate(data):
    # even index: file
    if i % 2 == 0:
        filesystem.extend([i // 2] * length)
    else:
        filesystem.extend([-1] * length)


L = len(filesystem)

i = 0
for j,v in enumerate(reversed(filesystem)):
    if v < 0:
        continue
    
    while filesystem[i] >= 0:
        i += 1

    if i >= L - j - 1:
        break

    filesystem[i] = v
    filesystem[-j-1] = -1

tot = 0
for i,v in enumerate(filesystem):
    if v < 0:
        break

    tot += i*v

print("Part One:")
print(tot)





files = []
spaces = {i: [] for i in range(1,10)}
p = 0
for i,length in enumerate(data):
    # even index: file
    if i % 2 == 0:
        files.append((i // 2, p, length))
    elif length > 0:
        heapq.heappush(spaces[length], p)
    
    p += length


tot = 0
for i,pos,length in reversed(files):
    first_l = None
    for l in range(length, 10):
        if not spaces[l] or spaces[l][0] >= pos:
            continue
        
        if first_l is None or spaces[l][0] < spaces[first_l][0]:
            first_l = l
    
    if first_l is not None:
        pos = heapq.heappop(spaces[first_l])
        
        short_space = first_l - length
        if short_space != 0:
            heapq.heappush(spaces[short_space], pos + length)
        
    tot += i * length * (2 * pos + length - 1) // 2
    
print()
print("Part Two:")
print(tot)
