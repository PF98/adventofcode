from functools import reduce
import re
import math
from collections import defaultdict

FILE_NAME = "example"
FILE_NAME = "input"



def isPossibleGroups(weight, numbers, used = set()):
    if not weight in used and weight in numbers:
        return True
    
    for n in reversed(numbers):
        if n > weight:
            break
        if n in used:
            continue
        
        if isPossibleGroup(weight - n, numbers, set([*used, n])):
            return True
    return False

def getGroupsIter(weight, numbers):
    bestSequence = None
    bestLength = None
    bestQuantum = None
    
    indices = []
    
    indices.append(0)
    
    while True:
        numSum = sum(numbers[i] for i in indices)
        
        #sequence = tuple(numbers[i] for i in indices)
        #print(f"trying sequence [{', '.join(f'{n:2d}' for n in sequence)}] (sum = {numSum})")
        #print(f"        indices ({', '.join(f'{n:2d}' for n in indices)})")
        if numSum == weight:
            #print(f" -> found sequence {sequence} (indices = {indices})")
            
            length = len(indices)
            sequence = tuple(numbers[i] for i in indices)
            if not isPossibleGroup(weight, numbers, set(sequence)):
                pass
                #print(f" -> discarded sequence {sequence} (indices = {indices}), since it's not possible")
            else:
                quantum = reduce(lambda a,b: a*b, (numbers[i] for i in indices))
                best = False
                if bestLength is None or length < bestLength:
                    best = True
                elif length == bestLength:
                    best = (bestQuantum is None or quantum < bestQuantum)
                    
                if best:
                    bestSequence = sequence
                    bestLength = length
                    bestQuantum = quantum
                    #print(f" -> found best sequence {bestSequence} (indices = {indices}) [length = {bestLength}, Q = {bestQuantum}]")


        decreaseBack = False
        if numSum < weight:
            lastInd = indices[-1]
            if lastInd + 1 < len(numbers):
                # adding a new index would only make matters worse
                if bestLength is not None and len(indices) == bestLength:
                    # all adjacent (something like [7,6,5,4] - (7-4 == 4-1)): can quit because
                    # if the sum is not enough at this length, no other sequence with smaller indices
                    # and at most the same length can have a bigger sum
                    if indices[-1] - indices[0] == len(indices) - 1:
                        break
                    
                    indices.pop()
                    decreaseBack = True
                else:
                    indices.append(lastInd + 1)
            else:
                #break
                decreaseBack = True
        else:
            # either >= or ==
            decreaseBack = True
        
        if decreaseBack:
            # the last index can't be increased to decrease the value: remove it
            while len(indices) > 0 and (not (indices[-1] + 1 < len(numbers))):
                indices.pop() # remove the last
            
            if len(indices) == 0:
                break
            
            # the last index can now be increased
            indices[-1] += 1
            
        #input()
    return bestQuantum
            
            






with open(FILE_NAME) as file:
    numbers = list(sorted([int(line) for line in file], reverse = True))
    
    
weight = sum(numbers)

q = getGroupsIter(weight // 3, numbers)

print("Part One: What is the quantum entanglement of the first group of packages in the ideal configuration?")
print(q)



q = getGroupsIter(weight // 4, numbers)

print()
print("Part Two: Now, what is the quantum entanglement of the first group of packages in the ideal configuration?")
print(q)
