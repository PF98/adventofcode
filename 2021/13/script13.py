from functools import reduce
import re
import math
from PIL import Image, ImageDraw

FILE_NAME = "example"
FILE_NAME = "input"

PRINT_MAP = [" ", "█"]

class Paper:
    def __init__(self, dots):
        w,h = (max(l) for l in zip(*dots))
        self.w = w+1;
        self.h = h+1;
        #print(w)
        #print(h)
        self.grid = [[0] * self.w for _ in range(self.h)]
        for x,y in dots:
            self.grid[y][x] = 1
            
        self.zoom = 1

    def fold(self, direction, num):
        if direction == "x":
            for row in self.grid:
                start = 2*num - self.w + 1
                row[start:] = list(a or b for a,b in zip(row[start:num], row[:num:-1]))
                
                #print("".join(PRINT_MAP[c] for c in rowpart))
                
        elif direction == "y":
            h = len(self.grid)
            for j in range(h - num - 1):
                line = self.grid.pop()
                self.grid[j][:] = (a or b for a,b in zip(self.grid[j], line))
            self.grid.pop() # remove the folding line

    def genImage(self, fold = None):
        if fold is not None:
            foldDir,foldNum = fold
        
        size = (math.ceil(self.w / self.zoom), math.ceil(self.h / self.zoom))
        
        img = Image.new("RGB", size, color=(100,100,100))
        draw = ImageDraw.Draw(img)
        
        w = len(self.grid[0])
        h = len(self.grid)
        
        draw.rectangle(((0,0), (w-1, h-1)), fill=(0,0,0))
        for y,row in enumerate(self.grid):
            for x,cell in enumerate(row):
                if cell == 1:
                    img.putpixel((x,y), (255,255,255))
            
        if fold is not None:
            if foldDir == "x":
                draw.rectangle(((foldNum, 0), (foldNum, h-1)), outline=(0,255,0))
            elif foldDir == "y":
                draw.rectangle(((0, foldNum), (w-1, foldNum)), outline=(0,255,0))
                
        
        return img

    def genZoom(self):
        w = len(self.grid[0])
        h = len(self.grid)
        
        return min(math.floor(self.w/w), math.floor(self.h/h))
    
    def setZoom(self, zoom):
        self.zoom = zoom
        
    def setCalcZoom(self):
        oz = self.zoom
        
        self.zoom = self.genZoom()
        return oz != self.zoom

    def count(self):
        return sum(sum(line) for line in self.grid)

    def __str__(self):
        #return "\n".join(''.join(PRINT_MAP[c] for c in line) for line in self.grid)
        
        block = "░"
        
        line = block + block * len(self.grid[0]) + block
        return f"{line}\n" + "\n".join(f"{block}{''.join(PRINT_MAP[c] for c in line)}{block}" for line in self.grid) + f"\n{line}"
        

def imgSave(img, num):
    img.save(f"out-{num:02}.png")
    return num+1


with open(FILE_NAME) as file:
    
    dots = []
    dotsy = {}
    isDots = True
    
    paper = None
    
    firstFoldCount = None
    
    imgCount = 1
    
    for line in file:
        if len(line.strip()) == 0:
            isDots = False
            paper = Paper(dots)
            #dotsy = {k:dotsy[k] for k in dotsy if len(dotsy[k]) > 1}
            #print("\n".join(str(k) + ": " + str(dotsy[k]) + (" -> " + str(sum(dotsy[k])/2) if len(dotsy[k]) == 2 else "") for k in dotsy))
            #print("Paper:")
            #print(paper)
            #img = paper.genImage()
            #imgCount = imgSave(img, imgCount)
            continue
        
        if isDots:
            #print(len(line))
            x,y = (int(n) for n in line.split(","))
            dots.append((x,y))
            
            if not y in dotsy:
                dotsy[y] = []
            
            dotsy[y].append(x)
            
        else:
            m = re.search("fold along (x|y)=(\d+)", line)
            direction = m.group(1)
            num = int(m.group(2))
            
            paper.fold(direction, num)
            
            #img = paper.genImage(fold=(direction, num))
            #imgCount = imgSave(img, imgCount)
            
            
            #while True:
                #img = paper.genImage()
                #imgCount = imgSave(img, imgCount)
                
                #changed = paper.setCalcZoom()
                #if not changed:
                    #break
            
            
            
            if firstFoldCount is None:
                ##print(paper)
                firstFoldCount = paper.count()
            
            
            
            #print(f"After \"{line[:-1]}\":")
            #print(paper)
        
    print("Part One: How many dots are visible after completing just the first fold instruction on your transparent paper?")
    print(firstFoldCount)
    
    print()
    print("Part Two: What code do you use to activate the infrared thermal imaging camera system?")
    print(paper)
    

    
    
