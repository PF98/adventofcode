FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    instr = [tuple(int(e) for e in line.strip().split()) for line in file]

tot = 0
for line in instr:
    diffs = tuple(b-a for b,a in zip(line,line[1:]))
    if not all(e > 0 for e in diffs) and not all(e < 0 for e in diffs):
        continue

    if not all(0 < abs(e) <= 3 for e in diffs):
        continue

    tot += 1


print("Part One:")
print(tot)


tot = 0
for line in instr:
    for i in range(len(line)):
        subline = (*line[:i], *line[i+1:])
        diffs = tuple(b-a for b,a in zip(subline,subline[1:]))

        if not all(e > 0 for e in diffs) and not all(e < 0 for e in diffs):
            continue

        if not all(0 < abs(e) <= 3 for e in diffs):
            continue

        tot += 1
        break
print()
print("Part Two")
print(tot)
