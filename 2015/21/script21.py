from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"

# cost, damage, armor
WEAPONS = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0)
]

ARMOR = [
    (0, 0, 0), # no armor
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5)
]

RINGS = [
    (0, 0, 0), # only one ring in combination with the others
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3)
]

HEALTH = 100


def calcWinner(boss, you):
    b_hp, b_atk, b_arm = boss
    y_hp, y_atk, y_arm = you
    
    
    
    b_time = math.ceil(b_hp / max(y_atk - b_arm, 1))
    y_time = math.ceil(y_hp / max(b_atk - y_arm, 1))
    
    #return (b_time, y_time)
    return y_time >= b_time

def sumStats(*args):
    return tuple(sum(stats) for stats in zip(*args))

with open(FILE_NAME) as file:
    # hp, atk, arm
    boss = tuple(int(line.strip().split(": ")[1]) for line in file)
    minCost = None
    maxCost = None
    
    for weapon in WEAPONS:
        #print(f"weapon: {weapon}")
        for armor in ARMOR:
            #print(f"armor: {armor}")
            for r1,r2 in ((x,y) for ix,x in enumerate(RINGS) for iy,y in enumerate(RINGS) if ix < iy or ix == 0):
                #print(f"rings: {r1} and {r2}")
                cost, atk, arm = sumStats(weapon, armor, r1, r2)
                if calcWinner(boss = boss, you = (HEALTH, atk, arm)):
                    if minCost is None or cost < minCost:
                        minCost = cost
                else:
                    if maxCost is None or cost > maxCost:
                        maxCost = cost
                    
                
    
            
    print("Part One: You have 100 hit points. The boss's actual stats are in your puzzle input. What is the least amount of gold you can spend and still win the fight?")
    print(minCost)
    
    print()
    print("Part Two: What is the most amount of gold you can spend and still lose the fight?")
    print(maxCost)
