FILE_NAME = "example1"
FILE_NAME = "example2"
FILE_NAME = "input"


import itertools

def surfaceArea(data):
    count = 0
    for cube in data:
        for i in range(3): # index for every direction
            for pm in range(-1, 2, 2): # +1 and -1
                option = list(cube)
                option[i] += pm
                if tuple(option) not in data:
                    count += 1
                    
    return count


with open(FILE_NAME) as file:
    data = set(tuple(int(n) for n in line.strip().split(",")) for line in file)
    #print(data)
    
    
    
    print("Part One: What is the surface area of your scanned lava droplet?")
    print(surfaceArea(data))
    
    mins = tuple(min(e) for e in zip(*data))
    maxs = tuple(max(e) for e in zip(*data))
    
    
    allAirCubes = set()
    
    # start just outside of the "playing field"
    start = tuple(m-1 for m in mins)
    
    tovisit = [start]
    visited = set()
    
    while tovisit:
        aircube = tovisit.pop()
        #print(f"popped {aircube=}, {len(tovisit)=}")
        if all(minc <= c <= maxc for minc,c,maxc in zip(mins, aircube, maxs)):
            #print(f"added {aircube=}")
            allAirCubes.add(aircube)
        
        for i in range(3): # index for every direction
            for pm in range(-1, 2, 2): # +1 and -1
                option = list(aircube)
                option[i] += pm
                if not (mins[i] - 1 <= option[i] <= maxs[i] + 1):
                    continue
                
                t = tuple(option)
                if t not in data and t not in visited:
                    tovisit.append(t)
                    visited.add(t)
                
        
    #print(set(c for c in allAirCubes if ))
    #print(len(allAirCubes))
    
    
    filledData = {t for t in itertools.product(*(range(minc, maxc+1) for minc,maxc in zip(mins,maxs))) if t not in allAirCubes}
    
    #print(max(allAirCubes))
        #allAirCubes.append(
    
    
    #print(len(filledData))
    
    print()
    print("Part Two: What is the exterior surface area of your scanned lava droplet?")
    print(surfaceArea(filledData))
