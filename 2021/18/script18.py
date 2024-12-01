from functools import reduce
import re
import math
import json


FILE_NAME = "example1"
FILE_NAME = "example2"
FILE_NAME = "example3"
FILE_NAME = "example4"
FILE_NAME = "example5"
FILE_NAME = "example"
FILE_NAME = "input"


def dprint(*args):
    print(*args)
def dprint(*a):
    pass


WEIGHTS = [3,2]


class ExplodeAction:
    def __init__(self, num, value):
        self.left, self.right = num
        self.value = value
    
    def isFinished(self):
        return (self.left is None) and (self.right is None)
    
    def __str__(self):
        return f"ExplodeAction {{value = {self.value}, l-r: [{self.left}, {self.right}]}}"
    
    def __repr__(self):
        return self.__str__()

# returns updated, number
def snailreduce(res):
    done = False
    while not done:
        exploded = True
        while exploded:
            exploded, res = snailexplode(res)
        
        split, res = snailsplit(res)
        done = not split
        #print(res)
    return res
    

def snailsplit(num):
    #dprint(f"split")
    if not isinstance(num, list):
        # split
        if num >= 10:
            half = num // 2
            return True, [half, half if num % 2 == 0 else half + 1]
        
        return False, num
    
    out = []
    globalUpdated = False
    for sub in num:
        if not globalUpdated:
            updated, subnum = snailsplit(sub)
            globalUpdated = updated
            out.append(subnum)
        else:
            out.append(sub)
    
    return globalUpdated, out

    
def snailexplode(num, depth = 0):
    dprint(f"{'    ' * depth}explode with depth = {depth}, num = {num}")
    if not isinstance(num, list):
        return False, num
    # is list
    
    
    # explode
    if depth == 4:
        ret = True, ExplodeAction(num, 0)
        dprint(f"{'    ' * (depth)}<- returned {ret}")
        return ret
    
    
    
    out = []
    globalUpdated = False
    for sub in num:
        if not globalUpdated:
            updated, subnum = snailexplode(sub, depth + 1)
            if isinstance(subnum, ExplodeAction):
                dprint(f"{'    ' * (depth+1)}Explode!!! on {num} - {str(num).replace(str(sub), '####')}")
            
            out.append(subnum)
            globalUpdated = updated
        else:
            out.append(sub)
    
    
    
    lo, ro = out
    
    if isinstance(lo, ExplodeAction):
        if lo.right is not None:
            ro = increaseLeftmost(ro, lo.right)
            lo.right = None
        
        out = ExplodeAction((lo.left, None), [lo.value, ro])
    elif isinstance(ro, ExplodeAction):
        if ro.left is not None:
            lo = increaseRightmost(lo, ro.left)
            ro.left = None
    
        out = ExplodeAction((None, ro.right), [lo, ro.value])
    
    
    if isinstance(out, ExplodeAction):
        if depth == 0 or out.isFinished():
            out = out.value
    
    
    ret = globalUpdated, out
    dprint(f"{'    ' * (depth)}<- returned {ret}")
    
    
    
    
    
    return ret



def increaseRightmost(arr, val):
    dprint(f"CALLED RIGHTMOST ON arr = {arr}, val = {val}")
    
    if not isinstance(arr, list):
        return arr + val
    
    l,r = arr
    
    return [l, increaseRightmost(r, val)]

def increaseLeftmost(arr, val):
    dprint(f"CALLED LEFTMOST ON arr = {arr}, val = {val}")
    
    if not isinstance(arr, list):
        return arr + val
    
    l,r = arr
    
    return [increaseLeftmost(l, val), r]


def snailsum(a,b):
    res = [a, b]
    dprint(res)
    
    return snailreduce(res)

def snailmagnitude(num):
    if not isinstance(num, list):
        return num
    
    return sum(w*snailmagnitude(n) for w,n in zip(WEIGHTS, num))

with open(FILE_NAME) as file:
    
    result = None
    
    addends = []
    
    for line in file:
        obj = json.loads(line.strip())
        addends.append(obj)
        
        if result is None:
            result = obj
            continue
        
        
        #print(f"  {result}")
        #print(f"+ {obj}")
        result = snailsum(result, obj)
        #print(f"= {result}\n")
        #print("".join(c for c in str(result) if c != " "))
        #print("\n")
        #break
        
    
    print("Part One: What is the magnitude of the final sum?")
    print(result)
    
    print(snailmagnitude(result))

    
    
    print()
    print("Part Two: What is the largest magnitude of any sum of two different snailfish numbers from the homework assignment?")
    
    
    maxMag = None
    for i in range(len(addends)):
        print(i)
        for j in range(len(addends)):
            if i == j:
                continue
            
            result = snailsum(addends[i], addends[j])
            mag = snailmagnitude(result)
            if maxMag is None or mag > maxMag:
                maxMag = mag
            
    
    print(maxMag)
    
