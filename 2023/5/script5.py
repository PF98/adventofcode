FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    lst = [line.strip() for line in file if line.strip()]

seeds,*lst = lst

seeds = [int(n) for n in seeds.split(": ")[1].split()]

maps = []

for line in lst:
    if line.endswith(" map:"):
        maps.append([])
        continue
    
    maps[-1].append(tuple(int(n) for n in line.split()))


values = seeds
for lmap in maps:
    newValues = []
    
    for v in values:
        for ds, ss, l in lmap:
            if ss <= v < ss + l:
                newValues.append(ds + (v - ss))
                break
        else:
            newValues.append(v)
    
    #print(newValues, lmap)
    values = newValues

#print(values)
    

t = 0
print("Part One:")
print(min(values))


values = list((a,b) for a,b in zip(seeds[::2], seeds[1::2]))
for lmap in maps:
    #print(f"{lmap = }")
    #break
    newValues = []
    
    while values:
        si,li = values.pop()
        for ds, ss, l in lmap:
            # [si, si+li-1] intersects [ss, ss+l-1]
            
            # disjoint
            if si+li <= ss or si >= ss+l:
                continue
                
            # interval completely within the mapping interval
            if si >= ss and si+li <= ss+l:
                newValues.append((ds + (si - ss), li))
                break
            
            # intersecting in [int_start, int_end]
            int_start = max(si, ss)
            int_end = min(si+li, ss+l)
            
            # the interval is too long on the left
            if int_start > si:
                values.append((si, int_start-si))
            
            # the interval is too long on the right
            if int_end < si+li:
                values.append((int_end, si+li - int_end))
            
            # the interval [int_start, int_end] is the one that should be mapped
            newValues.append((ds + (int_start - ss), int_end - int_start))
            break
        
        else:
            newValues.append((si, li))
        
        #print(f"{(si,li) = }, {values = }, {newValues = }")
        #input()
    #print(newValues, lmap)
    values = newValues

#for a,b in zip(seeds[::2], seeds[1::2]):
    #print(a,b)

#print(sum(b for a,b in zip(seeds[::2], seeds[1::2])))
print()
print("Part Two:")
print(min(a for a,_ in values))
print(len(values))
