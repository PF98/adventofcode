from functools import reduce
from collections import Counter

FILE_NAME = "example"
FILE_NAME = "input"


with open(FILE_NAME) as file:
    
    data = [line.strip() for line in file]

summ = 0
northPoleId = None
for line in data:
    code,checksum = line[:-1].split("[")
    
    name, idStr = code.rsplit("-", 1)
    
    
    counts = Counter(name)
    if "-" in counts:
        del counts["-"]
    
    sortedCounts = list(sorted(((v, ord("z") - ord(l), l) for l,v in counts.items()), reverse=True))
    
    calcChecksum = "".join(l for _,_,l in sortedCounts[:len(checksum)])
    if calcChecksum == checksum:
        idNum = int(idStr)
        
        summ += idNum
        
        
        realName = "".join(chr(ord("a") + (ord(c) - ord("a") + idNum) % 26) if c != "-" else " " for c in name)
        
        
        if "north" in realName or "pole" in realName:
            northPoleId = idNum




print("Part One: What is the sum of the sector IDs of the real rooms?")
print(summ)



print()
print("Part Two: What is the sector ID of the room where North Pole objects are stored?")
print(northPoleId)
