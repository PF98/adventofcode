# TODO: horrible efficiency - minutes

FILE_NAME = "example"
FILE_NAME = "input"

YLINE = 10
YLINE = 2000000


XYMIN = 0
# note: 4000000 for the input, 20 for the example
XYMAX = 2*YLINE


import re


class Intervals:
    def __init__(self):
        self.intervals = []

    def add(self, interval):
        self.intervals.append(tuple(interval))
        
        old = self.intervals
        self.intervals = []
        for begin,end in sorted(old):
            if self.intervals and self.intervals[-1][1] >= begin - 1:
                self.intervals[-1][1] = max(self.intervals[-1][1], end)
            else:
                self.intervals.append([begin, end])
                
        self.intervals = [tuple(t) for t in self.intervals]
    
    def contain(self, num):
        return any(a <= num <= b for a,b in self.intervals)
    
    def width(self):
        return sum(i[1] - i[0] + 1 for i in self.intervals)
    
    def findOutsider(self, lb, hb):
        for interv in self.intervals:
            # discard all intervals before lb
            if interv[1] < lb:
                continue
            
            # the interval ends before hb:
            # this means it wasn't joined to the next: return one value above
            if interv[1] < hb:
                return interv[1] + 1
            else:
                return None

        return None
        


def dist(pa, pb):
    return sum(abs(b - a) for a,b in zip(pa, pb))

def psum(pa, pb):
    return tuple(a+b for a,b in zip(pa, pb))

def pdiff(pa, pb):
    return tuple(a - b for a,b in zip(pa,pb))

def pinv(p):
    return tuple(-c for c in p)

def autorange(start, end):
    return range(start, end+1) if start < end else range(start, end-1, -1)


def getMovementRanges(xtri, ytri, bounds):
    #print(" -> getMovementRanges()")
    wave = (0, 1, 0, -1)
    LEN = len(wave)
    
    for i in range(LEN):
        xrng = (
            xtri[wave[i] + 1],
            xtri[wave[(i+1)%LEN] + 1],
        )
        yrng = (
            ytri[wave[(i+1)%LEN] + 1],
            ytri[wave[(i+2)%LEN] + 1],
        )
        
        #print(f"    {i = }, candidates {xrng=}, {yrng=}")
        out = doubleclamp(xrng, yrng, *bounds)
        
        if out is None:
            continue
        
        xrng, yrng = out
        yield (autorange(*xrng), autorange(*yrng))
    


def clamps(nums, l, h):
    return tuple(l if n <= l else h if n >= h else n for n in nums)


def doubleclamp(xint, yint, l, h):
    if all(l <= c <= h for c in [*xint, *yint]):
        return xint, yint
    
    if min(xint) > h or min(yint) > h:
        #print(f"      not clamping - higher {xint=}, {yint=} with {l=}, {h=}")
        return None
    if max(xint) < l or max(yint) < l:
        #print(f"      not clamping - lower {xint=}, {yint=} with {l=}, {h=}")
        return None
    
    #print(f"      clamping {xint=}, {yint=} with {l=}, {h=}")
    
    # True if the intervals are both increasing, False otherwise
    decreasing = [(xint[1] < xint[0]), (yint[1] < yint[0])]
    deltas = []
    for interv, decr in zip([xint, yint], decreasing):
        clamp = clamps(interv, l, h)
        delta = pdiff(clamp, interv)
        deltas.append(delta if not decr else pinv(delta))
    
    #print(f"       -> {deltas=}")
    
    # cumulative delta
    delta = (max(d[0] for d in deltas), min(d[1] for d in deltas))
    #print(f"       -> {delta=}")
    
    
    xint, yint = (psum(interv, delta) if not decr else pdiff(interv, delta) for interv, decr in zip([xint, yint], decreasing))
    
    
    #print(f"       -> after clamp: {xint=}, {yint=}")
    
    if any(c < l or c > h for c in [*xint, *yint]):
        return None
    
    return xint, yint




