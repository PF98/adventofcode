FILE_NAME = "example"
FILE_NAME = "input"

ROCKS_FILE = "rocks"

from itertools import groupby
from dataclasses import dataclass


WIDTH = 7
X_ORIGIN = 2
Y_ORIGIN = 3

ROCK_COUNT = 20220
ROCK_COUNT2 = 1_000_000_000_000

@dataclass
class Rock:
    width: int
    height: int
    shape: list[str]
    def __init__(self, lines):
        self.width = len(lines[0])
        self.height = len(lines)
                
        self.shape = lines.copy()


rocks = []
with open(ROCKS_FILE) as rocksfile:
    lst = [line.strip() for line in rocksfile]
    
    rocks = list(Rock(list(g)) for k,g in groupby(lst, key=lambda x: len(x) > 0) if k)


class Field:
    def __init__(self, WIDTH, rocks, winds):
        self.width = WIDTH
        self.field = []
        self.rocks = rocks
        self.winds = winds
    
    def reset(self):
        self.field = []
    
    def getRockOrigin(self):
        return (X_ORIGIN, len(self.field) + Y_ORIGIN)
        
    def checkRock(self, rockindex, windindex):
        # lower left corner of the rock
        x,y = self.getRockOrigin()
        rock = self.rocks[rockindex]
        #print(f"{x=},{y=}")
        while True:
            
            # push with the wind
            match self.winds[windindex]:
                case "<":
                    newX = x - 1
                case ">":
                    newX = x + 1
                
            # must check if the wind would push the rock outside the bounds
            # or within another rock
            if self.moveRock(rock, newX, y):
                #print(f" -> moving from {x=} to {newX}", end="")
                x = newX
                    
            
            windindex = (windindex + 1) % len(self.winds)
            
            #print(f" -> wind: {x=}")
            
            # check if the rock can move down
            if self.moveRock(rock, x, y - 1):
                y -= 1
                #print(f" -> the rock fell to {y=}")
                continue
            
            
            # the rock can't move down: add the required rows to fit it
            newRowsCnt = max(0, y + rock.height - len(self.field))
            self.field.extend(["."]*WIDTH for _ in range(newRowsCnt))
                
            # place all of the pixels of the rock
            for ry,row in enumerate(reversed(rock.shape), start=y):
                for rx,cell in enumerate(row, start=x):
                    if cell != "#":
                        continue
                    
                    self.field[ry][rx] = "#"
            
            return windindex
            
        raise Exception("should not end up here..." + str(self))
    
    
    def moveRock(self, rock, x, y):
        # rock is outside the bounds to the left or to the right
        if x < 0 or x + rock.width > self.width:
            return False
        
        # rock is outside the bounds below
        if y < 0:
            return False
        
        return not self.intersects(rock, x, y)
    
    def intersects(self, rock, x, y):
        for ry,row in enumerate(reversed(rock.shape), start=y):
            # rock line ry is above the last line
            if ry >= len(self.field):
                continue
            
            if any(self.field[ry][rx] == "#" for rx,cell in enumerate(row, start=x) if cell == "#"):
                return True
            
        return False
    
    def getHeight(self):
        return len(self.field)
                
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        numlen = 4
        rows = (f"{str(len(self.field) - 1 - n).rjust(numlen)} |{''.join(row)}|" for n,row in enumerate(reversed(self.field[-50:])))
                
        return "\n".join([*rows, f"{' '*numlen} +{'-'*self.width}+"])
        
with open(FILE_NAME) as file:
    winds = file.readline().strip()
    
    wi = 0
    f = Field(WIDTH, rocks, winds)
    #print(f)
    allwinds = []
    ori = None
    for ri in range(ROCK_COUNT):
        wi = f.checkRock(ri % len(rocks), wi)
        

    
    print("Part One: How many units tall will the tower of rocks be after 2022 rocks have stopped falling?")
    print(f.getHeight())
    #print(allwinds)
    #print(len(winds))
    
    
    owi = None
    ori = None
    oh = None
    rdelta = None
    hdelta = None
    
    final = None
    extraheight = None
    
    f.reset()
    
    ri = 0
    wi = 0
    while True:
        wi = f.checkRock(ri % len(rocks), wi)
        
        if owi is not None and wi < owi:
            if oh is not None and ori is not None:
                # detect the (empirically proven) periodicity
                if hdelta == (f.getHeight() - oh) and rdelta == (ri - ori):
                    start = ori
                    curr = ri
                    
                    #print(f"{start=}")
                    #print(f"{curr=}")
                    #print(f"{rdelta=}")
                    #print(f"{hdelta=}")
                    
                    
                    #print(f"{(ROCK_COUNT2 - curr) // rdelta=}")
                    
                    extraheight = hdelta * ((ROCK_COUNT2 - curr) // rdelta)
                    final = curr + ((ROCK_COUNT2 - curr) % rdelta)
                    
                    #print(f"{extraheight=}")
                    #print(f"{final=}")
                    #print(f"{hdelta=}, {rdelta=} ({final=}, {f.getHeight() + extraheight=}, )")
                rdelta = ri - ori
                hdelta = f.getHeight() - oh
            
            ori = ri
            
            oh = f.getHeight()
            
        owi = wi
        ri += 1
        
        if final is not None and ri == final:
            break
    
    print()
    print("Part Two: How many units tall will the tower of rocks be after 2022 rocks have stopped falling?")
    print(f.getHeight() + extraheight)
