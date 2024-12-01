from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"

STEPS1 = 10
#STEPS1 = 4

STEPS2 = 40


with open(FILE_NAME) as file:
    
    num1 = None
    
    data = [line[:-1] for line in file]
    
    polymer = data[0]
    couples = ["".join(polymer[i-1:i+1]) for i in range(1,len(polymer))]
    
    couplesDict = {k: sum(1 for c in couples if c == k) for k in set(couples)}
    
    rules = [ruleStr.split(" -> ") for ruleStr in data[2:]]
    ruleDict = {k:v for k,v in rules}
    
    allLetters = sorted(set(ruleDict.values()))
    
    elementAmount = {l: sum(1 for p1 in polymer if p1 == l) for l in allLetters}
    
    for n in range(STEPS2):
        newCouplesDict = couplesDict.copy()
        
        for couple,count in couplesDict.items():
            insert = ruleDict[couple]
            
            if insert not in elementAmount:
                elementAmount[insert] = 0
            elementAmount[insert] += count
            
            # remove the "count" amount of "couple"
            newCouplesDict[couple] -= count
            
            
            # insert a "count" amount for each new couple
            for nc in [couple[0] + insert, insert + couple[1]]:
                if nc not in newCouplesDict:
                    newCouplesDict[nc] = 0
                    
                newCouplesDict[nc] += count
            
        couplesDict = newCouplesDict
        
        
        if n+1 == STEPS1:
            sortedElems = list(sorted(elementAmount.values(), reverse=True))
            num1 = sortedElems[0] - sortedElems[-1]
            
    
    print("Part One: What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?")
    print(num1)
    
    print()
    print("Part Two: What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?")
    sortedElems = list(sorted(elementAmount.values(), reverse=True))
    print(sortedElems[0] - sortedElems[-1])
    

    
    
