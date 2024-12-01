CUBE_NETS = "cubenets"

FILE_NAME = "example"
FILE_NAME = "input"

SQUARESIZE = 4
SQUARESIZE = 50

PLOT = False

from itertools import groupby
from enum import Enum,auto
from dataclasses import dataclass
from copy import deepcopy


if PLOT:
    import numpy as np

    from mpl_toolkits import mplot3d
    import matplotlib.pyplot as plt




class Orientation(Enum):
    X = 1
    Y = 2
    Z = 3
    
    def get(key):
        return list(Orientation)[key]
    
class Transformation(Enum):
    TRANSLATION = auto()
    ROTATION = auto()

class RotationMatrix:
    # axis around which it rotates
    # |    Rx    |    Ry    |    Rz    |
    # +----------+----------+----------+
    # |  1  0  0 |  0  0 ±1 |  0 ∓1  0 |
    # |  0  0 ±1 |  0  1  0 | ±1  0  0 |
    # |  0 ∓1  0 | ∓1  0  0 |  0  0  1 |
    # +----------+----------+----------+
    def __init__(self, axis):
        self.axis = axis
        
        mat = [[0]*3 for _ in range(3)]
        
        i1 = axis.value - 1
        i2 = (i1 + 1) % 3
        i3 = (i1 + 2) % 3
        
        mat[i1][i1] = 1
        
        self.mats = [deepcopy(mat), deepcopy(mat)]
        
        for n,m in enumerate(self.mats):
            m[i2][i3] = (2*n - 1)
            m[i3][i2] = -(2*n - 1)
            
        self.results = []
        self.matrix = None
        self.resultIndex = None
    
    
    def apply(self, vector):
        for m in self.mats:
            self.results.append(tuple(sum(a*b for a,b in zip(r,vector)) for r in m))
    
    def setCorrectResult(self, translation):     
        for i,result in enumerate(self.results):
            transres = tuple(a-b for a,b in zip(result, translation))
            
            if sum(abs(t) for t in transres) == SQUARESIZE:
                self.resultIndex = i
        # get the correct matrix
        self.matrix = self.mats[self.resultIndex]
                
    def applyResult(self, net, translation):
        # translate to the same origin for all
        net.translate(translation)
        
        # rotate
        net.rotate(self)
        
        # undo the original translation
        net.restore(translation)
    
    
    def getOppositeRotation(self, resultIndex):
        self.resultIndex = 1 - resultIndex
        self.matrix = self.mats[self.resultIndex]
    
    def applySingleResult(self, vector, resultIndex):
        self.resultIndex = resultIndex
        self.matrix = self.mats[self.resultIndex]
        
        return tuple(sum(a*b for a,b in zip(r,vector)) for r in self.matrix)
        


