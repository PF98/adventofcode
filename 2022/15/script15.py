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
        
        # union of intervals: code from stackoverflow
        # https://stackoverflow.com/questions/15273693/union-of-multiple-ranges/15273749#15273749
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


# base change
def baseChange(x,y):
    return (x+y, x-y)


with open(FILE_NAME) as file:
    # input parsing
    sensors = []
    for line in file:
        m = re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line.strip())
        
        #print(m)
        
        spos = tuple(int(m[n+1]) for n in range(2))
        bpos = tuple(int(m[n+3]) for n in range(2))
        
        sensors.append((spos, bpos))
    
    # PART 1
    
    intervals = Intervals()
    
    SBs = []
    for spos,bpos in sensors:
        SB = dist(spos, bpos)
        SBs.append(SB)
        dy = abs(spos[1] - YLINE)
    
        if dy > SB:
            continue
        
        interval = (spos[0] - (SB - dy), spos[0] + (SB - dy))
        intervals.add(interval)
        
    beaconx = set(bpos[0] for _,bpos in sensors if bpos[1] == YLINE)
    
    
    print("Part One: Consult the report from the sensors you just deployed. In the row where y=2000000, how many positions cannot contain a beacon?")
    print(intervals.width() - sum(1 for x in beaconx if intervals.contain(x)))
    
    
    
    # PART 2
    
    # squares, as a tuple of (center, half-side-length)
    squares = [(baseChange(*spos), SB) for (spos,_), SB in zip(sensors, SBs)]
    
    points = set()
    
    for center, halflen in squares:
        xs = [center[0] + (halflen + 1) * (2*r - 1) for r in range(2)]
        ys = [center[1] + (halflen + 1) * (2*r - 1) for r in range(2)]
        
        for xside, yside in zip(xs, ys):
            xsidebound = min(xside, 2*XYMAX - xside) if 0 <= xside <= 2*XYMAX else False
            ysidebound = yside if 0 <= yside <= 2*XYMAX else False
            
            if xsidebound is False and ysidebound is False:
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
                
                outsider = xints.findOutsider(*xbounds)
                if outsider is not None:
                    points.add((xside, outsider))
                
            if ysidebound is not None:
                yboundsmath = (ysidebound, 2*XYMAX - ysidebound)
                ybounds = (max(yboundsmath[0], xs[0]), min(yboundsmath[1], xs[1]))
                
                outsider = yints.findOutsider(*ybounds)
                if outsider is not None:
                    points.add((outsider, yside))
    
        
    print()
    print("Part Two: Find the only possible position for the distress beacon. What is its tuning frequency?")
    
    for p in points:
        op = (sum(p) // 2, (p[0]-p[1])//2)
        print(op[0] * 4000000 + op[1])


