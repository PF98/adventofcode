from functools import reduce
import re
import math

PLOT = True
PLOT = False

if PLOT:
    import sys
    from pathlib import Path
    #print(list(Path(__file__).parents[0]))
    path_root = Path(__file__).parents[0]
    sys.path.append(str(path_root))
    #print(sys.path)

    import myplot

FILE_NAME = "example"
FILE_NAME = "example2"
FILE_NAME = "input"

RANGE1 = (-50, 50)
SIZE = RANGE1[1] - RANGE1[0] + 1

def inRange(num, r):
    return r[0] <= num <= r[1]

def extract(s):
    nums = s.split("=")[1]
    return tuple(int(n) for n in nums.split(".."))

def constraintRange(nums, r):
    if nums[1] < RANGE1[0] or nums[0] > RANGE1[1]:
        return False
    return tuple(r[0] if n < r[0] else (r[1] if n > r[1] else n) for n in nums)

    

class Space:
    def __init__(self):
        # list of cuboids, addCube and removeCube guarantees that they all are mutually exclusive from one another
        self.cubes = []
        self.count = 0

    def intersects(c1, c2):
        #xs1, ys1, zs1 = c1
        #xs2, ys2, zs2 = c2
        
        #c1,c2 = c2,c1
        out = tuple((max(d1[0], d2[0]),  min(d1[1], d2[1])) for d1, d2 in zip(c1, c2))
        if any(c1 > c2 for c1,c2 in out):
            return None
        return out


    def getVolume(cube):
        return reduce(lambda a,b: a*b, (abs(c2 - c1) + 1 for c1,c2 in cube), 1)

    def decomposeCube(otherCube, intersection, depth = 1):
        #print(f"{'    '*depth}Calling decompose on {otherCube}, ")
        #print(f"{'    '*depth}{' '*(len('Calling decompose on ') - len('and '))}and {intersection}")
        
        # otherCube is completely inside cube: discard otherCube => it's decomposition will be an empty set
        # equivalent to totBordersCount == 6
        if otherCube == intersection:
            #print(f"{'    '*depth}returning cubes = {[]}")
            return []
        
        
        
        # if totBordersCount == 0, then this function shouldn't have been called, since it would have been cube == intersection
        
        #bordersCount = [tuple(t[0] == t[1] for t in zip(*sl)) for sl in list(zip(otherCube, intersection))]
        #totBordersCount = sum(sum(b) for b in bordersCount)

        #print(f"{'    '*depth}bordersCount: {bordersCount} -> {totBordersCount}")
        
        # bordersCount: list of tuples denoting which coordinates are not equal: (axis 0->2 for x->y, direction 0 or 1 for low or high bound)
        #bordersCount = reduce(lambda a,b: set([*a, *b]), (list((c,i) for i,t in enumerate(zip(*sl)) if t[0] != t[1]) for c,sl in enumerate(zip(otherCube, intersection))))
        bordersCount = [tuple(t[0] == t[1] for t in zip(*sl)) for sl in list(zip(otherCube, intersection))]
        totBordersCount = sum(sum(b) for b in bordersCount)
        #print(f"{'    '*depth}bordersCount: {bordersCount} -> {totBordersCount}")
        
        
        cubes = []
        currentCube = otherCube
        for i,lh in enumerate(bordersCount):
            if all(lh):
                continue
            
            l, h = lh
            
            cl, ch = currentCube[i]
            il, ih = intersection[i]
            
            #cubes = []
            
            remainingCube = list(currentCube)
            
            # l is False: cl != il (in particular cl < il)
            # => the new cube must be between cl and il-excluded)
            # => the remaining cube must be between il and rh
            if l is False:
                lbox = list(currentCube)
                lbox[i] = (cl, il-1)
                cubes.append(tuple(lbox))
                
                rl, rh = remainingCube[i]
                remainingCube[i] = (il, rh)
                
            # h is False: ch != ih (in particular ih < ch
            # => the new cube must be between ih(excluded) and ch
            # => the remaining cube must be between rl and ih
            if h is False:
                lbox = list(currentCube)
                lbox[i] = (ih+1, ch)
                cubes.append(tuple(lbox))
                
                rl, rh = remainingCube[i]
                remainingCube[i] = (rl, ih)
                
            
            currentCube = tuple(remainingCube)
            #recCubes = Space.decomposeCube(tuple(remainingCube), intersection, depth + 1)
            
            #cubes.extend(recCubes)
            
            #print(f"{'    '*depth}returning cubes = {cubes}")
            #return cubes
            
        return cubes
        #raise Exception("It should never get to here")

    def addCube(self, cube):
        # idea of adding a cube: decompose every otherCube which intersects cube and keep cube intact        
        volume = Space.getVolume(cube)
        self.count += volume
        #print(f"Adding cube {cube} with volume = {volume}")
        #print(f"self.cubes: len = {len(self.cubes)}")
        
        newCubes = [cube]
        
        for otherCube in self.cubes:
            intersection = Space.intersects(otherCube, cube)
            if intersection is None:
                #print(f"    no intersection with {otherCube}, it's added back to self.cubes")
                newCubes.append(otherCube)
                continue
            
            oldVolume = Space.getVolume(otherCube)
            
            # remove the volume of any intersection
            intvolume = Space.getVolume(intersection)
            self.count -= intvolume
            #print(f"    intersection with {otherCube} found: {intersection} with volume = {intvolume}")
            
            
            # cube is completely inside otherCube: we don't need do do anything, keep otherCube intact and discard cube
            if intersection == cube:
                return
                

            
            
            # cube (the negative one) intersects otherCube
            # decompose otherCube into subcubes not intersecting cube and still on
            decomposedCubes = Space.decomposeCube(otherCube, intersection)
            #print(f"     -> decomposed into {decomposedCubes}, to be added to self.cubes")
            
            decVolume = sum(Space.getVolume(c) for c in decomposedCubes)
            
            if decVolume != (oldVolume - intvolume):
                raise Exception("volume errato")
            
            newCubes.extend(decomposedCubes)
        
        self.cubes = newCubes
    
    
    def removeCube(self, cube):
        newCubes = []
        
        for otherCube in self.cubes:
            intersection = Space.intersects(otherCube, cube)
            if intersection is None:
                newCubes.append(otherCube)
                continue
            
            oldVolume = Space.getVolume(otherCube)

            # remove the volume of any intersection
            intvolume = Space.getVolume(intersection)
            self.count -= intvolume
            
            
            
            
            # cube (the new one) intersects otherCube
            # decompose otherCube into subcubes not intersecting 
            decomposedCubes = Space.decomposeCube(otherCube, intersection)
            
            decVolume = sum(Space.getVolume(c) for c in decomposedCubes)
            
            if decVolume != (oldVolume - intvolume):
                raise Exception("volume errato")
            
            newCubes.extend(decomposedCubes)
        
        self.cubes = newCubes




