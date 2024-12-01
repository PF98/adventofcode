FILE_NAME = "example"
FILE_NAME = "input"


if FILE_NAME == "example":
    TESTAREA = (7,27)
else:
    TESTAREA = (200000000000000,400000000000000)

from dataclasses import dataclass
import itertools

def extr(s):
    return (int(e) for e in s.split(","))

@dataclass
class Hail:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int
    def __init__(self, pos, vel):
        self.x, self.y, self.z = pos
        self.vx, self.vy, self.vz = vel
        
        # straight line: (x = sx + svx*t, y = sy + svy*t)
        # therefore svx*svt*t = svy*(x - sx), svx*svy*t = svx*(y - sy)
        # and thus svy*(x - sx) = svx*(y - sy)
        # thus svy*x - svx*y = sx*svy - sy*svx
        
        # straight line as ax + by = c    
        self.a = self.vy
        self.b = -self.vx
        self.c = self.x*self.vy - self.y*self.vx
        
        
    def pathCross(self, other, testarea):
        # system, directly from the parametric equations
        #     .-         -.   .- -.   .-       -.
        #     | vsx  -vox |   | t |   | xo - xs |
        #     |           | * |   | = |         |
        #     | vsy  -voy |   | s |   | yo - ys |
        #     '-         -'   '- -'   '-       -'
        # where t and s are the parameters for "self" and "other", respectively
        delta = self.vx * (- other.vy) - self.vy * (- other.vx)
        
        # either parallel or overlapping
        if delta == 0:
            # if overlapping: the system is indeterminate
            # vsx/vsy = vox/voy (and thus delta is zero)
            # and vsx/vsy = (xo-xs)/(yo-ys), or better vsx*(yo-ys) = vsy*(xo-xs)
            if self.vx * (other.y - self.y) == self.vy * (other.x - self.x):
                raise Exception()
            # if parallel but not overlapping: no solutions
            else:
                return False
                
        
        deltaST = (other.x - self.x)  * (- other.vy) - (other.y - self.y) * (- other.vx)
        deltaOT = self.vx * (other.y - self.y) - self.vy * (other.x - self.x)
        
        if delta < 0:
            delta = -delta
            deltaST = -deltaST
            deltaOT = -deltaOT

        # st < 0 or ot < 0:
        # since delta is positive, we just need to check for the sign of deltaST
        # and deltaOT
        if deltaST < 0 or deltaOT < 0:
            return False
        
        
        
        #st = deltaST/delta
        #ot = deltaOT/delta
        
        
        tl,th = testarea
        # tl <= x,y <= th
        # tl <= self.{x,y} + self.v{x,y} * deltaST/delta <= th
        # 
        # tl*delta <= self.{x,y} * delta + self.v{x,y} * deltaST <= th*delta
        
        xval = self.x * delta + self.vx * deltaST
        yval = self.y * delta + self.vy * deltaST
        
        
        
        return (tl*delta <= xval <= th*delta) and (tl*delta <= yval <= th*delta)
        

hails = []
with open(FILE_NAME) as file:
    hails = [Hail(*(list(extr(s)) for s in line.strip().split("@"))) for line in file]


print("Part One:")
print(sum(1 for h1,h2 in itertools.combinations(hails, 2) if h1.pathCross(h2, TESTAREA)))


i0 = 0
i1 = 1
i2 = 2

x0 = hails[i0].x
y0 = hails[i0].y
z0 = hails[i0].z
x1 = hails[i1].x
y1 = hails[i1].y
z1 = hails[i1].z
x2 = hails[i2].x
y2 = hails[i2].y
z2 = hails[i2].z

vx0 = hails[i0].vx
vy0 = hails[i0].vy
vz0 = hails[i0].vz
vx1 = hails[i1].vx
vy1 = hails[i1].vy
vz1 = hails[i1].vz
vx2 = hails[i2].vx
vy2 = hails[i2].vy
vz2 = hails[i2].vz


import z3

t0 = z3.Int("t0")
t1 = z3.Int("t1")
t2 = z3.Int("t2")
xs = z3.Int("xs")
ys = z3.Int("ys")
zs = z3.Int("zs")
vsx = z3.Int("vsx")
vsy = z3.Int("vsy")
vsz = z3.Int("vsz")

solver = z3.Solver()
solver.add(
    x0 + vx0*t0 == xs + vsx*t0,
    y0 + vy0*t0 == ys + vsy*t0,
    z0 + vz0*t0 == zs + vsz*t0,
    x1 + vx1*t1 == xs + vsx*t1,
    y1 + vy1*t1 == ys + vsy*t1,
    z1 + vz1*t1 == zs + vsz*t1,
    x2 + vx2*t2 == xs + vsx*t2,
    y2 + vy2*t2 == ys + vsy*t2,
    z2 + vz2*t2 == zs + vsz*t2,
)

solver.check((t0 >= 0, t1 >= 0, t2 >= 0))

solution = solver.model()
print()
print("Part Two:")
print(sum(solution[v].as_long() for v in (xs,ys,zs)))
#print(solution)
