FILE_NAME = "example"
FILE_NAME = "input"

import re
import heapq
from dataclasses import dataclass
import itertools

START = "AA"
MAXTIME = 30
ELEPHANT_TIME = 4

class Valve:
    def __init__(self, name, flow, tunnels):
        self.name = name
        self.flow = flow
        self.tunnels = tunnels
        self.distances = {}
        
    def findAllDistances(self, valveNames, valves):
        nodes = []
        nodes.append(self.name)
        dist = 0
        
        while nodes:
            alltunnels = set(t for t in itertools.chain(*(valves[vn].tunnels for vn in nodes)) if t not in self.distances)
            dist += 1
            for t in alltunnels:
                self.distances[t] = dist
            nodes = alltunnels
        
        self.distances = {k:v for k,v in self.distances.items() if valves[k].flow > 0 and k != self.name}
        
        #print(f"{self.name=}, {self.distances=}")

@dataclass
class Status:
    time: int
    position: str
    openValves: dict[str]
    currentPressure: int
    def __init__(self, time, position, openValves):
        self.time = time
        self.position = position
        self.openValves = openValves.copy()
        
        self.currentPressure = 0
        
    def openValve(self):
        self.openValves[self.position] = self.time
    
    def calcPressure(self):
        self.currentPressure = sum(Status.valves[vn].flow * (self.time - self.openValves[vn]) for vn in self.openValves)
    
    def getProjectedPressure(self, maxTime):
        return self.currentPressure + sum(Status.valves[vn].flow for vn in self.openValves) * (maxTime - self.time)
    
    def projectTo(self, maxTime):
        s = Status(
            maxTime,
            self.position,
            self.openValves
        )
        s.calcPressure()
        return s
    
    def __lt__(self, other):
        return self.currentPressure > other.currentPressure
    
    def __eq__(self, other):
        return self.currentPressure == other.currentPressure



def findMax(valveNames, valves, maxTime):
    statusheap = [Status(0, START, {})]
    
    nextTimeStatuses = []
    
    allBestPaths = {}
    
    bestResult = None
    while statusheap:
        #print()
        #print("="*100, end="")
        #print(statusheap)
        #print("visited:")
        #print("\n".join("".join("." if v else "x" for v in r) for r in unvisited))
        
        maxStatus = heapq.heappop(statusheap)
        #print("\nStepping: ")
        #print(f"extracted status {maxStatus}, with current pressure = {maxStatus.currentPressure} at time {maxStatus.time}")
        #print(f"  {len(statusheap)=}, {maxStatus.time=}, {maxTime}", end="\r")
        
        projected = maxStatus.getProjectedPressure(maxTime)
        t = tuple(sorted(maxStatus.openValves))
        if t not in allBestPaths or allBestPaths[t] < projected:
            allBestPaths[t] = projected
        if bestResult is None or projected > bestResult.currentPressure:
            bestResult = maxStatus.projectTo(maxTime)
            #print(f"  -> found new best result{bestResult=}")
        
        
        if maxStatus.time == maxTime:
            continue
        
        
        newStatus = None
        
        # if we visit a node, then it must be opened, since it would be a waste to visit
        # it and not open it (unless it's the starting node)
        if valves[maxStatus.position].flow > 0:
            newStatus = Status(
                maxStatus.time + 1,
                maxStatus.position,
                maxStatus.openValves
            )
            newStatus.calcPressure()
            newStatus.openValve()
            
            projected = newStatus.getProjectedPressure(maxTime)
            t = tuple(sorted(newStatus.openValves))
            if t not in allBestPaths or allBestPaths[t] < projected:
                allBestPaths[t] = projected
            if bestResult is None or projected > bestResult.currentPressure:
                bestResult = newStatus.projectTo(maxTime)
                #print(f"  -> found new best result{bestResult=}")
        else:
            newStatus = maxStatus
        
        
        # try travelling to other nodes
        for dest,dist in valves[newStatus.position].distances.items():
            if dest in newStatus.openValves:
                continue
            
            # travelling there takes too long
            if newStatus.time + dist >= maxTime:
                continue
            
            travelStatus = Status(
                newStatus.time + dist,
                dest,
                newStatus.openValves
            )
            travelStatus.calcPressure()
            #print(f"  -> added {newStatus=}")
            heapq.heappush(statusheap, travelStatus)

        
    return bestResult, allBestPaths


