FILE_NAME = "example"
FILE_NAME = "input"

import re
from dataclasses import dataclass

RESOURCES = ["ore", "clay", "obsidian", "geode"]

ROBOTS = [
    (0,),
    (0,),
    (0, 1),
    (0, 2),
]

MAXTIME = 24
MAXTIME2 = 32

@dataclass
class Status:
    time: int
    resources: tuple[int]
    robots: tuple[int]
    def __init__(self, time, resources, robots, maxTime):
        self.time = time
        self.resources = resources
        self.robots = robots
        self.maxTime = maxTime
        
        self.potential = tuple(res + rob * (maxTime - time) for res,rob in zip(resources, robots))
    
    def stepTime(self):
        self.time += 1
        self.resources = tuple(res + rob for res,rob in zip(self.resources, self.robots))
        
    def createRobot(self, index, costs):
        res = list(self.resources)
        for resind, rc in zip(ROBOTS[index], costs):
            res[resind] -= rc
        
        robots = list(self.robots)
        robots[index] += 1
            
        news = Status(self.time, tuple(res), tuple(robots), self.maxTime)
        return news
    
    
    
def findMax(robotcosts, maxTime, pruneamount):
    statuses = [Status(0, (0,)*len(ROBOTS), (1, *(0,)*(len(ROBOTS) - 1)), maxTime)]
    
    for t in range(maxTime):
        print(f"{t} {len(statuses) = }, best: {statuses[0]}", end="\r")
        #print(f"{len(statuses) = }, ({statuses})")
        #input()
        newStatues = []
        
        # generate new statues at time t+1
        for s in statuses:
            oldres = s.resources
            # steps time forward and mines the resources
            s.stepTime()
            
            # don't create anything
            newStatues.append(s)
            
            # create all possible combinations of robots
            for nameind, resind in reversed(list(enumerate(ROBOTS))):
                #print(f"{nameind=}, {resind=}, {oldres=}, {robotcosts[nameind]=}")
                if all(oldres[ri] >= req  for ri,req in zip(resind, robotcosts[nameind])):
                    news = s.createRobot(nameind, robotcosts[nameind])
                    
                    newStatues.append(news)
                #print(newStatues)
                #exit()
                    
        statuses = sorted(newStatues, key=lambda s: tuple(reversed(s.potential)), reverse=True)
        
        # arbitrary pruning of the state space
        statuses = statuses[:pruneamount]
            
    return statuses
    
with open(FILE_NAME) as file:
    
    allrobotcosts = []
    for line in file:
        bp, robotsstr = line.strip().split(": ")
        bpid = int(bp[10:])
        
        robots = robotsstr.split(". ")
        
        robotcosts = []
        
        for robotstr, (robind, reslist) in zip(robots, enumerate(ROBOTS)):
            res = ' and '.join(f'(\\d+) {RESOURCES[r]}' for r in reslist)
            
            m = re.match(f"Each {RESOURCES[robind]} robot costs {res}", robotstr)
            
            robotcosts.append(tuple(int(m[n+1]) for n in range(len(reslist))))
        
        allrobotcosts.append(robotcosts) 
    
    sumprod = 0
    
    for bpid,robotcosts in enumerate(allrobotcosts):
        #print(robotcosts)
        m = findMax(robotcosts, MAXTIME, 200)
        print(" "*100, end="\r")
        #print(f"Blueprint {bpid+1} -> {m[0].resources[-1]}")
        
        sumprod += (bpid+1) * m[0].resources[-1]
    
    
    #chunks = sorted(sum(int(n) for n in g) for k,g in groupby(lst, key=lambda x: len(x) > 0) if k)
    
    print("Part One: Determine the quality level of each blueprint using the largest number of geodes it could produce in 24 minutes. What do you get if you add up the quality level of all of the blueprints in your list?")
    print(sumprod)
    print()
    
    prod = 1
    
    # part 2: only the first 3 blueprints
    for robotcosts in allrobotcosts[:3]:
        m = findMax(robotcosts, MAXTIME2, 10000)
        print(" "*100, end="\r")
        print(f"Blueprint {bpid+1} -> {m[0].resources[-1]}")
        
        prod *= m[0].resources[-1]
    

    
    
    print()
    print("Part Two: Don't worry about quality levels; instead, just determine the largest number of geodes you could open using each of the first three blueprints. What do you get if you multiply these numbers together?")
    print(prod)