with open(FILE_NAME) as file:
    sensors = []
    for line in file:
        m = re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line.strip())
        
        #print(m)
        
        spos = tuple(int(m[n+1]) for n in range(2))
        bpos = tuple(int(m[n+3]) for n in range(2))
        
        sensors.append((spos, bpos))
    
    intervals = Intervals()
    
    
    SBs = []
    for spos,bpos in sensors:
        #print()
        SB = dist(spos, bpos)
        SBs.append(SB)
        dy = abs(spos[1] - YLINE)
    
        #print(f"{spos} -> {SB=}, {dy=}")
        if dy > SB:
            continue
        
        interval = (spos[0] - (SB - dy), spos[0] + (SB - dy))
        intervals.add(interval)
        #print(interval)
        
        #print(intervals.intervals)
        
        
    beaconx = set(bpos[0] for _,bpos in sensors if bpos[1] == YLINE)
    
    
    print("Part One: Consult the report from the sensors you just deployed. In the row where y=2000000, how many positions cannot contain a beacon?")
    print(intervals.width() - sum(1 for x in beaconx if intervals.contain(x)))
    
    
    
    
    # base change
    def baseChange(x,y):
        return (x+y, x-y)
    
    # squares, as a tuple of (center, half-side-length
    squares = [(baseChange(*spos), SB) for (spos,_), SB in zip(sensors, SBs)]
    
    points = set()
    
    for center, halflen in squares:
        # 5,25
        xs = [center[0] + (halflen + 1) * (2*r - 1) for r in range(2)]
        # -9,11
        ys = [center[1] + (halflen + 1) * (2*r - 1) for r in range(2)]
        
        
        #print()
        #print(f"{center=} -> {halflen=}")
        #print(f"  {xs=}\n  {ys=}\n-------------------")
        # 5, 25
        for xside, yside in zip(xs, ys):
            xsidebound = min(xside, 2*XYMAX - xside) if 0 <= xside <= 2*XYMAX else False
            ysidebound = yside if 0 <= yside <= 2*XYMAX else False
            
            if xsidebound is False and ysidebound is False:
                #print("both sides are all outside")
                continue
            
            
            xints = Intervals()
            yints = Intervals()
            for (c2,hl2) in squares:
                if (center == c2 and halflen == hl2):
                    continue
                
                xs2 = [c2[0] + hl2 * (2*r - 1) for r in range(2)]
                ys2 = [c2[1] + hl2 * (2*r - 1) for r in range(2)]
                
                
                # overlap between the x coordinates                
                if xsidebound is not False and (xs2[0] < xside < xs2[1]):
                    xints.add(ys2)
                
                
                # overlap between the y coordinates
                if ysidebound is not False and not (ys2[0] < yside < ys2[1]):
                    yints.add(xs2)
            
            
            if xsidebound is not None:
                xboundsmath = (-xsidebound, xsidebound)
                xbounds = (max(xboundsmath[0], ys[0]), min(xboundsmath[1], ys[1]))
                #print(f"  for {xside=}, intervals {xints.intervals=}")
                #print(f"   -> but with {xboundsmath=}, {ys=}, the bounds become {xbounds=}")
                
                #print(f"   => {xints.findOutsider(*xbounds)=}")
                
                outsider = xints.findOutsider(*xbounds)
                if outsider is not None:
                    points.add((xside, outsider))
                    print(f"found an ousider on side {xside=}, with coordinate {outsider}")
                
            if ysidebound is not None:
                yboundsmath = (ysidebound, 2*XYMAX - ysidebound)
                ybounds = (max(yboundsmath[0], xs[0]), min(yboundsmath[1], xs[1]))
                #print(f"  for {yside=}, intervals {yints.intervals=}")
                #print(f"   -> but with {yboundsmath=}, {xs=}, the bounds become {ybounds=}")
    
                #print(f"   => {yints.findOutsider(*ybounds)=}")
                
                outsider = yints.findOutsider(*ybounds)
                if outsider is not None:
                    points.add((outsider, yside))
                    print(f"found an ousider on side {yside=}, with coordinate {outsider}")
    
    
    print(points)
    
    for p in points:
        op = (sum(p) // 2, (p[0]-p[1])//2)
        print(f"excluded point: {p}, originally {op}, with frequency {op[0] * 4000000 + op[1]}")
    
    exit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    print()
    points = set()
    for (spos,_), SB in zip(sensors, SBs):
        
        xtri = tuple(spos[0] + (SB+1) * (r-1) for r in range(3))
        ytri = tuple(spos[1] + (SB+1) * (r-1) for r in range(3))
        print()
        print(f"{spos} -> {SB=}")
        #print(f"{xtri=}, {ytri=}")
        for (sensor,_), sensorSB in zip(sensors, SBs):
            senssumval = [sum(sensor) + (sensorSB) * (2*r - 1) for r in range(2)]
            sensdiffval = [sensor[0] - sensor[1] + (sensorSB) * (2*r - 1) for r in range(2)]
        
            # sum is a constant: lines like these / /
            # values of the const: x+y = xs + ys +- (SB + 1)
            for maxmove in [(SB + 1) * (2*r - 1) for r in range(2)]:
                sumval = sum(spos) + maxmove
                # the origin is the point on the line that minimizes the difference
                origin = (spos[0], spos[1] + maxmove) if maxmove > 0 else (spos[0] - maxmove, spos[1])
                
                # there is not an intersection (squares to eliminate)
                if not (senssumval[0] <= sumval <= senssumval[1]):
                    continue
                
                # there is an intersection
                #intersections = 
                print(sumval, origin)
            
            # difference is a constant: lines like these \ \
            # values of the const: x-y = xs - ys +- (SB + 1)
            for maxmove in [(SB + 1) * (2*r - 1) for r in range(2)]:
                diffval = spos[0] - spos[1] + maxmove
                # minimize the sum
                origin = (spos[0], spos[1] - maxmove) if maxmove > 0 else (spos[0] + maxmove, spos[1])
                print(diffval, origin)
                
                if not (sensdiffval[0] <= diffval <= sensdiffval[1]):
                    continue
        #for xrng, yrng in getMovementRanges(xtri, ytri, (XYMIN, XYMAX)):
            ##print(xrng, yrng)
            #for x,y in zip(xrng, yrng):
                #if any(dist(sensor, (x,y)) <= sensorSB for (sensor,_), sensorSB in zip(sensors, SBs)):
                    #continue
                
                #points.add((x,y))
                #print(f" -> added ({x,y})")
                #print(4000000 * x + y)
                ##matrix[y][x] = "#"
            ##p(matrix)
        
    
    print(points)
    
    #print()
    #print("Part Two: Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?")
    #print(sum(chunks[-3:]))
