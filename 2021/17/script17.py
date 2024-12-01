from functools import reduce
import re
import math
#import heapq
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk


FILE_NAME = "example"
FILE_NAME = "input"

def imageXY(minx, miny, maxx, maxy, x, y):
    (minx,miny),(maxx, maxy) = RANGE
    
    
    ix = x - minx
    iy = maxy - y
    
    return ix,iy

RANGE = ((0,-120), (300, 280))
def inRange(x,y):
    return all(c1 <= p < c2 for c1,c2,p in zip(*RANGE, (x,y)))

def printGrid(target, steps, saveImage = False):
    minx = None
    miny = None
    maxx = None
    maxy = None
    for t in steps + list(target):
        if minx == None or t.x < minx:
            minx = t.x
        if miny == None or t.y < miny:
            miny = t.y
        if maxx == None or t.x > maxx:
            maxx = t.x
        if maxy == None or t.y > maxy:
            maxy = t.y
    stepTuples = [s.getTuple() for s in steps]
    
    if not saveImage:
        for y in range(maxy, miny-1, -1):
            print(f"{y:4} ", end="")
            for x in range(minx, maxx+1):
                coord = Coord(x,y)
                if (x,y) == stepTuples[0]:
                    c = "S"
                elif (x,y) in stepTuples:
                    c = "#"
                elif coord.within(target):
                    c = "T"
                else:
                    c = "."
                    
                print(c, end="")
            print("")

    else:
        size = (maxx - minx + 1, maxy - miny + 1)
        size = tuple(c2-c1+1 for c1,c2 in zip(*RANGE))
        img = Image.new("RGB", size, color=(0,0,0))
        draw = ImageDraw.Draw(img)
        t1 = imageXY(minx, miny, maxx, maxy, *target[0].getTuple())
        t2 = imageXY(minx, miny, maxx, maxy, *target[1].getTuple())
        draw.rectangle((t1, t2), fill=(0,255,0))

        for i,(x,y) in enumerate(stepTuples):
            if not inRange(x,y):
                continue
            print(f"p: {(x,y)}")
            ix,iy = imageXY(minx, miny, maxx, maxy, x, y)
            print(f"i: {(ix,iy)}")
            
            img.putpixel((ix,iy), (255,255,255) if i > 0 else (255,0,0))
        
        z = 5
        z = 2
        if z > 1:
            img = img.resize(tuple(z * s for s in size), Image.NEAREST)
        #img.save("out.png")
        
        
        tkimg = ImageTk.PhotoImage(img)
        
        label = tk.Label(window, image=tkimg)
        label.pack()
        window.mainloop()
        label.destroy()
        #img.show()
        

START = (0,0)

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def clone(self):
        return Coord(self.x, self.y)
    
    @classmethod
    def fromTuple(cls, t):
        return cls(t[0], t[1])
        
    def getTuple(self):
        return (self.x, self.y)
    
    def update(self, vel):
        self.x += vel.x
        self.y += vel.y
        
    def within(self, target):
        return all(c1 <= p <= c2 for c1, c2, p in zip(*(t.getTuple() for t in target), self.getTuple()))
    
    def after(self, target, vel):
        # under the target with negative y velocity
        if vel.y < 0 and pos.y < target[0].y:
            return True

        # right of the target with positive x velocity
        if vel.x >= 0 and pos.x > target[1].x:
            return True
        
        return False


    def __str__(self):
        return f"{(self.x, self.y)}"
        
