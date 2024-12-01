from functools import reduce
import re
import random
from enum import Enum
import heapq

FILE_NAME = "example"
FILE_NAME = "input"



with open(FILE_NAME) as file:
    
    data = [line.strip() for line in file]
        
    print("Part One: what is the number of characters of code for string literals minus the number of characters in memory for the values of the strings in total for the entire file?")
    print(sum(len(s) - len(eval(s)) for s in data))
    
    
    
    
    
    
    print()
    print("Part Two: find the total number of characters to represent the newly encoded strings minus the number of characters of code in each original string literal")
    print(sum(2 + sum(1 for ch in s if ch == '"' or ch == '\\') for s in data))
    
