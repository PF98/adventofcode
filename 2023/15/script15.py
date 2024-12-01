FILE_NAME = "example"
FILE_NAME = "input"

from functools import reduce

with open(FILE_NAME) as file:
    data = file.readline().strip().split(",")
    
def HASH(s):
    return reduce(lambda acc,e: ((acc + ord(e)) * 17) & 0xFF, s, 0)

hashes = list(map(HASH, data))

print("Part One:")
print(sum(hashes))


boxes = [[] for _ in range(256)]
for instr in data:
    
    if instr[-1] == "-":
        label = instr[:-1]
    else:
        label,f = instr.split("=")
        f = int(f)
        
    box = boxes[HASH(label)]
    
    if instr[-1] == "-":
        for i,(l,_) in enumerate(box):
            if l == label:
                del box[i]
                break
    else:
        for i,(l,_) in enumerate(box):
            if l == label:
                box[i] = (l, f)
                break
        else:
            box.append((label, f))
    
    #print()
    #print(instr)
    #print("\n".join(f"{i} => {b}" for i,b in enumerate(boxes) if b))
    

#print(data)
tot = 0
for b,box in enumerate(boxes, start = 1):
    tot += b * sum(i * f for i,(_,f) in enumerate(box, start=1))

print()
print("Part Two:")
print(tot)