@dataclass
class Net:
    position: tuple[int]
    orientation: Orientation
    fixed: bool
    def __init__(self, x, y, z, orientation, block):
        self.position = (x, y, z)
        self.orientation = orientation
        self.fixed = False
        self.visitedAllNeigh = False
        self.rocks = set()
        self.transformations = []
        
        for r,row in enumerate(block):
            yr = y + (SQUARESIZE - 1) - 2*r
            for c,cell in enumerate(row):
                if cell == ".":
                    continue
                
                xr = x - (SQUARESIZE - 1) + 2*c
                self.rocks.add((xr, yr , z))
    
    def getInitialPos(self, pos):
        c,r = pos
        
        x,y,z = self.position
        
        return (x - (SQUARESIZE - 1) + 2*c, y + (SQUARESIZE - 1) - 2*r, z)
    
    def translate(self, v, remember = True):
        self.position = tuple(a+b for a,b in zip(self.position, v))
        
        if remember:
            self.transformations.append((Transformation.TRANSLATION, v))
            newRocks = set()
            for rock in self.rocks:
                newRocks.add(tuple(a+b for a,b in zip(rock, v)))
                
            self.rocks = newRocks
        
    def restore(self, v, remember = True):
        self.position = tuple(a-b for a,b in zip(self.position, v))
        
        if remember:
            self.transformations.append((Transformation.TRANSLATION, tuple(-e for e in v)))
            
            newRocks = set()
            for rock in self.rocks:
                newRocks.add(tuple(a-b for a,b in zip(rock, v)))
                
            self.rocks = newRocks
        
    def rotate(self, m):
        self.position = tuple(sum(a*b for a,b in zip(r,self.position)) for r in m.matrix)
        
        # change the orientation for the net
        # if the orientation is Z and the rotation is X -> Y (et cetera)
        orientations = [o for o in Orientation if o not in (m.axis, self.orientation)]
        self.orientation = orientations[0]
        
        # remember
        self.transformations.append((Transformation.ROTATION, m.axis, m.resultIndex))
        
        newRocks = set()
        for rock in self.rocks:
            newRocks.add(tuple(sum(a*b for a,b in zip(r, rock)) for r in m.matrix))
            
        self.rocks = newRocks
    
    
    def unwrap(self, ns):
        transformations = self.transformations.copy()
        for tup in reversed(transformations):
            match tup:
                case (Transformation.TRANSLATION, v):
                    self.restore(v, True)
                case (Transformation.ROTATION, axis, resultIndex):
                    m = RotationMatrix(axis)
                    m.getOppositeRotation(resultIndex)
                    
                    self.rotate(m)
                    
        self.transformations = transformations
    
    
    def dist(self, other):
        return sum(abs(a-b) for a,b in zip(self.position, other.position))
    
    def getTranslation(self, other):
        diff = list((a-b)//2 for a,b in zip(self.position, other.position))
        
        
        orientation = None
        for i,d in enumerate(diff):
            if d != 0:
                continue
            
            if Orientation.get(i) == self.orientation:
                continue
            
            orientation = Orientation.get(i)
        
        diff[self.orientation.value - 1] = -self.position[self.orientation.value - 1]
        
        
        return tuple(diff), orientation
    
    def isOutside(self, pos):
        return any(abs(coord) > SQUARESIZE for coord in pos)
    
    def isRock(self, pos):
        return pos in self.rocks
    
            
        

@dataclass
class NetSquares:
    nets: list[Net]
    def __init__(self):
        self.nets = []
        
    def add(self, net):
        self.nets.append(net)
            
    def hasUnfixed(self):
        return any(not n.fixed for n in self.nets)
    
    def getFirstFixedNeighbour(self):
        for net in self.nets:
            if not net.fixed:
                continue
            
            for n2 in self.nets:
                # same net, the second is fixed or the two have different orientations
                if net is n2 or n2.fixed or net.orientation != n2.orientation:
                    continue
                
                # nets not adjacent
                if net.dist(n2) != 2*SQUARESIZE:
                    continue
                
                return net, n2
        
        return None, None
    
    def getAllUnfixedTouching(self, neigh):
        candidates = [n for n in self.nets if not n.fixed and n is not neigh and n.orientation == neigh.orientation]
        out = [neigh]
        
        changed = True
        while changed:
            changed = False
            
            for net in candidates:
                if any(net is outnet for outnet in out):
                    continue
                
                for outnet in out:
                    if net.dist(outnet) != 2*SQUARESIZE:
                        continue
                
                    out.append(net)
                    changed = True
                
            candidates = [c for c in candidates if all(c is not outnet for outnet in out)]
                    
        return out
    
    def getRotationNet(self, net, position, direction, outsideIndex):
        outsideCoord = position[outsideIndex]
            
        # calculate the center of the new net
        newCenter = [0]*3
        newCenter[outsideIndex] = SQUARESIZE * (1 if outsideCoord > 0 else -1)
        newCenter = tuple(newCenter)
        
        newnet = next((n for n in self.nets if n.position == newCenter), None)
        
        ni = net.orientation.value - 1
        # calculate the new direction on the new net
        newDir = [0]*3
        newDir[ni] = (1 if net.position[ni] < 0 else -1)
        
        
        # calculate the new position on the new net
        newPos = list(position)
        # the coordinate of the orientation of the old square must be ±(SQUARESIZE - 1),
        # which i.e. for net(Z) becomes net.position[Z] + newDir[Z]
        newPos[ni] = net.position[ni] + newDir[ni]
        
        # the coordinate of the orientation of the new square must be ±SQUARESIZE
        nni = newnet.orientation.value - 1
        newPos[nni] = newnet.position[nni]
        
        
        
        return newnet, tuple(newPos), tuple(newDir)
        
        #newPos
            
            
    
    def unwrapAll(self, position):
        for net in self.nets:
            net.unwrap(self)
            
        for tup in reversed(position.net.transformations):
            match tup:
                case (Transformation.TRANSLATION, v):
                    position.backtranslate(v)
                case (Transformation.ROTATION, axis, resultIndex):
                    m = RotationMatrix(axis)
                    m.getOppositeRotation(resultIndex)
                    
                    position.backrotate(m)
                    
    
    def drawSphere(self, ax, point, color, alpha=1, radius=5):
        x,y,z = point

        ax.plot([x], [y], [z], markerfacecolor=color, markeredgecolor=color, marker='o', markersize=radius, alpha=alpha)
    
    def drawSquare(self, ax, point, orientation, color):
        x,y,z = point
            
        xr = (x-1,x+1)
        yr = (y-1,y+1)
        zr = (z-1,z+1)

        match orientation:
            case Orientation.X:
                yy,zz = np.meshgrid(yr, zr)
                xx = x
            case Orientation.Y:
                xx,zz = np.meshgrid(xr, zr)
                yy = y
            case Orientation.Z:
                xx,yy = np.meshgrid(xr, yr)
                zz = np.zeros([len(xx), len(xx[0])], int) + z
                    
        
        ax.plot_surface(xx, yy, zz, color=color, alpha=0.8)
    
    def plotAll(self, neighbour = None, position = None, final = False):
        if not PLOT:
            return
        
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        
        M = 7*SQUARESIZE if not final else SQUARESIZE
        
        ax.axes.set_xlim3d(left=-M, right=M)
        ax.axes.set_ylim3d(bottom=-M, top=M)
        ax.axes.set_zlim3d(bottom=-M, top=M)
        for net in self.nets:
            color = "red" if net.fixed else "black"
            
            if net is neighbour:
                color = "green"
            
            x,y,z = net.position
            
            xr = (x-SQUARESIZE,x+SQUARESIZE)
            yr = (y-SQUARESIZE,y+SQUARESIZE)
            zr = (z-SQUARESIZE,z+SQUARESIZE)

            match net.orientation:
                case Orientation.X:
                    yy,zz = np.meshgrid(yr, zr)
                    xx = x
                case Orientation.Y:
                    xx,zz = np.meshgrid(xr, zr)
                    yy = y
                case Orientation.Z:
                    xx,yy = np.meshgrid(xr, yr)
                    zz = np.zeros([len(xx), len(xx[0])], int) + z
                        
            
            ax.plot_wireframe(xx, yy, zz, color=color)
            #ax.plot_surface(xx, yy, zz, color=color, alpha=0.2)

        
            for xl,yl,zl in net.rocks:
                self.drawSquare(ax, (xl, yl, zl), net.orientation, color)
                
        if position is not None:
            self.drawSquare(ax, position.pos, position.net.orientation, "blue")
    
        
        plt.show()
    
    def __bool__(self):
        return bool(self.nets)

@dataclass
class Position:
    pos: tuple[int]
    direction: tuple[int]
    def __init__(self, net, pos, direction):
        self.net = net
        self.pos = net.getInitialPos(pos)
        self.direction = direction
    
    
    def backtranslate(self, v):
        self.pos = tuple(a-b for a,b in zip(self.pos, v))
    
        
    def backrotate(self, m):
        self.pos = tuple(sum(a*b for a,b in zip(r,self.pos)) for r in m.matrix)
        self.direction = tuple(sum(a*b for a,b in zip(r,self.direction)) for r in m.matrix)
    
    
    def rotate(self, inst):
        # reversed, because of boh
        # counterclockwise for left, clockwise for right
        pick = 1 if inst == "L" else 0
        
        # if the constant coordinate of the plane is negative: reverse
        if self.net.position[self.net.orientation.value - 1] < 0:
            pick = 1 - pick
        
        m = RotationMatrix(self.net.orientation)
        
        self.direction = m.applySingleResult(self.direction, pick)
        
    def move(self, ns, num):
        
        for i in range(num):
            # 2*d because spots are 2 units away
            newPos = tuple(p+2*d for p,d in zip(self.pos, self.direction))
            newDir = self.direction
            newnet = self.net
            
            # newPos is outside the bounds of the net
            outsideIndex = next((i for i,e in enumerate(newPos) if abs(e) > SQUARESIZE), None)
            if outsideIndex is not None:
                newnet, newPos, newDir = ns.getRotationNet(self.net, newPos, newDir, outsideIndex)
                
            # new position is the rock: stop and keep the old value
            if newnet.isRock(newPos):
                break
        
            # open space: update the position and the net and continue looping
            self.pos = newPos
            self.net = newnet
            self.direction = newDir
    
    def getRowCol(self, cstart):
        x,y,_ = self.pos
        
        # set the leftmost line to 0 (the others to 2, 4, 6, ...)
        x += (SQUARESIZE - 1)
        # set the distance between lines to 1
        x //= 2
        # account for the skipped squares in the top left with cstart
        x -= cstart*SQUARESIZE
        
        # set the topmost line to 0 (the others to -2, -4, -6, ...)
        y -= (SQUARESIZE - 1)
        # set the distance between lines to 1 and make y positive going down
        y = -y//2
        
        return y+1, x+1
    
    def getDirection(self):
        return {
            (1,0,0): 0, # right
            (0,-1,0): 1, # down
            (-1,0,0): 2, # left
            (0,1,0): 3, # up
        }[self.direction]
            


with open(FILE_NAME) as file:
    lst = [line[:-1] for line in file]
    
    *lst, _, instr = lst
    
    gb = groupby(instr, key=lambda x: True if '0' <= x <= '9' else False)
    instructions = [int("".join(g)) if k else "".join(g) for k,g in groupby(instr, key=lambda x: True if '0' <= x <= '9' else False)]

    h = len(lst)
    w = max(len(r) for r in lst)
    
    hn = h // SQUARESIZE
    wn = w // SQUARESIZE
    

    ns = NetSquares()
    
    rows = [lst[r*SQUARESIZE:(r+1)*SQUARESIZE] for r in range(hn)]
    cstart = - min(index for index,value in enumerate(lst[0]) if value != " ")//SQUARESIZE

    # parsing the cube net into a single NetSquares comprised of Net objects
    for r,rowblock in enumerate(rows):
        #print(wn)
        #print(len(rowblock[0])//SQUARESIZE)
        for c in range(min(wn, len(rowblock[0])//SQUARESIZE)):
            block = [row[c*SQUARESIZE:(c+1)*SQUARESIZE] for row in rowblock]
            #print(block)
            
            # empty block
            if block[0][0] == " ":
                continue
            
            net = Net(
                (c + cstart) * 2*SQUARESIZE,
                -r * 2*SQUARESIZE,
                -SQUARESIZE,
                Orientation.Z,
                block
            )
                
            
            if not ns:
                net.fixed = True
                
            ns.add(net)
    
    
    # wrapping the cube
    while ns.hasUnfixed():
        fixed, neighbour = ns.getFirstFixedNeighbour()
        
        # centers the line between the two centers around 0,0 to allow for an easier rotation
        translation, rotationAxis = fixed.getTranslation(neighbour)
        neighbour.translate(translation, remember=False)
        
        # applies the correct rotation to the neighbour and all the squares it reaches
        m = RotationMatrix(rotationAxis)
        m.apply(neighbour.position)
        m.setCorrectResult(translation)
        
        neighbour.restore(translation, remember=False)
        
        toRotate = ns.getAllUnfixedTouching(neighbour)
        
        for net in toRotate:
            m.applyResult(net, translation)
        
        neighbour.fixed = True

        
    # we have built the cube!
    # starting net, position, and direction
    pos = Position(ns.nets[0], (0,0), (1,0,0))
    
    for index,inst in enumerate(instructions):
        func = None
        match inst:
            case "L" | "R":
                pos.rotate(inst)
            case num:
                pos.move(ns, num)
    
    ns.plotAll(position = pos, final=True)
    #print(*pos, direction)
    
    
    
    ns.unwrapAll(pos)
    ns.plotAll(position = pos)
    
    row,col = pos.getRowCol(cstart)
    
    dirNum = pos.getDirection()
    print("Part Two: Fold the map into a cube, then follow the path given in the monkeys' notes. What is the final password?")
    print(1000 * row + 4 * col + dirNum)
    
