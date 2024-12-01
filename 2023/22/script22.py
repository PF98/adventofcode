FILE_NAME = "example"
FILE_NAME = "input"

from dataclasses import dataclass

def extr(s):
    return (int(e) for e in s.split(","))

@dataclass
class Block:
    x: tuple
    y: tuple
    z: tuple
    aligned: list
    def __init__(self, xs, ys, zs):
        self.x = xs
        self.y = ys
        self.z = zs
        
        self.aligned = []
    
    def isAligned(self, other):
        return \
            self.x[0] <= other.x[1] and other.x[0] <= self.x[1] \
            and \
            self.y[0] <= other.y[1] and other.y[0] <= self.y[1] \

blocks = []
with open(FILE_NAME) as file:
    for i,line in enumerate(file):
        block = Block(*zip(*(extr(s) for s in line.split("~"))))
        
        for j,other in enumerate(blocks):
            if block.isAligned(other):
                block.aligned.append(j)
                other.aligned.append(i)
        
        blocks.append(block)


# moving down all of the blocks
moved = True
while moved:
    moved = False
    for i1,b1 in enumerate(blocks):
        blockz = b1.z[0]
        # check if it has no supporting blocks among the aligned ones
        dropz = 1 + max((zt for zt in (blocks[i2].z[1] for i2 in b1.aligned) if zt < blockz), default = 0)
        
        # drop the block
        if dropz < blockz:
            height = b1.z[1] - b1.z[0]
            b1.z = (dropz, dropz + height)
            moved = True


removable = [True] * len(blocks)

holdsups = [[] for _ in range(len(blocks))]
heldbys = [[] for _ in range(len(blocks))]

# check which block is held up by which other block (for part 2), while also 
# checking which blocks are removable
for i1,b1 in enumerate(blocks):
    heldby = None
    # look for the blocks that hold up b1
    for i2 in b1.aligned:
        b2 = blocks[i2]
        # b2 holds up b1
        if b2.z[1] + 1 == b1.z[0]:
            holdsups[i2].append(i1)
            heldbys[i1].append(i2)
            
            if heldby is None:
                heldby = i2
            else:
                heldby = False

    # exactly 1 block (holdup = b2) holds up b1: it can't be removed
    if heldby is not None and heldby is not False:
        removable[heldby] = False


print("Part One:")
print(sum(removable))




out = 0
for i1,b1 in enumerate(blocks):
    if removable[i1]:
        continue
    
    moving = {i1}
    candidates = {i1}
    
    while candidates:
        i = candidates.pop()
        
        for i2 in holdsups[i]:
            if i2 in moving:
                continue
            
            if all(c in moving for c in heldbys[i2]):
                candidates.add(i2)
                moving.add(i2)
    
    out += (len(moving) - 1)
    
print()
print("Part Two:")
print(out)
