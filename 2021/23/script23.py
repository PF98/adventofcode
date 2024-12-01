from functools import reduce
import re
import math
import heapq
from collections import defaultdict

FILE_NAME = "example"
FILE_NAME = "input"


#############
#8 ..->.. 18#
###1#3#5#7###
  #0#2#4#6#
  #########



AMPHIPODS = [chr(i + ord("A")) for i in range(4)]
COSTS = [1, 10, 100, 1000]




class Burrow:
    ROOM_SIZE = 2
    ROOM_COUNT = 4
    ROOM_PLACES = None
    
    CORRIDOR_SIZE = None
    
    ROOM_TO_CORRIDOR = None
    CORRIDOR_TO_ROOM = None
    
    def recalculateConstants():
        Burrow.ROOM_PLACES = Burrow.ROOM_SIZE * Burrow.ROOM_COUNT
        Burrow.CORRIDOR_SIZE = 2*2 + (2*Burrow.ROOM_COUNT - 1)
        Burrow.ROOM_TO_CORRIDOR = dict([i, Burrow.ROOM_PLACES + 2 + 2 * i] for i in range(Burrow.ROOM_COUNT))
        Burrow.CORRIDOR_TO_ROOM = dict(reversed(i) for i in Burrow.ROOM_TO_CORRIDOR.items())
    
    def fromTuple(positions, energy = 0):
        return Burrow(positions, energy)
        pass
    
    def __init__(self, positions, energy = 0):
        self.rooms = [[None] * Burrow.ROOM_SIZE for _ in range(Burrow.ROOM_COUNT)]
        self.corridor = [None] * Burrow.CORRIDOR_SIZE
        
        self.positions = tuple(list(sorted(p)) for p in positions)
        
        self.energy = energy
        
        # t: amphipod type
        for t,lst in enumerate(self.positions):
            for a in lst:
                if a < Burrow.ROOM_PLACES:
                    room = a // Burrow.ROOM_SIZE
                    self.rooms[room][a - room * Burrow.ROOM_SIZE] = t
                else:
                    self.corridor[a - Burrow.ROOM_PLACES] = t
    
    def toEnergyAndTuple(self):
        pos = tuple(tuple(t) for t in self.positions)
        return self.energy, pos
    
    def isFinished(self):
        # all ok if in room index r there are only amphipods with the same index a
        return all(all(r == a for a in room) for r,room in enumerate(self.rooms))
    
    def getEveryMove(self):
        outBurrows = []
        
        
        #self.printStatus()
        # t: type of amph, lst: list of their positions
        for t, lst in enumerate(self.positions):
            for i,pos in enumerate(lst):
                # type t in position pos is moving:
                #print(f"moving type {t}, pos = {pos}")
                #print(self.getOptions(pos, t))
                
                for move, dist in self.getOptions(pos, t):
                    toRoom = (move < Burrow.ROOM_PLACES)
                    
                    newPositions = tuple(list(t) for t in self.positions)
                    newPositions[t][i] = move
                    
                    newEnergy = self.energy + dist * COSTS[t]
                    
                    outBurrows.append(Burrow(newPositions, newEnergy))
        return outBurrows
    
    
    def getOptions(self, pos, t):
        visited = set()
        out = []
        
        toDo = [(0,pos)]
        
        fromCorridor = not (pos < Burrow.ROOM_PLACES)
        
        while len(toDo) > 0:
            dist,pos = toDo.pop()
            #print(f"  Analizing {pos} at dist = {dist}")
            
            visited.add(pos)
            
            # only remember actual moves (not the starting pos with dist = 0)
            if dist == 0:
                pass
            # furthermore you cannot stop in the corridor directly in front of a room
            elif pos in self.CORRIDOR_TO_ROOM:
                pass
            # if it started from corridor, it cannot land on corridor
            elif fromCorridor and not (pos < Burrow.ROOM_PLACES):
                pass
            # otherwise use it as an exit
            else:
                out.append((pos, dist))
            
            # pos is in a room
            if pos < Burrow.ROOM_PLACES:
                #print(f"    in room")
                room = pos // Burrow.ROOM_SIZE
                roomPlace = pos - room * Burrow.ROOM_SIZE
                
                # already in its optimal room and there are no wrong amphipod types in the room: no need to move
                if room == t and all(c is None or c == room for c in self.rooms[room]):
                    #print(f"      skipping: optimal room and no wrong in room")
                    continue
                
                # if it's blocked in any cell going towards the corridor, then skip
                if any(c is not None for c in self.rooms[room][roomPlace+1:]):
                    #print(f"      skipping: blocked")
                    continue
                
                # it's in the wrong room or this room also has a wrong amphipod type: to the corridor
                
                corridorCell = self.ROOM_TO_CORRIDOR[room]
                if corridorCell not in visited and self.corridor[corridorCell - Burrow.ROOM_PLACES] is None:
                    extraDist = Burrow.ROOM_SIZE - roomPlace
                    toDo.append((dist + extraDist, corridorCell))
                    #print(f"      adding: dist = {dist + extraDist}, pos = {corridorCell} | leaving room for corridor")
            
            # pos is in the corridor
            else:
                #print(f"    in corridor")
                corridorIndex = pos - Burrow.ROOM_PLACES
                # move left in the corridor
                if corridorIndex > 0:
                    if (pos-1) not in visited and self.corridor[corridorIndex - 1] is None:
                        #print(f"      adding: dist = {dist + 1}, pos = {pos - 1} | moving left in corridor")
                        toDo.append((dist + 1, pos - 1))
                
                # move right in the corridor
                if corridorIndex < Burrow.CORRIDOR_SIZE - 1:
                    if (pos+1) not in visited and self.corridor[corridorIndex + 1] is None:
                        #print(f"      adding: dist = {dist + 1}, pos = {pos + 1} | moving right in corridor")
                        toDo.append((dist + 1, pos + 1))
                
                # move to a room available
                if pos in self.CORRIDOR_TO_ROOM:
                    room = self.CORRIDOR_TO_ROOM[pos]
                    roomCell = room * Burrow.ROOM_SIZE + (Burrow.ROOM_SIZE - 1)
                    
                    # wrong room or the room contains at least a wrong amphipod: don't enter
                    if room != t or any(c is not None and c != room for c in self.rooms[room]):
                        #print(f"      skipping: wrong room or at least a wrong amphipod")
                        continue
                    
                    # right room and it contains no wrong amphipods 
                    # first index of an empty spot
                    roomCell = self.rooms[room].index(None)
                    newPos = (room * Burrow.ROOM_SIZE + roomCell)
                    if newPos not in visited:
                        extraDist = Burrow.ROOM_SIZE - roomCell
                        toDo.append((dist + extraDist, newPos))
                        #print(f"      adding: dist = {dist + extraDist}, pos = {newPos} | moving down in the room")
        
        # start with the biggest leaps
        return sorted(out, key = lambda x: x[1], reverse = True)
    
    
    def printStatus(self):
        out = []
        
        s = []
        
        s.append("#" * (len(self.corridor) + 2))
        
        corridor = "".join(AMPHIPODS[i] if i is not None else "." for i in self.corridor)
        
        s.append("#" + corridor + "#")
        
        overHang = (len(self.corridor) - (2*len(self.rooms) - 1)) // 2
        
        
        lines = [[]] * len(self.rooms)
        first = True
        for l in reversed(range(0, Burrow.ROOM_SIZE)):
            line = ("#" if first else " ") * overHang
            for r,room in enumerate(self.rooms):
                line += "#"
                line += AMPHIPODS[room[l]] if room[l] is not None else "."
            line += "#" + ("#" if first else " ") * (overHang)
            s.append(line)
            
            first = False
        
        s.append(" " * overHang + "#" * (len(self.rooms) * 2 + 1) + " " * overHang)
        
        length = len(self.corridor) + 2
        
        if len(out) == 0:
            out = [""] * len(s)
        
        for i,line in enumerate(s):
            out[i] += line.ljust(10, " ")
        print("\n".join(out))





