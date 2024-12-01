FILE_NAME = "example"
FILE_NAME = "input"

from collections import Counter

with open(FILE_NAME) as file:
    instr = [tuple(int(e) for e in line.strip().split()) for line in file]


lists = list(zip(*instr))

print("Part One:")
print(sum(abs(a-b) for a,b in zip(*(sorted(e) for e in lists))))


count2 = Counter(lists[-1])

tot = 0
for n,c in Counter(lists[0]).items():
    if n in count2:
        tot += count2[n] * n * c

print()
print("Part Two")
print(tot)