def findMax2(maxTime):
    openedValves = []
    print(maxTime)
    # format: you, eleph (both t,pos), opened valves (dict of name -> time)
    statusi = [([(0, START), (0, START)], {})]

    maxPressure = None
    cnt = 0
    while statusi:
        cnt += 1
        if cnt % 30000 == 0:
            print(f"{len(statusi)=}", end="\r")
            
        people, opened = statusi.pop()
        #print(f"extracted {people=}, {opened=}")
        t,p = list(zip(*people))
        
        options = [[], []]
        # always sorted so that the first in people is the one with the lowest time
        #print(f"   dist1: {Status.valves[p[0]].distances.items()}")
        #print(f"   dist2: {Status.valves[p[1]].distances.items()}")
        
        for dest1, dist1 in Status.valves[p[0]].distances.items():
            if dest1 in opened:
                continue
            
            if t[0] + dist1 >= maxTime:
                continue
            
            for dest2, dist2 in Status.valves[p[1]].distances.items():
                if dest2 == dest1 or dest2 in opened:
                    continue
            
                if t[1] + dist2 >= maxTime:
                    continue
                
                newOpened = opened.copy()
                newOpened[dest1] = t[0] + dist1 + 1
                newOpened[dest2] = t[1] + dist2 + 1
                
                newStatus = (
                    list(sorted([(t[0] + dist1 + 1, dest1), (t[1] + dist2 + 1, dest2)])),
                    newOpened
                )
                
                newPressure = sum((maxTime - openTime) * Status.valves[vn].flow for vn,openTime in newOpened.items())
                #print(f"  ({newPressure=})")
                if maxPressure is None or newPressure > maxPressure:
                    maxPressure = newPressure
                    print(f"### Found new {maxPressure=} with {newOpened=}")
                
                #print(f" -> {newStatus=}")
                statusi.append(newStatus)
        
        #print("\n".join(str(s) for s in statusi))
        #print(f"{len(statusi)=}", end="\r\n")
        #input()

with open(FILE_NAME) as file:
    
    valves = {}
    valveNames = []
    for line in file:
        m = re.match("Valve ([A-Z]+) has flow rate=(\d+); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.+)", line.strip())
        
        name = m[1]
        flow = int(m[2])
        tunnels = m[3].split(", ")
    
        valves[name] = Valve(name, flow, tunnels)
        valveNames.append(name)

    Status.valves = valves
    Status.valveNames = valveNames
    
    
    Status.usefulValves = [v for v in valveNames if valves[v].flow > 0]
    #print(usefulValves)
    
    
    #print(valves)
    #print(valveNames)
    
    #valves["AA"].findAllDistances(valveNames, valves)
    #exit()
    for v in valves.values():
        v.findAllDistances(valveNames, valves)
    
    bestResult, _ = findMax(valveNames, valves, MAXTIME)
    
    print("Part One: Work out the steps to release the most pressure in 30 minutes. What is the most pressure you can release?")
    print(bestResult.currentPressure)
    
    
    #bestResult2 = findMax2(valveNames, valves, MAXTIME - ELEPHANT_TIME)
    #findMax2(MAXTIME - ELEPHANT_TIME)
    
    best, allBestPaths = findMax(valveNames, valves, MAXTIME - ELEPHANT_TIME)
    #print(best)
    
    #print(f"{len(allStatusi)=}")
    #print(f"{len(allBestPaths)=}")
    #print(max(allBestPaths.values()))
              
    maxP = None
    for i,(t1,p1) in enumerate(allBestPaths.items()):
        if i % 10 == 0:
            print(f" {i:4d}/{len(allBestPaths)}", end="\r")
        for t2,p2 in allBestPaths.items():
            if any(pos2 in t1 for pos2 in t2):
                continue
            
            # distinct:
            tot = p1 + p2
            #print(f"{s1=} and {s2=} distinct: total pressure: {s1.currentPressure} + {s2.currentPressure} = {tot}")
            
            if maxP is None or tot > maxP:
                maxP = tot
                #print("new max:", end="")
                #print(f" total pressure: {p1} + {p2} = {tot}")
            pass
    
    print(" "*30)
    print("Part Two: With you and an elephant working together for 26 minutes, what is the most pressure you could release?")
    print(maxP)
