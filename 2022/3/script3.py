FILE_NAME = "example"
FILE_NAME = "input"

from itertools import groupby

def priority(letter):
    charnum = ord(letter)
    
    if ord("a") <= charnum <= ord("z"):
        return charnum - ord("a") + 1
    if ord("A") <= charnum <= ord("Z"):
        return charnum - ord("A") + 27
    
    raise Exception
    
with open(FILE_NAME) as file:
    lines = [line.strip() for line in file]


sumPrior = 0
for line in lines:
    halves = (line[:len(line)//2], line[len(line)//2:])
    
    common = set.intersection(*(set(l) for l in halves))
    sumPrior += sum(priority(l) for l in common)
    
print("Part One: Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?")
print(sumPrior)



chunks = [lines[i:i+3] for i in range(0, len(lines), 3)]
    
sumPrior2 = 0
for chunk in chunks:
    common = set.intersection(*(set(l) for l in chunk))
    sumPrior2 += sum(priority(l) for l in common)

print()
print("Part Two: Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?")
print(sumPrior2)