def findLeastEnergy(startingBurrow):
    energyDist = {}
    prev = {}
    
    _,startingStatus = startingBurrow.toEnergyAndTuple()
    
    energyDist[startingStatus] = 0
    prev[startingStatus] = None
    
    visited = set()
    unvisitedHeap = [(energyDist[startingStatus], startingStatus)]
    
    while len(unvisitedHeap) > 0:
        nodeEnergy, status = heapq.heappop(unvisitedHeap)
        #print("\nStepping: ")
        #print(f"  extracted status {status}, with energy = {nodeEnergy}")
        print(f"energy: {nodeEnergy}, len: {len(unvisitedHeap)}")
        #print(f"Status selected at energy {nodeEnergy}: {status}, {len(unvisitedHeap)} remaining")
        #toPrint = [status]
        #if status in prev:
            #toPrint.append(prev[status])
        #printStatus(toPrint, amphipods)
        #print()
        
        # if we find that a node has a better distance, we don't remove its entry from the heap, we
        # just add a new one to its left in the heap: the later one will then be ignored
        if status in visited:
            continue
        
        visited.add(status)
        
        burrow = Burrow.fromTuple(status, nodeEnergy)
        # end: every other remaining status has a bigger nodeEnergy value
        if burrow.isFinished():
            sequence = [status]
            while prev[sequence[-1]] is not None:
                sequence.append(prev[sequence[-1]])
            
            print(f"reached end")
            return nodeEnergy, sequence[::-1]
        
        
        
        moveBurrows = burrow.getEveryMove()
        
        
        for moveb in moveBurrows:
            moveEnergy, moveStatus = moveb.toEnergyAndTuple()
            
            # visited means it was selected as the node with lowest energy, so another path will necessarily be worse
            if moveStatus in visited:
                continue
            
            if moveStatus not in energyDist or moveEnergy < energyDist[moveStatus]:
                energyDist[moveStatus] = moveEnergy
                prev[moveStatus] = status
                heapq.heappush(unvisitedHeap, (moveEnergy, moveStatus))
                #print(f"     -> Added status at energy {newEnergy}: {newStatus}")

        
    return None













