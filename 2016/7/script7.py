from functools import reduce
from collections import Counter
import hashlib

FILE_NAME = "example"
FILE_NAME = "input"



with open(FILE_NAME) as file:
    data = [line.strip() for line in file]



cnt = 0
cnt2 = 0
for line in data:
    inParenthesis = False
    ok = False
    err = False
    
    ok2 = False
    
    inps, outps = list(zip(*(s.split("[") for s in (line + "[").split("]"))))
    #print(inps)
    #print(outps)
    #print()
    for outp in outps:
        for i,ch in enumerate(outp[:-3]):
            if ch != outp[i+1] and outp[i:i+2] == outp[i+3:i+1:-1]:
                #print(outp[i:i+4])
                err = True
                ok = False
            
        if err:
            break
    #print("outp done")
    
    BABs = set()
    
    for inp in inps:
        for i,ch in enumerate(inp):
            if not err and i < len(inp) - 3 and ch != inp[i+1] and inp[i:i+2] == inp[i+3:i+1:-1]:
                ok = True
                #break
                
            if i < len(inp) - 2 and ch != inp[i+1] and ch == inp[i+2]:
                BABs.add(f"{inp[i+1]}{ch}{inp[i+1]}")
    
    
    if ok:
        cnt += 1
    
    
    #print()
    #print(line)
    #print(BABs)
    for outp in outps:
        for i,_ in enumerate(outp[:-2]):
            if outp[i:i+3] in BABs:
                cnt2 += 1
                #print(line)
                break
        


print("Part One: How many IPs in your puzzle input support TLS?")
print(cnt)



print()
print("Part Two: How many IPs in your puzzle input support SSL?")
print(cnt2)
