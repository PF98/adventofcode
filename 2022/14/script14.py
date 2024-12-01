FILE_NAME = "example"
FILE_NAME = "input"

import itertools
import time
import os
from collections import defaultdict

ORIGIN = (500,0)

# list of func
SAND_MOVEMENT = [
    # down
    lambda p: (p[0], p[1] + 1),
    # down-left
    lambda p: (p[0] - 1, p[1] + 1),
    # down-right
    lambda p: (p[0] + 1, p[1] + 1),
]

AIR_CHAR = " "
SAND_CHAR = "░"
WALL_CHAR = "█"
ORIGIN_CHAR = "U"


class Map:
    def __init__(self, xbounds, ybounds, origin):
        self.xmin, self.xmax = xbounds
        self.ymin, self.ymax = ybounds
        self.origin = origin
        self.obj = defaultdict(lambda: AIR_CHAR)
        self.obj[origin] = "U"
    
    def addBottomLines(self, num):
        self.ymax = self.ymax + 2
    
    def putLine(self, start, end):
        match tuple(e-s for s,e in zip(start, end)):
            case (d,0):
                for i in range(abs(d)+1):
                    self.obj[(start[0] + (i if d > 0 else -i), start[1])] = WALL_CHAR
            case (0,d):
                for i in range(abs(d)+1):
                    self.obj[(start[0], start[1] + (i if d > 0 else -i))] = WALL_CHAR
            case _:
                raise Exception(f"{start=}, {end=}")


    def generateSand(self, minlevel = False):
        point = self.origin
        while True:
            for func in SAND_MOVEMENT:
                newpoint = func(point)
                # there is a min level on which the sand rests -> same as if some block was below
                if minlevel and newpoint[1] == self.ymax:
                    continue
                
                # the map has finished, every sand falls out
                if newpoint[1] > self.ymax:
                    return False
                
                # air is below the new point: move the sand there and continue
                if self.obj[newpoint] == AIR_CHAR:
                    point = newpoint
                    #os.system("clear")
                    #self[point] = "~"
                    #print(self)
                    #self[point] = AIR_CHAR
                    #time.sleep(0.01)
                    break
            # the sand has no free blocks in any of SAND_MOVEMENT
            else:
                self.obj[point] = SAND_CHAR
                self.xmin = min(self.xmin, point[0])
                self.xmax = max(self.xmax, point[0])
                
                if point == self.origin:
                    return False
                
                break
            
        return True
    
    def clearSand(self):
        self.obj = defaultdict(lambda: AIR_CHAR, {k:v for k,v in self.obj.items() if v != SAND_CHAR})
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        arr = [[self.obj[(c+self.xmin,r+self.ymin)] for c in range(self.xmax - self.xmin + 1)] for r in range(self.ymax - self.ymin + 1)]
        
        m = "\n".join("|" + "".join(line) + "|" for line in arr)
        line = "+" + "-" * len(arr[0]) + "+"
        return f"{line}\n{m}\n{line}"

with open(FILE_NAME) as file:
    lst = [[tuple(int(n) for n in c.split(",")) for c in line.strip().split(" -> ")] for line in file]
    
    xmax, ymax = (max(n) for n in zip(*itertools.chain(*lst), ORIGIN))
    xmin, ymin = (min(n) for n in zip(*itertools.chain(*lst), ORIGIN))
    
    #print(lst)
    #print(xmax, ymax)
    #print(xmin, ymin)
    
    m = Map((xmin, xmax), (ymin, ymax), ORIGIN)
    for line in lst:
        for start,end in zip(line, line[1:]):
            m.putLine(start, end)
    
    #print(m)
    
    cnt = 0
    while True:
        if not m.generateSand():
            break
        
        cnt += 1
        #os.system("clear")
        #print(m)
        #time.sleep(0.05)
        
    print("Part One: Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?")
    print(cnt)
    
    
    #print(m)
    m.clearSand()
    
    m.addBottomLines(2)
    
    
    cnt = 0
    while True:
        if not m.generateSand(True):
            break
        
        cnt += 1
        #os.system("clear")
        #print(m)
        #print(cnt)
        #time.sleep(0.05)
    
    #os.system("clear")
    print(m)
    
    
    print()
    print("Part Two: Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?")
    print(cnt + 1)
    
