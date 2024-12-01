from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"


calcAfterTimes = [1000, 2503]
DIST = 1000
DIST = 2503

with open(FILE_NAME) as file:
    
    reindeers = []
    
    reindeersRes = []
    
    for line in file:
        m = re.match("([A-Za-z]+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.", line)
        
        name = m.group(1)
        speed,time,rest = (int(m.group(i)) for i in range(2,5))
        
        reindeers.append((speed, time, rest))
        
        r = []
        
        for totTime in calcAfterTimes:
            integerTimes = totTime // (time + rest)
            intTime = integerTimes * (time + rest)
            dist = (integerTimes * time + min(time, totTime - intTime)) * speed
            r.append(dist)
        
        reindeersRes.append(r)
    
    print("Part One: what distance has the winning reindeer traveled?")
    print(max(sum(d for i,d in enumerate(r) if calcAfterTimes[i] == DIST) for r in reindeersRes))
    
    times = [0] * len(reindeers)
    resting = [False] * len(reindeers)
    positions = [0] * len(reindeers)
    scores = [0] * len(reindeers)
    for n in range(DIST):
        for i,(speed,time,rest) in enumerate(reindeers):
            if not resting[i]:
                positions[i] += speed
                
            times[i] += 1
            
            if (not resting[i] and times[i] == time) or (resting[i] and times[i] == rest):
                times[i] = 0
                resting[i] = not resting[i]
        
        maxPos = max(positions)
        #print(f"{n}) {positions}")
        scores[:] = (s if positions[j] < maxPos else s+1 for j,s in enumerate(scores))
        
    
    print()
    print("Part Two: how many points does the winning reindeer have?")
    print(max(scores))
    
