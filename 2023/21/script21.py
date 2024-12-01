FILE_NAME = "example"
FILE_NAME = "input"

STEPS = 1
STEPS = 2
STEPS = 3
STEPS = 6
STEPS = 64

import itertools

start = None
field = []
with open(FILE_NAME) as file:
    for line in file:
        line = line.strip()
        if "S" in line:
            start = (len(field), line.index("S"))
        
        field.append(list(line))
            
W = len(field[0])
H = len(field)


prevPos = set()
positions = {start}

evens = 1
odds = 0
for s in range(1, 1 + STEPS):
    newPos = set()
    
    for r,c in positions:
        for nr,nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
            if nr < 0 or nr >= H or nc < 0 or nc >= W:
                continue
            
            if field[nr][nc] == "#":
                continue
            
            if (nr,nc) in prevPos or (nr,nc) in newPos:
                continue
            
            newPos.add((nr,nc))
            if s % 2 == 0:
                evens += 1
            else:
                odds += 1
            
    positions,prevPos = newPos,positions
    
    

print("Part One:")
print(evens if STEPS % 2 == 0 else odds)


STEPS2 = 26501365


MC = 1
M = 2*MC + 1

#def bigPrint(positions, prevPos):
    #print("╔" + ("═"*W + "╦")*(M-1) + "═"*W + "╗")
    #for br in range(-MC, 1 + MC):
        #outs = [["║"] for _ in range(H)]
        
        #for bc in range(-MC, 1 + MC):
            #for r,row in enumerate(field):
                #outs[r].append("".join(cmap(cell, r+br*W, c+bc*W, positions, prevPos) for c,cell in enumerate(row)))
                #outs[r].append("║")
        
        #print("\n".join("".join(row) for row in outs))
        
        #cl,cc,cr = "╠╬╣" if br < MC else "╚╩╝"
        #print(cl + ("═"*W + cc)*(M-1) + "═"*W + cr)



# FIRST JOB: propagate through a single cell, noting when it starts going outside
# to the left, the right, up or down (note the number of steps and the position)
# furthermore take note of the number of cells reached in each loop

prevPos = set()
positions = {start}

directions = ["left", "right", "up", "down"]

origins = {k: None for k in directions}
delays = {k: None for k in directions}

maincounts = [1]

for s in itertools.count(1):
    newPos = set()
    
    if len(maincounts) == 1:
        maincounts.append(0)
    else:
        maincounts.append(maincounts[-2])
    
    for r,c in positions:
        for nr,nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
            # take note of the first time going outside in each direction
            if nr < 0:
                if origins["up"] is None:
                    origins["up"] = (nr % H, nc)
                    delays["up"] = s
                continue
            if nr >= H:
                if origins["down"] is None:
                    origins["down"] = (nr % H, nc)
                    delays["down"] = s
                continue
            if nc < 0:
                if origins["left"] is None:
                    origins["left"] = (nr, nc % W)
                    delays["left"] = s
                continue
            if nc >= W:
                if origins["right"] is None:
                    origins["right"] = (nr, nc % W)
                    delays["right"] = s
                continue
            
            if field[nr][nc] == "#":
                continue
            
            if (nr,nc) in prevPos or (nr,nc) in newPos:
                continue
            
            newPos.add((nr,nc))
            
            maincounts[-1] += 1
            
    positions,prevPos = newPos,positions
    if not newPos:
        maincounts.pop()
        break

# the amount of steps that are reachable after an even/odd number of steps within
# a single cell
mainfulls = {}
if len(maincounts) % 2 == 0:
    # last is odd, the penultimate is even
    mainfulls["even"] = maincounts[-2]
    mainfulls["odd"] = maincounts[-1]
else:
    mainfulls["even"] = maincounts[-1]
    mainfulls["odd"] = maincounts[-2]



# SECOND JOB: loop over 4 different cells (each one represents one of the 
# left/right/up/down directions; each has its starting origin and step delay)
# the idea is to note the number of steps until we access the next cell in the 
# same direction (saved in periods) and the number of reachable cells after each 
# step that's taken
# furthermore, we take note of the first time we step into any of the 4 "corner" 
# cells (saving their origin and delay in origins2 and delays2)



counts = {k: [1] for k in directions}
periods = {k: None for k in directions}

directions2 = ["up left", "up right", "down left", "down right"]

origins2 = {k: None for k in directions2}
delays2 = {k: None for k in directions2}


RELATIONS = {
    "left": {
        "left": "period",
        "right": None,
        "up": "up left",
        "down": "down left",
    },
    "right": {
        "left": None,
        "right": "period",
        "up": "up right",
        "down": "down right",
    },
    "up": {
        "left": "up left",
        "right": "up right",
        "up": "period",
        "down": None,
    },
    "down": {
        "left": "down left",
        "right": "down right",
        "up": None,
        "down": "period",
    },
}


# loop over all of the left/right/up/down squares
prevPos = {k: set() for k in directions}
positions = {k: {origins[k]} for k in directions}

