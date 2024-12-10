FILE_NAME = "example"
FILE_NAME = "input"

from collections import defaultdict
import itertools

with open(FILE_NAME) as file:
    field = [[int(e) for e in line.strip()] for line in file]

H = len(field)
W = len(field[0])

starts = [(r,c) for r,row in enumerate(field) for c,h in enumerate(row) if h == 0]

tot = 0
for start in starts:
    known = {start}
    for i in range(1,10):
        new_known = set()

        for r,c in known:
            tests = []
            if r > 0:
                tests.append((r-1,c))
            if r < H - 1:
                tests.append((r+1,c))
            if c > 0:
                tests.append((r,c-1))
            if c < W - 1:
                tests.append((r,c+1))

            for nr,nc in tests:
                if field[nr][nc] == i:
                    new_known.add((nr,nc))

        known = new_known

    tot += len(known)

print("Part One:")
print(tot)




tot = 0
known = {v: 1 for v in starts}
for i in range(1,10):
    new_known = defaultdict(int)

    for r,c in known:
        tests = []
        if r > 0:
            tests.append((r-1,c))
        if r < H - 1:
            tests.append((r+1,c))
        if c > 0:
            tests.append((r,c-1))
        if c < W - 1:
            tests.append((r,c+1))

        for nr,nc in tests:
            if field[nr][nc] == i:
                new_known[(nr,nc)] += known[(r,c)]

    known = new_known

print()
print("Part Two:")
print(sum(known.values()))
