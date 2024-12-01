CUBE_NETS = "cubenets"

from itertools import groupby
from enum import Enum,auto
from dataclasses import dataclass
from copy import deepcopy

import numpy as np

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


SQUARESIZE = 7


class Orientation(Enum):
    X = 1
    Y = 2
    Z = 3


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
    
    
    def apply(self, vector):
        for m in self.mats:
            #print(list(zip(m,vector)))
            self.results.append(tuple(sum(a*b for a,b in zip(r,vector)) for r in m))
    
    def setCorrectResult(self, translation):        
        for i,result in enumerate(self.results):
            transres = tuple(a-b for a,b in zip(result, translation))
            print(f"{transres=}")
            
            if sum(abs(t) for t in transres) == SQUARESIZE:
                self.resultIndex = i
                
    def applyResult(self, net, translation):
        
        # get the correct matrix
        matrix = self.mats[self.resultIndex]
        
        # translate to the same origin for all
        net.translate(translation)
        
        # rotate
        net.rotate(matrix)
        
        # change the orientation for the net
        # if the orientation is Z and the rotation is X -> Y (et cetera)
        orientations = [o for o in Orientation if o not in (self.axis, net.orientation)]
        net.orientation = orientations[0]
        
        # undo the original translation
        net.restore(translation)
        


@dataclass
class Net:
    position: tuple[int]
    orientation: Orientation
    fixed: bool
    def __init__(self, x, y, orientation):
        self.position = (x, y, 0)
        self.orientation = orientation
        self.fixed = False
        self.visitedAllNeigh = False
    
    def translate(self, v):
        self.position = tuple(a+b for a,b in zip(self.position, v))
        
    def restore(self, v):
        self.position = tuple(a-b for a,b in zip(self.position, v))
        
    def rotate(self, matrix):
        self.position = tuple(sum(a*b for a,b in zip(r,self.position)) for r in matrix)

    def dist(self, other):
        return sum(abs(a-b) for a,b in zip(self.position, other.position))
    
    def getTranslation(self, other):
        diff = list((a-b)//2 for a,b in zip(self.position, other.position))
        
        orientations = [o for o in Orientation]
        
        orientation = None
        for i,d in enumerate(diff):
            if d != 0:
                continue
            
            if orientations[i] == self.orientation:
                continue
            
            orientation = orientations[i]
        
        diff[self.orientation.value - 1] = -self.position[self.orientation.value - 1]
        
        
        return tuple(diff), orientation
        

@dataclass
class NetSquares:
    nets: list[Net]
    def __init__(self):
        self.nets = []
        
    def add(self, net):
        self.nets.append(net)
        
    def translateAll(self, v):
        for net in self.nets:
            net.translate(v)
    
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
                
    
    def drawSphere(self, ax, point, color):
        x,y,z = point

        ax.plot([x], [y], [z], markerfacecolor=color, markeredgecolor=color, marker='o', markersize=5)
        
    
    def plotAll(self, neighbour = None):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        
        M = 7*SQUARESIZE
        
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
                    #for yl in range(yr[0]+1, yr[1], 2):
                        #for zl in range(zr[0]+1, zr[1], 2):
                            #self.drawSphere(ax, (x, yl, zl), color)
                case Orientation.Y:
                    xx,zz = np.meshgrid(xr, zr)
                    yy = y
                    #for xl in range(xr[0]+1, xr[1], 2):
                        #for zl in range(zr[0]+1, zr[1], 2):
                            #self.drawSphere(ax, (xl, y, zl), color)
                case Orientation.Z:
                    xx,yy = np.meshgrid(xr, yr)
                    zz = np.zeros([len(xx), len(xx[0])], int) + z
                    #for xl in range(xr[0]+1, xr[1], 2):
                        #for yl in range(yr[0]+1, yr[1], 2):
                            #self.drawSphere(ax, (xl, yl, z), color)
                        
            
            ax.plot_wireframe(xx, yy, zz, color=color)
            ax.plot_surface(xx, yy, zz, color=color, alpha=0.2)
        
        if False:
            pass
        plt.show()
    
    def __bool__(self):
        return bool(self.nets)
             


with open(CUBE_NETS) as file:
    lst = [line.strip() for line in file]
    
    netlists = list(list(g) for k,g in groupby(lst, key=lambda x: len(x) > 0) if k)
    
    
    for netlist in netlists:
        ns = NetSquares()
        
        cstart = -netlist[0].index("#")
        
        for r,row in enumerate(netlist):
            for c,cell in enumerate(row, start=cstart):
                print(f"{cell=} at {r=}, {c=}")
                if cell == ".":
                    continue
                
                net = Net(c * 2*SQUARESIZE, -r * 2*SQUARESIZE, Orientation.Z)
                
                if not ns:
                    net.fixed = True
                    
                ns.add(net)
        
        ns.translateAll((0,0,-SQUARESIZE))
        
        print(f"{ns=}")
        ns.plotAll()
        
        
        while ns.hasUnfixed():
            fixed, neighbour = ns.getFirstFixedNeighbour()
            print("\n\n")
            print(f"{fixed=}")
            print(f"{neighbour=}")
            
            #ns.plotAll(neighbour)
            
            # centers the line between the two centers around 0,0
            translation, rotationAxis = fixed.getTranslation(neighbour)
            print(translation, rotationAxis)
            
            neighbour.translate(translation)
            #print(fixed)
            #print(neighbour)
            
            #ns.plotAll()
            
            
            m = RotationMatrix(rotationAxis)
            m.apply(neighbour.position)
            m.setCorrectResult(translation)
            
            neighbour.restore(translation)
            
            toRotate = ns.getAllUnfixedTouching(neighbour)
            
            
            for net in toRotate:
                m.applyResult(net, translation)
            
            neighbour.fixed = True
            
            #ns.plotAll()
        ns.plotAll()
        
        #print(ns)
