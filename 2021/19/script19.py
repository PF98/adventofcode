from functools import reduce
import re
import math

FILE_NAME = "example2d"
FILE_NAME = "example"
FILE_NAME = "input"


SKIP_PART_1 = True


OVERLAP_NUM = 12
#OVERLAP_NUM = 3

# counter-clockwise rotations about the given axis
ROT = {
    "xc": lambda x,y,z: (x, -z, y), 
    "yc": lambda x,y,z: (z, y, -x),
    "zc": lambda x,y,z: (-y, x, z), # 1,0,0 => 0,1,0 | 0,1,0 => -1,0,0
    "xcc": lambda x,y,z: (x, z, -y),
    "ycc": lambda x,y,z: (-z, y, x),
    "zcc": lambda x,y,z: (y, -x, z), # 0,1,0 => 1,0,0
}


# default rotation: facing x > 0
ROTATIONS = [
    # face x > 0 (do nothing)
    *(["xc"] * r for r in range(4)),
    
    # face y > 0 (z counter clockwise) (0,1,0 => 1,0,0)
    *(["zcc"] + ["yc"] * r for r in range(4)),
    
    # face x < 0 (2*zc) (-1,0,0 => 1,0,0)
    *(["zc"]*2 + ["xc"] * r for r in range(4)),
    
    # face y < 0 (z clockwise (0,-1,0 => 1,0,0)
    *(["zc"] + ["yc"] * r for r in range(4)),
    
    # face z > 0 (y clockwise) (0,0,1 => 1,0,0)
    *(["yc"] + ["zc"] * r for r in range(4)),
    
    # face z < 0 (y counter clocwise) (0,0,-1 => 1,0,0)
    *(["ycc"] + ["zc"] * r for r in range(4)),
]

REV_ROTATIONS = [[f"{s}c" if len(s) == 2 else s[:2] for s in reversed(r)] for r in ROTATIONS]

def reverseRotation(r):
    return [f"{s}c" if len(s) == 2 else s[:2] for s in reversed(r)]


class Scanner:
    def __init__(self, num):
        self.num = num
        self.beacons = []
        self.rotBeacons = [None] * len(ROTATIONS)
        self.rot = None
        self.pos = None
        
        # map of num => (scanner obj, its coords in my ref., the transform to get my coords in its ref.)
        self.others = {}

    def __repr__(self):
        return f"S({self.num})"

    def addBeacon(self, b):
        self.beacons.append(b)
    
    def rotate(self, ri):
        self.rot = ri

        if self.rotBeacons[ri] is not None:
            return
        
        r = ROTATIONS[ri]
        self.rotBeacons[ri] = [rotate(p, r) for p in self.beacons]
        
        
        
    def getAllScannerPositions(self, fr = None, used = set(), d = 0):
        scanners = set()
        for n in self.others:
            if n in used:
                continue
            
            obj, coords, rotObj = self.others[n]
            
            newScanners = obj.getAllScannerPositions(self.num, set((*used, self.num)), d+1)
            
            scanners.update((n, move(p, coords)) for n,p in newScanners)
            
        scanners.add((self.num, (0,0,0)))
        if fr is not None:
            obj, coords, rotObj = self.others[fr]
            
            rotInv, r, ri = rotObj
            
            scanners = set((n, rotate(p, r)) for n,p in scanners)
                
        else:
            return list(scanners)
        
        return scanners




    def getAllBeacons(self, fr = None, used = set(), d = 0):
        #print(f"{'    '*d}Called get on {self.__repr__()} from {fr} having used {used}")
        
        beacons = set()
        for n in self.others:
            #if fr is not None:
                #break
            
            if n in used:
                continue
            
            obj, coords, rotObj = self.others[n]
            
            # gets all of the beacons from my perspective
            newBeacons = obj.getAllBeacons(self.num, set((*used, self.num)), d+1)
            
            beacons.update(move(b, coords) for b in newBeacons)
            #beacons.update((move(b, coords), orig) for b,orig in newBeacons)
            
        if fr is not None:
            obj, coords, rotObj = self.others[fr]
            
            rotInv, r, ri = rotObj
            
            # it means that "self" was the fixed one, "fr" was the rotated one
            # therefore the rotation should be done by r (it's reverse: rr) itself to get in the frame of reference of "fr"
            if rotInv:
                beacons.update(self.beacons)
                #beacons.update((b,self.num) for b in self.beacons)
                
                beacons = set(rotate(p, r) for p in beacons)
                #beacons = set((rotate(p, r), orig) for p,orig in beacons)
                
                
            # "self" was the rotated one, "fr" was the fixed one
            # every beacon is now in the frame of reference of "self",
            # therefore the rotation should be done by r (the direct one) to get to the frame of reference of the fixed one
            else:
                beacons = set(rotate(p, r) for p in beacons)
                #beacons = set((rotate(p, r), orig) for p,orig in beacons)

                # for some points we already have it calculated
                beacons.update(self.rotBeacons[ri])
                #beacons.update((b,self.num) for b in self.rotBeacons[ri])
                
        else:
            beacons.update(self.beacons)
            return list(beacons)
            #beacons.update((b,self.num) for b in self.beacons)
        
        return beacons
    


    
    def findMatch(self, s2):
        for ri,r in enumerate(ROTATIONS):
            s2.rotate(ri)
            for i1,p1 in enumerate(self.beacons[:-(OVERLAP_NUM-1)]):
                for i2,p2 in enumerate(s2.rotBeacons[s2.rot]):
                    #print(f"        hypothesis: p1 {p1} and p2 {p2} (formerly {s2.beacons[i2]} are the same point")
                    # hypothesise p1 and p2 are in the same point
                    # therefore every point in s2 should be moved by (p1 - p2) to be in the same frame of reference
                    
                    diff = tuple(a-b for a,b in zip(p1, p2))
                    
                    #matches = (p for p in s2.rotBeacons[s2.rot] if move(p, diff) in self.beacons)
                    cnt = sum(1 for p in s2.rotBeacons[s2.rot] if move(p, diff) in self.beacons)
                    
                    # overlap successful
                    if cnt >= OVERLAP_NUM:
                        r = ROTATIONS[s2.rot]
                        rr = REV_ROTATIONS[s2.rot]
                        
                        self.others[s2.num] = (s2, diff, (True, rr, ri))
                        s2.others[self.num] = (self, tuple(-c for c in rotate(diff, rr)), (False, r, ri))
                        
                        return True, (cnt, s2.rot, i1, i2, diff)
                
        return False, None
        