with open(FILE_NAME) as file:
    
    data = [line.strip().split(" ", 1) for line in file]
    
    
    
    
data = [(status == "on", tuple(extract(s) for s in rhs.split(","))) for status, rhs in data]


space = Space()

for i, (status, cube) in enumerate(data):
    newRanges = tuple(constraintRange(dr, RANGE1) for dr in cube)
    # the range is outside -50:50 in one direction at least
    if any((nr is False) for nr in newRanges):
        continue

    #print(f"{i+1}) {cube}")
    if status:
        space.addCube(cube)
    else:
        space.removeCube(cube)
    
    if PLOT:
        myplot.fig = myplot.plt.figure()
        myplot.ax = myplot.fig.gca(projection='3d')
        myplot.ax.clear()
        for c in space.cubes:
            myplot.drawCube(c, "r")
            
        myplot.drawCube(cube, "g" if status else "y")
        myplot.plt.show()
        myplot.plt.close()

print("Part One: Execute the reboot steps. Afterward, considering only cubes in the region x=-50..50,y=-50..50,z=-50..50, how many cubes are on?")
print(space.count)


space = Space()
#print(space.count)

for i, (status, cube) in enumerate(data):
    #print(f"{i+1}) {cube}")
    if status:
        space.addCube(cube)
    else:
        space.removeCube(cube)
    
    num = sum(Space.getVolume(cube) for cube in space.cubes)
    if num != space.count:
        print(f"diverso allo step {i+1}: sum = {num}, count = {space.count}")


print()
print("Part Two: Starting again with all cubes off, execute all reboot steps. Afterward, considering all cubes, how many cubes are on?")
print(space.count)
