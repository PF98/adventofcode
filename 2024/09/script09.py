FILE_NAME = "example"
# FILE_NAME = "input"

with open(FILE_NAME) as file:
    data = [int(v) for v in file.readline().strip()]

filesystem = []

# count =

for i,length in enumerate(data):
    # even index: file
    if i % 2 == 0:
        filesystem.extend([i // 2] * length)
    else:
        filesystem.extend([-1] * length)


L = len(filesystem)

fs1 = list(filesystem)

i = 0
for j,v in enumerate(reversed(filesystem)):
    if v < 0:
        continue


    while fs1[i] >= 0:
        i += 1

    if i >= L - j - 1:
        break

    fs1[i] = v
    fs1[-j-1] = -1


tot = 0
for i,v in enumerate(fs1):
    if v < 0:
        break

    tot += i*v

print("Part One:")
print(tot)

