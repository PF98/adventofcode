from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"

STEPS1 = 1
STEPS1 = 40

#STEPS2 = 10
STEPS2 = 50

with open(FILE_NAME) as file:
    data = file.readline().strip()
    #data = "1211"
    
    out1 = None
    
    for i in range(STEPS2):
        old = data
        
        # acc: (count, previous, list[(num, count)]
        # el: enumerate, so (index, element)
        data = []
        prev = None
        cnt = 0
        for j,ch in enumerate(old):
            if ch == prev or prev is None:
                cnt += 1
            else:
                data.append(str(cnt))
                data.append(prev)
                cnt = 1
            
            prev = ch
            
            if j == len(old) - 1:
                data.append(str(cnt))
                data.append(ch)
        
        
        
        #print(f"After step {i+1: 2}: {len(data)}")
        #print(f"After step {i: 2}: {data}")
        #print(f"After step {i: 2}: {max(len(d) for d in data)}")
        
        if i+1 == STEPS1:
            out1 = len(data)
        
        
        
    print("Part One: Starting with the digits in your puzzle input, apply this process 40 times. What is the length of the result?")
    print(out1)
    
    
    
        
    print()
    print("Part Two: Now, starting again with the digits in your puzzle input, apply this process 50 times. What is the length of the new result?")
    print(len(data))
    
    
