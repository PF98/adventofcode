FILE_NAME = "example"
FILE_NAME = "input"

from functools import lru_cache

rows = []
with open(FILE_NAME) as file:
    lst = [line.strip().split(" ") for line in file]
    



RECORD = None
@lru_cache(None)
def countOccurrences2(brokens, i = 0):
    if not brokens:
        return 1 if "#" not in RECORD[i:] else 0
    
    leeway = sum(brokens) + len(brokens) - 1
    
    out = 0
    
    # try placing the next broken chain here:    
    for j in range(i, len(RECORD) - leeway + 1):
        if j > i and RECORD[j-1] == "#":
            break
        
        end = j + brokens[0]
        if all(c != "." for c in RECORD[j:end]) and (end == len(RECORD) or RECORD[end] != "#"):
            out += countOccurrences2(brokens[1:], end + 1)
    
    return out


tot = 0
for record,brokens in lst:
    brokens = tuple(int(n) for n in brokens.split(","))
    
    countOccurrences2.cache_clear()
    
    RECORD = record
    cnt = countOccurrences2(brokens)
    tot += cnt


print("Part One:")
print(tot)




tot = 0
c = 0
for record,brokens in lst:
    record = "?".join([record]*5)
    brokens = tuple(int(n) for n in brokens.split(","))*5
    
    
    countOccurrences2.cache_clear()
    
    RECORD = record
    cnt = countOccurrences2(brokens)
    tot += cnt


print()
print("Part Two:")
print(tot)
