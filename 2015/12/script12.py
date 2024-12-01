from functools import reduce
import re
import math
import json

FILE_NAME = "example"
FILE_NAME = "input"


def mcount(data, is2 = False):
    if isinstance(data, list):
        #print("list")
        #print(data)
        return sum(mcount(d, is2) for d in data)
    elif isinstance(data, dict):
        #print("dict")
        #print(data)
        return sum(mcount(d, is2) for d in data.values()) if ((not is2) or ("red" not in data.values())) else 0
    elif isinstance(data, int):
        #print("number")
        #print(data)
        return data
    
    return 0


with open(FILE_NAME) as file:
    data = json.loads(file.readline().strip())
    
    
    
    print("Part One: What is the sum of all numbers in the document?")
    print(mcount(data))
    
    
    
        
    print()
    print("Part Two: Ignore any object (and all of its children) which has any property with the value \"red\". Do this only for objects ({...}), not arrays ([...]).")
    print(mcount(data, is2=True))
    
