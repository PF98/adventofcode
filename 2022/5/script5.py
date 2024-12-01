FILE_NAME = "example"
FILE_NAME = "input"

from itertools import groupby
import re
import copy

def printStack(stack):
    maxLen = max(len(s) for s in stack)
    
    for i in range(maxLen):
        
        letters = (stack[j][maxLen - 1 - i] if maxLen - 1 - i < len(stack[j]) else " " for j in range(len(stack)))
        print(" ".join(f"[{l}]" if l != " " else " "*3 for l in letters))
    
    print(" ".join(f"{n+1:^3d}" for n in range(len(stack))))
    print("-".join("-"*3 for n in range(len(stack))))
    print()
    
def solve(stack, instr, part):
    stack = copy.deepcopy(stack)
    for inst in instr:
        #input(f" > {inst}")
        m = re.match("move (\d+) from (\d+) to (\d+)", inst)
        
        num, fr, to = (int(m[n+1]) for n in range(3))
        
        match (part):
            case 1:
                stack[to-1].extend(stack[fr-1][-1:-num-1:-1])
            case 2:
                stack[to-1].extend(stack[fr-1][-num:])

        stack[fr-1] = stack[fr-1][:-num]
        
        #printStack(stack)
        
    return "".join(s[-1] for s in stack);

with open(FILE_NAME) as file:
    lst = [line[:-1] for line in file]
    
    stackLst, instr = [list(g) for k,g in groupby(lst, key=lambda x: len(x) > 0) if k]
    
    
    stackLen = (len(stackLst[-1])+1)//4;
    
    stack = [[] for _ in range(stackLen)]
    
    for s in stackLst[-2::-1]:
        letters = [s[i + 1] for i in range(0, len(s), 4)]

        for i,l in enumerate(letters):
            if l == " ":
                continue
            
            stack[i].append(l)
    
    #printStack(stack)


    r1 = solve(copy.deepcopy(stack), instr, 1)
    
    print("Part One: After the rearrangement procedure completes, what crate ends up on top of each stack?")
    print(r1)
    
    r2 = solve(copy.deepcopy(stack), instr, 2)
    print()
    print("Part Two: After the rearrangement procedure completes, what crate ends up on top of each stack?")
    print(r2)