with open(FILE_NAME) as file:
    
    data = [line.strip() for line in file]

Burrow.recalculateConstants()

#print(Burrow.CORRIDOR_TO_ROOM)
#exit()

rooms = list(reduce(lambda a,b: a+b, zip(*([c for c in l if c != "#"] for l in reversed(data[2:2+Burrow.ROOM_SIZE])))))

positions = [[] for _ in AMPHIPODS]

for i,amph in enumerate(rooms):
    positions[ord(amph) - ord("A")].append(i)
positions = [tuple(t) for t in positions]



burrow = Burrow(positions)
burrow.printStatus()


out = findLeastEnergy(burrow)

if out is None:
    print(f"Problema, non si è arrivati in fondo")
    exit()

energy, sequence = out
for status in sequence:
    sburrow = Burrow.fromTuple(status)
    sburrow.printStatus()
    print()

print("Part One: What is the least energy required to organize the amphipods?")
print(energy)
exit()






# part 2



extraRows = ["#D#C#B#A#", "#D#B#A#C#"]
rooms = list(reduce(lambda a,b: a+b, zip(*([c for c in l if c != "#"] for l in reversed((data[2], *extraRows, data[3]))))))

positions = [[] for _ in AMPHIPODS]

for i,amph in enumerate(rooms):
    positions[ord(amph) - ord("A")].append(i)
positions = [tuple(t) for t in positions]



Burrow.ROOM_SIZE = 4
Burrow.recalculateConstants()


burrow2 = Burrow(positions)
burrow2.printStatus()

out = findLeastEnergy(burrow2)

if out is None:
    print("we did not get to the end")
    exit()
    
energy, sequence = out

for status in sequence:
    sburrow = Burrow.fromTuple(status)
    sburrow.printStatus()
    print()


print()
print("Part Two: Using the initial configuration from the full diagram, what is the least energy required to organize the amphipods?")
print(energy)