NUMS = [(1,0,0), (0,1,0), (0,0,1)]

def move(p, dist):
    return tuple(a+b for a,b in zip(p, dist))

def rotate(p, r):
    for string in r:
        rot = ROT[string]
        p = rot(*p)
    return p

def matchAll(scanners):
    for i,s1 in enumerate(scanners):
        for j,s2 in enumerate(scanners[i+1:]):
            j += i+1
            #print(f"Trying to match {i} with {j}")
            res, obj = s1.findMatch(s2)
            if res:
                num, ri, pi1, pi2, coords = obj
                #print(f"Matched scanners {i}-{j} with rot {ri}: [{', '.join(ROTATIONS[ri])}] on {num} matches with points {pi1} {s1.beacons[pi1]} and {pi2} {s2.rotBeacons[s2.rot][pi2]}")
                #print(f"  therefore s2 is at coords {coords}")
                #print()
                    
            #break
        #break

with open(FILE_NAME) as file:
    scanners = []
    
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        m = re.match("--- scanner (\d+) ---", line)
        if m is not None:
            num = int(m.group(1))
            scanners.append(Scanner(num))
            continue
        scanners[-1].addBeacon(tuple(int(n) for n in line.split(",")))
            
    
    
    
    print("Part One: Assemble the full map of beacons. How many beacons are there?")
    if not SKIP_PART_1:
    # part 1: runtime 2-3 minutes
    
        matchAll(scanners)
        root = scanners[0]
        ab = root.getAllBeacons()
        print(len(ab))


        scannerPos = root.getAllScannerPositions()
        
    else:
        print("378 -- skipped because of a case of long runtime")
        # part 2: i have scannerPos buffered in case i don't want to wait 3 minutes for part 1
        scannerPos = [(0, (0, 0, 0)), (1, (3500, 3631, -1219)), (2, (3584, -1097, 28)), (3, (3552, 2494, -1276)), (4, (2321, 1180, -92)), (5, (1117, 110, 2)), (6, (-118, 62, 1184)), (7, (3594, -16, 5)), (8, (2259, 2358, -125)), (9, (-1206, -2265, 60)), (10, (1157, 125, 1081)), (11, (1205, 1180, 2285)), (12, (2428, -8, 1258)), (13, (1213, -1163, -83)), (14, (4662, 1149, 6)), (15, (2292, 3715, 68)), (16, (1106, -2264, 11)), (17, (-119, -2390, -58)), (18, (1146, -1076, 1131)), (19, (3525, 2487, -110)), (20, (2358, 35, 55)), (21, (1066, -1172, 2432)), (22, (3499, 3664, 41)), (23, (-1223, 55, 1)), (24, (3597, 1300, 46)), (25, (3549, 2476, -2383)), (26, (1195, 48, 2365)), (27, (-1195, -3575, -30)), (28, (4638, 2451, -106)), (29, (3504, 1269, -1287)), (30, (3532, 1263, 1097))]
    
    
    manDist = max(sum(abs(c1-c2) for c1,c2 in zip(p1,p2)) for i1,(_,p1) in enumerate(scannerPos) for _,p2 in scannerPos[i1+1:])
    #manDist = [list(zip(p1,p2)) for i1,p1 in enumerate(ab) for p2 in ab[i1+1:]]
    
    print()
    print("Part Two: What is the largest Manhattan distance between any two scanners?")
    print(manDist)
