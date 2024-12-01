from functools import reduce
import itertools
import re
import heapq

FILE_NAME = "example"
FILE_NAME = "input"


PART2 = False
PART2 = True



ELEMENT_NAMES = {
    "hydrogen": "H",
    "lithium": "Li",
    "thulium": "Tm",
    "plutonium": "Pu",
    "strontium": "Sr",
    "promethium": "Pm",
    "ruthenium": "Ru",
    "elerium": "El",
    "dilithium": "Dt"
}


FLOOR_NUMS = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eigth", "ninth", "tenth"]
FLOOR_NUMS_DICT = dict(reversed(t) for t in enumerate(FLOOR_NUMS))

FLOORNUM = f"([a-z]+)"
GENERATOR_TOKEN = f"a ([a-z]+) generator"
CHIP_TOKEN = f"a ([a-z]+)-compatible microchip"

MATCH_FLOOR = f"The {FLOORNUM} floor contains"


def getFloorTuple(floors, elevator, elements):
    out = [None] * (2 * len(elements) + 1) # 2 for each element (generator and microchip), elevator at the end
    out[-1] = elevator
    for i,floor in enumerate(floors):
        for elem, typ in floor:
            out[2*elem + typ] = i
            
    return tuple(out)


def getFloorListToPrint(floorTuple, floorCount):
    elemCount = (len(floorTuple) // 2)
    elevator = floorTuple[-1]
    
    out = [[] for _ in range(floorCount)]
    for i,num in enumerate(floorTuple[:-1]):
        elem = (i // 2)
        typ = (i % 2)
        
        out[num].append((elem, typ))
    return elevator, out

CCs = '\033[42m'
OCs = '\033[41m'
Ce = '\033[0m'
def printBuilding(floorTuple, floorCount, elements, prev = None):
    elementStrings = [ELEMENT_NAMES[name] for name in elements]
    maxLen = max(len(s) for s in elementStrings)
    elementStrings = [s.ljust(maxLen) for s in elementStrings]
    
    #print(floorTuple)
    *floors, elevator = floorTuple
    #elevator, floors = getFloorListToPrint(floorTuple, floorCount)
    
    numLen = len(f"{floorCount}")
    print(f"F{'#' * numLen} ", end="")
    print("↕ |", end="") # elevator 
    for e, elementStr in enumerate(elementStrings):
        print(f" {elementStr.center(maxLen + 2, '-')} |", end="")
    print("\n")
    for f in reversed(range(floorCount)):
        print(f"F{str(f + 1).rjust(numLen, '0')} ", end="")
        before = ""
        after = ""
        if prev is not None:
            if prev[-1] == f:
                before += OCs
                after += Ce
            elif elevator == f:
                before += CCs
                after += Ce
                
        elevStr = "E" if (elevator == f) else "."
        print(f"{before}{elevStr}{after}", end="")
        
        print(" | ", end="")
        
        for e, elementStr in enumerate(elementStrings):
            # generator
            for i,L in enumerate(["G", "M"]):
                floor = floors[2*e + i]
                before = ""
                after = ""
                if prev is not None:
                    oldFloor = prev[2*e + i]
                    if floor != oldFloor:
                        if floor == f:
                            before += CCs
                            after += Ce
                        elif oldFloor == f:
                            before += OCs
                            after += Ce
                    
                print(f"{before}{L if floor == f else '.'}{after}", end="")
                
                
                if i < 1:
                    print(" " * maxLen, end="")
                else:
                    print(" | ", end="")
            
        
        
        print()
    print()




cache = {}
visited = set()
def exploreBuilding(floorTuple, floorCount, elements, objectiveFloor, depth = 0):
    visited.add(floorTuple)
    
    printBuilding(floorTuple, floorCount, elements)
    input()
    if floorTuple in cache:
        return cache[floorTuple]
    
    if all(f == objectiveFloor for f in floorTuple):
        cache[floorTuple] = 0
        print("arrived")
        return 0
    
    
    *floors, elevator = floorTuple
    
    currentFloorIndex = [i for i,f in enumerate(floors) if f == elevator]
    #print(currentFloorIndex)
    
    # nothing is on this floor: it should be impossible because we wouldn't have moved to here
    if len(currentFloorIndex) == 0:
        cache[floorTuple] = None
        return None
    
    currentFloorIndex.append(None)
    
    bestSteps = None
    # none will only be in ib
    for indices in itertools.combinations(currentFloorIndex, 2):
        indices = [i for i in indices if i is not None]
        
        moveToOptions = []
        if elevator + 1 < floorCount:
            moveToOptions.append(elevator + 1)
        if elevator - 1 >= 0:
            moveToOptions.append(elevator - 1)
            
        for moveTo in moveToOptions:
            newFloors = [moveTo if i in indices else f for i,f in enumerate(floors)]
            
            newFloorTuple = tuple([*newFloors, moveTo])
            if newFloorTuple in visited:
                continue
            
            # check if newFloors is ok
            ok = True
            newGenerators = newFloors[::2]
            newMicrochips = newFloors[1::2]
            for e,(mf, gf) in enumerate(zip(newMicrochips, newGenerators)):
                # generator and microchip are separated
                if mf != gf:
                    # there is another generator (for element "oe") on the same floor ("ogf")
                    if any(ogf == mf for oe, ogf in enumerate(newGenerators) if oe != e):
                        ok = False
                        break
            
            if not ok:
                continue
            
            
            steps = exploreBuilding(newFloorTuple, floorCount, elements, objectiveFloor, depth + 1)
            if bestSteps is None or (steps is not None and steps < bestSteps):
                bestSteps = steps
        
    out = bestSteps + 1 if bestSteps is not None else None
    cache[floorTuple] = out
    return out






def exploreBuildingDijkstra(floorTuple, floorCount, elements, objectiveFloor):
    dist = {}
    prev = {}
        
    dist[floorTuple] = 0
    prev[floorTuple] = None
    
    visited = set()
    
    # heap of tuples containing (distance, distFromTop, status tuple)
    # distFromTop is a heuristic to consider first the statuses closest to the finished status,
    # in case of an equal distance
    unvisitedHeap = [(dist[floorTuple], 0, floorTuple)]
    
    cnt = 0
    viscnt = 0
    while len(unvisitedHeap) > 0:
        cnt += 1
        #input()
        nodeDist, _, status = heapq.heappop(unvisitedHeap)
        
        #print("\nStepping: ")
        #print(f"  extracted status {status}, with dist = {nodeDist}")
        print(f"dist: {nodeDist}, len: {len(unvisitedHeap)}", end="\r")
        #print(f"Status selected at dist {nodeDist}: {status}, {len(unvisitedHeap)} remaining")
        #printBuilding(status, floorCount, elements)
        #print()
        
        # if we find that a node has a better distance, we don't remove its entry from the heap, we
        # just add a new one to its left in the heap: the later one will then be ignored
        if status in visited:
            continue
        
        viscnt += 1
        visited.add(status)
        
        # end: every other remaining status has a bigger nodeDist value
        if all(f == objectiveFloor for f in status):
            sequence = [status]
            while prev[sequence[-1]] is not None:
                sequence.append(prev[sequence[-1]])
            
            print("\n")
            print(f"reached end")
            return cnt, viscnt, (nodeDist, sequence[::-1])
        
        
        *floors, elevator = status

        currentFloorIndex = [i for i,f in enumerate(floors) if f == elevator]
        if len(currentFloorIndex) == 0:
            raise Exception(f"elevator: {elevator}, floors: {floors}")
        
        currentFloorIndex.append(None)
        
        # move up or down one floor, if possible
        moveToOptions = []
        if elevator + 1 < floorCount:
            moveToOptions.append(elevator + 1)
        if elevator - 1 >= 0:
            moveToOptions.append(elevator - 1)
            
        # pick all possible combinations of 1 (thanks to None) or 2 elements to move in the elevator
        for indices in itertools.combinations(currentFloorIndex, 2):
            indices = [i for i in indices if i is not None]
            
            
            
            for moveTo in moveToOptions:
                newFloors = [moveTo if i in indices else f for i,f in enumerate(floors)]
                
                newStatus = tuple([*newFloors, moveTo])
                if newStatus in visited:
                    continue
                
                # check if newFloors is ok
                ok = True
                newGenerators = newFloors[::2]
                newMicrochips = newFloors[1::2]
                for e,(mf, gf) in enumerate(zip(newMicrochips, newGenerators)):
                    # generator and microchip are separated
                    if mf != gf:
                        # there is another generator (for element "oe") on the same floor ("ogf")
                        if any(ogf == mf for oe, ogf in enumerate(newGenerators) if oe != e):
                            ok = False
                            break
                
                if not ok:
                    continue
                
                newDist = dist[status] + 1
                
                if newStatus not in dist or newDist < dist[newStatus]:
                    dist[newStatus] = newDist
                    prev[newStatus] = status
                    
                    distFromTop = sum(abs(f - objectiveFloor) for f in newFloors)
                    
                    heapq.heappush(unvisitedHeap, (newDist, distFromTop, newStatus))
                    #heapq.heappush(unvisitedHeap, (newDist, 0, newStatus))
    
    return cnt, viscnt, None









floors = {}
elements = []
with open(FILE_NAME) as file:
    for line in file:
        line = line.strip()
        
        m = re.match(MATCH_FLOOR, line)
        if m is None:
            raise Exception("cazzo")
        
        floorNum = FLOOR_NUMS_DICT[m.group(1)]
        floor = []
        
        
        for m in re.finditer(GENERATOR_TOKEN, line):
            element = m.group(1)
            if element not in elements:
                elements.append(element)
            
            floor.append((elements.index(element), 0))
        
        for m in re.finditer(CHIP_TOKEN, line):
            element = m.group(1)
            if element not in elements:
                elements.append(element)
                
            floor.append((elements.index(element), 1))
        
        floors[floorNum] = floor

floors = [floors[i] for i in range(len(floors))]
#print(floorsTotal)
#print(elements)
#print(floors)

elevator = 0
floorTuple = getFloorTuple(floors, elevator, elements)
floorCount = len(floors)



if PART2:
    elements.extend(["elerium", "dilithium"])
    floorTuple = tuple([*floorTuple[:-1], 0, 0, 0, 0, floorTuple[-1]])


printBuilding(floorTuple, floorCount, elements)



cnt, viscnt, out = exploreBuildingDijkstra(floorTuple, floorCount, elements, floorCount - 1)
print(f"count: {cnt}, of which visited: {viscnt}\n")

if out is None:
    print("not found")
    exit()

#input()

dist, seq = out
#for s,sp in zip(seq, [None, *seq[:-1]]):
    ##print("\n"* 30)
    #printBuilding(s, floorCount, elements, prev = sp)
    #print("-" * 50)
    #input()
#print()
#print(f"distance: {dist}")

if not PART2:
    print("Part One: In your situation, what is the minimum number of steps required to bring all of the objects to the fourth floor?")
else:
    print("Part Two: What is the minimum number of steps required to bring all of the objects, including these four new ones, to the fourth floor?")
    
print(dist)



#print()
#print(reduce(lambda a,b: a*b, (outputs[n] for n in range(3))))
#print(outputs[0])
#print(outputs[1])
#print(outputs[2])
#print(outputs)
