FILE_NAME = "example1"
FILE_NAME = "example2"
FILE_NAME = "input"

from collections import defaultdict
import itertools

# list of tuples (cond(pos,elves), func(pos)
PROPOSABLE_MOVES = [
    # north (if N, NE, NW are free)
    (
        lambda x,y, elves: all((x+dx,y-1) not in elves for dx in range(-1,2)),
        lambda x,y: (x,y-1)
    ),
    # south (if S, SE, SW are free)
    (
        lambda x,y, elves: all((x+dx,y+1) not in elves for dx in range(-1,2)),
        lambda x,y: (x,y+1)
    ),
    # west (if W, NW, SW are free)
    (
        lambda x,y, elves: all((x-1,y+dy) not in elves for dy in range(-1,2)),
        lambda x,y: (x-1,y)
    ),
    # east (if E, NE, SE are free)
    (
        lambda x,y, elves: all((x+1,y+dy) not in elves for dy in range(-1,2)),
        lambda x,y: (x+1,y)
    ),
]

class Elf:
    def __init__(self, pos):
        self.pos = pos
        self.moveIndex = 0
        self.proposedMove = None
    
    def proposeMove(self, elves):
        x,y = self.pos
        
        #s = sum(1 for dx,dy in itertools.product(range(-1,2), range(-1,2)) if (x+dx,y+dy) in elves)
        #s = list((x+dx,y+dy) for dx,dy in itertools.product(range(-1,2), range(-1,2)) if (x+dx,y+dx) in elves)
        
        #print(f"{s=} for {self=}")
        
        
        
        # no other elf around: don't move
        if sum(1 for dx,dy in itertools.product(range(-1,2), range(-1,2)) if (x+dx,y+dy) in elves) == 1:
            self.proposedMove = None
        # some elves are around: move
        else:
            for i, (cond, func) in enumerate((*PROPOSABLE_MOVES[self.moveIndex:], *PROPOSABLE_MOVES[:self.moveIndex])):
                if cond(x,y, elves):
                    self.proposedMove = func(x,y)
                    #print(f"{self.proposedMove=}, with {self.moveIndex=} and {i=} for {self=}")
                    break
            else:
                self.proposedMove = None
            
        self.moveIndex += 1
        self.moveIndex %= len(PROPOSABLE_MOVES)
            
        return self.proposedMove
    
        
    def executeMove(self, proposedMoves):
        m = self.proposedMove
        # not moving: no move available or a conflict with another elf
        if m is None or proposedMoves[m] > 1:
            return False
        
        # moving
        self.pos = self.proposedMove
        return True
        
    def __repr__(self):
        return str(self)
    def __str__(self):
        return f"Elf(id={hex(id(self))}, pos={self.pos}, proposedMove={self.proposedMove}, moveIndex={self.moveIndex})"

def drawAutoElves(elves):
    minX, minY = (min(e) for e in zip(*elves.keys()))
    maxX, maxY = (max(e) for e in zip(*elves.keys()))
    
    drawElves((minX, maxX), (minY, maxY), elves)

def drawElves(xrng, yrng, elves):
    print(f"  +{'-' * (xrng[1] - xrng[0] + 1)}+")
    for r in range(yrng[0], yrng[1]+1):
        print(f"{r:2d}|", end="")
        for c in range(xrng[0], xrng[1]+1):
            print("#" if (c,r) in elves else ".", end="")
        print("|")
    print(f"  +{'-' * (xrng[1] - xrng[0] + 1)}+")

with open(FILE_NAME) as file:
    field = [line.strip() for line in file]
    
    elves = {}
    for r,row in enumerate(field):
        for c,cell in enumerate(row):
            if cell == "#":
                elves[(c,r)] = Elf((c,r))
    
    
    #drawAutoElves(elves)
    hasMoved = True
    i = 0
    while hasMoved:
        proposedMoves = defaultdict(lambda: 0)
        for elf in elves.values():
            m = elf.proposeMove(elves)
            
            if m is not None:
                proposedMoves[m] += 1
        
        hasMoved = False
        
        newElves = {}
        for elf in elves.values():
            moved = elf.executeMove(proposedMoves)
            hasMoved = hasMoved or moved
            
            newElves[elf.pos] = elf

        #print("\n")
        #print("elves:")
        #print("\n".join(f"  {k} => {v}" for k,v in elves.items()))
        #print("newElves:")
        #print("\n".join(f"  {k} => {v}" for k,v in newElves.items()))
        
        i += 1
        elves = newElves
        
        #print(f"== End of Round {i} ==", end="\r")
        #drawAutoElves(elves)
        
        
        if i == 10:
            minX, minY = (min(e) for e in zip(*elves.keys()))
            maxX, maxY = (max(e) for e in zip(*elves.keys()))
            
            area = (maxX - minX + 1) * (maxY - minY + 1)
            print(" "*100, end="\r")
            print("Part One: Simulate the Elves' process and find the smallest rectangle that contains the Elves after 10 rounds. How many empty ground tiles does that rectangle contain?")
            #print(f"Total area: {area}")
            #print(f"Total elves: {len(elves)}")
            print(area - len(elves))
            
    
    
    #print()
    print(" "*100)
    print("Part Two: Figure out where the Elves need to go. What is the number of the first round where no Elf moves?")
    print(i)
