FILE_NAME = "example"
FILE_NAME = "input"

import json
import functools
from functools import reduce

def to_tuple(lst):
    return tuple(to_tuple(i) if isinstance(i, list) else i for i in lst)

def incompare(l,r):
    ll = isinstance(l, tuple)
    rl = isinstance(r, tuple) 
    if ll and rl:
        for el,er in zip(l,r):
            c = incompare(el,er)
            
            if c != 0:
                return c
        
        # equal, but the left side ran out first -> right order
        if len(l) < len(r):
            return 1
        # same, but the right side ran out first -> wrong order
        elif len(l) > len(r):
            return -1
        
        # equal
        return 0
    
    # only one is a list -> convert the other to a list
    if ll or rl:
        if ll:
            r = (r,)
        elif rl:
            l = (l,)
        
        return incompare(l,r)
    
    # both numbers
    return r - l

def compare(l,r):
    #print(f"comparing {l=} and {r=}")
    c = incompare(l,r)
    
    if c == 0:
        raise Exception(f"{l=} and {r=} are equal")
    
    return c > 0


DIVIDER_PACKETS = [to_tuple(t) for t in [ [[2]], [[6]] ]]

with open(FILE_NAME) as file:
    lst = [to_tuple(json.loads(line.strip())) for line in file if len(line.strip()) > 0]
    
    s = 0
    for i in range(0, len(lst), 2):
        l,r = lst[i:i+2]
        if compare(l,r):
            s += (i//2)+1
        else:
            pass

    
    print("Part One: Determine which pairs of packets are already in the right order. What is the sum of the indices of those pairs?")
    print(s)


    lst.extend(DIVIDER_PACKETS)
    
    lst.sort(key=functools.cmp_to_key(incompare), reverse=True)
    
    
    print()
    print("Part Two: Organize all of the packets into the correct order. What is the decoder key for the distress signal?")
    print((lst.index(DIVIDER_PACKETS[0]) + 1) * (lst.index(DIVIDER_PACKETS[1]) + 1))