for s in itertools.count(1):
    newPos = {k: set() for k in directions}
    
    for k in directions:
        if len(counts[k]) == 1:
            counts[k].append(0)
        else:
            counts[k].append(counts[k][-2])
        for r,c in positions[k]:
            for nr,nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
                if nr < 0:
                    rel = RELATIONS[k]["up"]
                    if rel == "period":
                        if periods["up"] is None:
                            periods["up"] = s
                    elif rel is not None and origins2[rel] is None:
                        origins2[rel] = (nr % H, nc % W)
                        delays2[rel] = s + delays[k]
                    continue
                if nr >= H:
                    rel = RELATIONS[k]["down"]
                    if rel == "period":
                        if periods["down"] is None:
                            periods["down"] = s
                    elif rel is not None and origins2[rel] is None:
                        origins2[rel] = (nr % H, nc % W)
                        delays2[rel] = s + delays[k]
                    continue
                if nc < 0:
                    rel = RELATIONS[k]["left"]
                    if rel == "period":
                        if periods["left"] is None:
                            periods["left"] = s
                    elif rel is not None and origins2[rel] is None:
                        origins2[rel] = (nr % H, nc % W)
                        delays2[rel] = s + delays[k]
                    continue
                if nc >= W:
                    rel = RELATIONS[k]["right"]
                    if rel == "period":
                        if periods["right"] is None:
                            periods["right"] = s
                    elif rel is not None and origins2[rel] is None:
                        origins2[rel] = (nr % H, nc % W)
                        delays2[rel] = s + delays[k]
                    continue
                
                if field[nr][nc] == "#":
                    continue
                
                if (nr,nc) in prevPos[k] or (nr,nc) in newPos[k]:
                    continue
                
                newPos[k].add((nr,nc))

                counts[k][-1] += 1
                
        tmp = positions[k]
        positions[k] = newPos[k]
        prevPos[k] = tmp
    if not any(np for np in newPos.values()):
        for l in counts.values():
            l.pop()
        break


# THIRD JOB:finally, loop over the "corner" cells, saving their period and 
# "counts" (as for the left/right/up/down cells), in the variables counts2 and 
# periods2

counts2 = {k: [1] for k in directions2}
periods2 = {k: None for k in directions2}

prevPos = {k: set() for k in directions2}
positions = {k: {origins2[k]} for k in directions2}
for s in itertools.count(1):
    newPos = {k: set() for k in directions2}
    
    for k in directions2:
        if len(counts2[k]) == 1:
            counts2[k].append(0)
        else:
            counts2[k].append(counts2[k][-2])
        for r,c in positions[k]:
            for nr,nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
                
                if nr < 0:
                    if "up" in k and periods2[k] is None:
                        periods2[k] = s
                    continue
                if nr >= H:
                    if "down" in k and periods2[k] is None:
                        periods2[k] = s
                    continue
                if nc < 0:
                    if "left" in k and periods2[k] is None:
                        periods2[k] = s
                    continue                    
                if nc >= W:
                    if "right" in k and periods2[k] is None:
                        periods2[k] = s
                    continue

                if field[nr][nc] == "#":
                    continue
                
                if (nr,nc) in prevPos[k] or (nr,nc) in newPos[k]:
                    continue
                
                newPos[k].add((nr,nc))

                counts2[k][-1] += 1
                
        tmp = positions[k]
        positions[k] = newPos[k]
        prevPos[k] = tmp
        
    if not any(np for np in newPos.values()):
        for l in counts2.values():
            l.pop()
        break

def calc(s):
    out = 0
    # CENTRAL STARTING SQUARE
    # if it's not filled yet: use the partial counts in "maincounts"
    if s < len(maincounts):
        out += maincounts[s]
    # if it is filled yet: use the 2 options in "mainfulls"
    else:
        out += mainfulls["even" if s % 2 == 0 else "odd"]
        
    # each of the <,>,^,v directions: only after "delays"
    for k in directions:
        s1 = s - delays[k]
        
        # there are some cells that are full
        if s1 >= len(counts[k]):
            # the first has the opposite evenness as "s", all of the remaining ones 
            # are alternating
            fulls = 1 + (s1 - len(counts[k])) // periods[k]
            
            # all pairs
            out += sum(mainfulls.values()) * (fulls//2)
            
            # first one with the opposite evenness as "s", if it's an odd number of them
            if fulls % 2 == 1:
                out += mainfulls["even" if s % 2 == 1 else "odd"]
                
            s1 -= fulls * periods[k]
        
        # all of the non-full cells
        while s1 >= 0:
            out += counts[k][s1]
            s1 -= periods[k]
    
    # each of the diagonal directions: only after the "delays2"
    for k in directions2:
        s2 = s - delays2[k]
        
        
        fullrows = 0
        # some cells are full
        if s2 >= len(counts2[k]):
            fullrows = 1 + (s2 - len(counts2[k])) // periods2[k]
            
            # full is in a triangle of (fullrows * (fullrows + 1)) // 2 elements
            fulls = (fullrows * (fullrows + 1)) // 2
            
            # the fulls are in a checkerboard pattern
            # each diagonal thus is even or odd; alternatingly
            # firstline means the first diagonal (and all subsequent odd-positioned ones)
            # secondline means the second diagonal (and all subsequent even-positioned ones)
            full_firstline = ((fullrows + 1)//2)**2
            full_secondline = (fullrows//2 * (fullrows//2 + 1))
            
            # the first line has the same evenness as "s", the second line has 
            # opposite evenness
            out += full_firstline * mainfulls["even" if s % 2 == 0 else "odd"]
            out += full_secondline * mainfulls["even" if s % 2 == 1 else "odd"]

            
            s2 -= fullrows * periods2[k]
        
        halfrows = fullrows
        # all of the non-full rows of cells
        while s2 >= 0:
            # each new row (with fewer filled cells) has one more cell (thus 
            # halfrows increases)
            halfrows += 1
            out += counts2[k][s2] * halfrows
            
            s2 -= periods2[k]
    
    return out



print()
print("Part Two:")
print(calc(STEPS2))
