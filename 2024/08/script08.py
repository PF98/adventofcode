FILE_NAME = "example"
FILE_NAME = "input"

from collections import defaultdict
import math

with open(FILE_NAME) as file:
    lines = [line.strip() for line in file]

W = len(lines[0])
H = len(lines)

sparse = defaultdict(list)

for r,row in enumerate(lines):
    for c,l in enumerate(row):
        if l == ".":
            continue
        
        sparse[l].append((r,c))


antinodes = set()

for antennas in sparse.values():
    for i,(r1,c1) in enumerate(antennas):
        for (r2,c2) in antennas[i+1:]:
            for an in [(2*r1 - r2, 2*c1 - c2), (2*r2 - r1, 2*c2 - c1)]:
                if 0 <= an[0] < H and 0 <= an[1] < H:
                    antinodes.add(an)

print("Part One:")
print(len(antinodes))



antinodes = set()

for antennas in sparse.values():
    for i,(r1,c1) in enumerate(antennas):
        for (r2,c2) in antennas[i+1:]:
            # all antinodes of the form:
            # a1 + k (a2 - a1).
            # for the row coordinate, the conditions are:
            # 0 <= r1 + k (r2 - r1) < H, therefore
            #   kmin = -r1 / (r2 - r1)          if r2 > r1, else (H - 1 - r1) / (r2 - r1)
            #   kmax = (H - 1 - r1) / (r2 - r1) if r2 > r1, else r1 / (r2 - r1)
            # i.e., we get to -r1 <= k (r2 - r1) <= H-1-r1, therefore becoming:
            #  -> -r1/(r2 - r1) <= k <= (H-1-r1)/(r2 - r1)      if r2 > r1
            #  -> (H-1-r1)/(r2 - r1) <= k <= (H-1-r1)/(r2 - r1) if r2 > r1
            
            kmin = -math.inf
            kmax = math.inf
            
            if r2 > r1:
                kmin = max(kmin, math.ceil(-r1 / (r2 - r1)))
                kmax = min(kmax, math.floor((H - 1 - r1) / (r2 - r1)))
            elif r2 < r1:
                kmin = max(kmin, math.ceil((H - 1 - r1) / (r2 - r1)))
                kmax = min(kmax, math.floor(-r1 / (r2 - r1)))
            
            if c2 > c1:
                kmin = max(kmin, math.ceil(-c1 / (c2 - c1)))
                kmax = min(kmax, math.floor((W - 1 - c1) / (c2 - c1)))
            elif c2 < c1:
                kmin = max(kmin, math.ceil((W - 1 - c1) / (c2 - c1)))
                kmax = min(kmax, math.floor(-c1 / (c2 - c1)))

            antinodes.update((r1 + k * (r2 - r1), c1 + k * (c2 - c1)) for k in range(kmin, kmax + 1))

print()
print("Part Two:")
print(len(antinodes))
