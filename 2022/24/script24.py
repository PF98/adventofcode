FILE_NAME = "example1"
FILE_NAME = "example2"
FILE_NAME = "input"

from collections import defaultdict
import time

# note: I'm including the walls in these conditions
CHANGE_COORD = [
    # down
    (
        lambda x,y,w,h: 0 < x < w-1 and y < h - 2,
        lambda x,y: (x, y+1),
    ),
    # right
    (
        lambda x,y,w,h: x < w - 2 and 0 < y < h-1,
        lambda x,y: (x+1, y),
    ),
    # still
    (
        lambda *args: True,
        lambda x,y: (x,y),
    ),
    # up
    (
        lambda x,y,w,h: 0 < x < w-1 and y > 1,
        lambda x,y: (x, y-1),
    ),
    # left
    (
        lambda x,y,w,h: x > 1 and 0 < y < h-1,
        lambda x,y: (x-1, y),
    ),
]
    
    
    
class Blizzards:
    def __init__(self, w, h):
        self.dd = defaultdict(lambda: [])
        self.w = w
        self.h = h
        
    def step(self):
        newdd = defaultdict(lambda: [])
        #print("stepping blizzards")
        for pos,winds in self.dd.items():
            for wind in winds:
                xWind, yWind = pos
                match wind:
                    case "<" | ">":
                        # wrapping between indices 1 and w-2 (0 and w-1 are walls)
                        xWind = (xWind + (1 if wind == ">" else -1) - 1) % (self.w - 2) + 1
                    case "^" | "v":
                        # wrapping between indices 1 and h-2 (0 and h-1 are walls)
                        yWind = (yWind + (1 if wind == "v" else -1) - 1) % (self.h - 2) + 1
                
                #print(f"  moving '{wind}' from {pos=} to newPos={(xWind,yWind)}")
                
                newdd[(xWind, yWind)].append(wind)
        
        self.dd = newdd
    
    def add(self, pos, val):
        self.dd[pos].append(val)
    
    def __contains__(self, value):
        return value in self.dd
    
    def _getChr(self, pos, positions):
        if pos in positions:
            return "█"
        
        if pos not in self:
            return "."
        
        l = len(self.dd[pos])
        return self.dd[pos][0] if l == 1 else str(l)
    
    def __len__(self):
        return len(self.dd)
    
    def print(self, positions):
        tb = "#"*(self.w)
        top = list(tb)
        # start
        top[1] = self._getChr((1,0), positions)
        top = "".join(top)
        
        bot = list(tb)
        bot[-2] = " "
        bot = "".join(bot)
        
        
        rows = [f"#{''.join(self._getChr((x,y), positions) for x in range(1,self.w - 1))}#" for y in range(1, self.h - 1)]
    
        
    
        print("\n".join([top, *rows, bot]))
def searchPath(blizzards, start, end):
    positions = {start}
    
    #print(f"Initial state:")
    #blizzards.print(positions)
    #input()
    
    turn = 0
    while True:
        blizzards.step()
        turn += 1
        
        
        newPositions = set()
        for x,y in positions:
            for cond, func in CHANGE_COORD:
                newPos = func(x,y)
                if (cond(x,y,w,h) or newPos == start) and newPos not in blizzards:
                    newPositions.add(newPos)
                elif newPos == end:
                    return turn
                
        positions = newPositions
        
        #print(f"Step {turn}, {len(positions) = }")
        #blizzards.print(positions)
        #time.sleep(0.2)

                
            

with open(FILE_NAME) as file:
    lst = [line.strip() for line in file]
    
    w = len(lst[0])
    h = len(lst)
    
    start = (1, 0)
    end = (w-2, h-1)
    
    blizzards = Blizzards(w,h)
    
    for y,row in enumerate(lst[1:-1], start=1):
        for x,cell in enumerate(row[1:-1], start=1):
            if cell == ".":
                continue
            
            blizzards.add((x,y), cell)
            
    
    
    #print(len(blizzards))
    
    out = searchPath(blizzards, start, end)
    
    
    print("Part One: What is the fewest number of minutes required to avoid the blizzards and reach the goal?")
    print(out)
    
    out2 = searchPath(blizzards, end, start)
    #print(out2)
    
    out3 = searchPath(blizzards, start, end)
    #print(out3)
    print()
    print("Part Two: What is the fewest number of minutes required to reach the goal, go back to the start, then reach the goal again?")
    print(out + out2 + out3)