class Velocity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def clone(self):
        return Velocity(self.x, self.y)

    def getTuple(self):
        return (self.x, self.y)
    
    def update(self):
        self.x -= sign(self.x)
        self.y -= 1
        
    def setX(self, x):
        self.x = x
        
    def setY(self, y):
        self.y = y
        
    def sets(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"{(self.x, self.y)}"
    
    
    
#window = tk.Tk()
#window.geometry("500x500")
#tk.Button(window, text="Continue", command=window.quit).pack()
#window.mainloop()

with open(FILE_NAME) as file:
    line = file.readline().strip()
    m = re.match("target area: x=(-?\d+\.\.-?\d+), y=(-?\d+\.\.-?\d+)", line)
    
    
    xs = tuple(int(n) for n in m.group(1).split(".."))
    ys = tuple(int(n) for n in m.group(2).split(".."))
    
    target = (Coord(min(xs), min(ys)), Coord(max(xs), max(ys)))
    #velocity = (7,2)
    #velocity = (6,3)
    #velocity = (9,0)
    #velocity = (17,-4)
    #velocity = (6,9)
    #velocity = (6,11)
    
    count = 0
    
    directionUp = True
    maxyglob = None
    maxvel = None
    velocity = Velocity(0,0)
    while True:
        vel = velocity.clone()
        pos = Coord.fromTuple(START)
        #print(f"pos: {pos}")
        #print(f"vel: {vel}")
        #print()
        cnt = 0
        inTargetb = False
        
        steps = [pos.clone()]
        
        maxy = 0
        while not pos.after(target, vel):
            pos.update(vel)
            vel.update()
            #print(f"pos: {pos}")
            #print(f"vel: {vel}")
            #print()
            steps.append(pos.clone())
            if pos.within(target):
                inTargetb = True
                break
            
            if maxy is None or pos.y > maxy:
                maxy = pos.y
        
        #printGrid(target, steps)
        #printGrid(target, steps, True)
        if inTargetb:
            #print("In TARGET!")
            #print(velocity.getTuple())
            count += 1
            if maxyglob is None or maxy > maxyglob:
                maxyglob = maxy
                maxvel = velocity.getTuple()
        else:
            pass
            #print("After target")
        #print([t.getTuple() for t in target])
        
        #print(f"starting velocity: {velocity.getTuple()}")
        #print(f"max: {maxyglob}")
        #print(f"pos: {pos.getTuple()}")
        #print(f"vel: {vel.getTuple()}")
    
        
        #input()
        if not inTargetb:
            # only 2 steps (start and current), if we are left and below target, then end
            if pos.x > target[1].x and len(steps) == 2:
                break
            
            # is moving vertically...
            if vel.x == 0:
                # ...and has not reached the target: increase the starting x velocity
                if pos.x < target[0].x:
                    velocity.sets(velocity.x+1, 0)
                    continue
            
            # has gone under the target without hitting it...
            if pos.y < target[0].y:
                # if the y of the penultimate step was zero: it passed straight through the target
                # need to increment
                if directionUp:
                    if steps[-2].y == 0:
                        velocity.setY(-1)
                        directionUp = False
                        continue
                    else:
                        velocity.setY(velocity.y + 1)
                        continue
                else:
                    # the previous one was to the left of target, going down won't help
                    if steps[-2].x < target[0].x:
                        velocity.sets(velocity.x + 1, 0)
                        directionUp = True
                        continue
                    else:
                        velocity.setY(velocity.y - 1)
                        continue
                
            # this has gone straight over the target: should be enough to end -> it's not
            if pos.x > target[1].x:
                if directionUp:
                    directionUp = False
                    velocity.setY(-1)
                    continue
                else:
                    # the previous step is before the target: skip this completely to the next x
                    if steps[-2].x < target[0].x:
                        velocity.sets(velocity.x + 1, 0)
                        directionUp = True
                        continue
                    else:
                        velocity.setY(velocity.y - 1)
                        continue
        # in target: need to increase until this does not work anymore
        else:
            if directionUp:
                velocity.setY(velocity.y + 1)
                continue
            else:
                velocity.setY(velocity.y - 1)
                continue
            
        
    
    print("Part One: What is the highest y position it reaches on this trajectory?")
    print(maxyglob)
    #print(maxvel)
    
    
    print()
    print("Part Two: How many distinct initial velocity values cause the probe to be within the target area after any step?")
    print(count)
    
