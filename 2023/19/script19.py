FILE_NAME = "example"
FILE_NAME = "input"


import math


workflows = {}
parts = []
with open(FILE_NAME) as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        
        # parts
        if line[0] == "{":
            parts.append(dict(tuple(v if i == 0 else int(v) for i,v in enumerate(e.split("="))) for e in line[1:-1].split(",")))
            continue
        
        # workflows
        name,values = line[:-1].split("{")
        
        workflows[name] = []
        
        for checkstr in values.split(","):
            # final
            if ":" not in checkstr:
                workflows[name].append(checkstr)
                continue
                
            check,dest = checkstr.split(":")
            if "<" in check:
                var,num = check.split("<")
                workflows[name].append(("<", var, int(num), dest))
            elif ">" in check:
                var,num = check.split(">")
                workflows[name].append((">", var, int(num), dest))
            else:
                raise Exception()
            
        
#print(workflows)
#print(parts)

def check(part, workflows, wid):
    if wid == "A":
        return True
    if wid == "R":
        return False
    
    for tup in workflows[wid]:
        # actual check
        if isinstance(tup, tuple):
            #print(tup)
            typ, var, num, dest = tup
            if (typ == "<" and (part[var] < num)) or (typ == ">" and (part[var] > num)):
                return check(part, workflows, dest)
        # resulting string
        else:
            return check(part, workflows, tup)



print("Part One:")
print(sum(sum(part.values()) for part in parts if check(part, workflows, "in")))


def checkRange(part, workflows, wid):
    if wid == "A":
        return math.prod(b - a + 1 for a,b in part.values())
    if wid == "R":
        return 0
    
    part = part.copy()
    
    out = 0
    for tup in workflows[wid]:
        # actual check
        if isinstance(tup, tuple):
            #print(tup)
            typ, var, num, dest = tup
            if typ == "<":
                l,h = part[var]
                
                # num --- (l --- h): the range (l -> h) goes to the next wf
                if num <= l:
                    pass
                # (l --- num --- h): 
                #  * the range (l -> num-1) goes to dest
                #  * the range (num -> h) goes to the next wf
                elif l < num <= h:
                    newPart = part.copy()
                    newPart[var] = (l, num-1)
                    out += checkRange(newPart, workflows, dest)
                    
                    part[var] = (num, h)
                # (l --- h) --- num: the entire range (l -> h) goes to dest
                else: # num > h
                    out += checkRange(part, workflows, dest)
                    # nothing left for the next workflow
                    break
                
                # the remaining part goes the the next workflow
                    
            else: # typ == ">"
                l,h = part[var]
                
                # num --- (l --- h): the range (l -> h) goes to dest
                if num < l:
                    out += checkRange(part, workflows, dest)
                    # nothing left for the next workflow
                    break
                # (l --- num --- h): 
                #  * the range (l -> num) goes to the next wf
                #  * the range (num+1 -> h) goes to dest
                elif l <= num < h:
                    newPart = part.copy()
                    newPart[var] = (num+1, h)
                    out += checkRange(newPart, workflows, dest)
                    
                    part[var] = (l, num)
                # (l --- h) --- num: the entire range (l -> h) goes to dest
                else: # num >= h
                    pass
                
                # the remaining part goes the the next workflow


        # resulting string
        else:
            out += checkRange(part, workflows, tup)
    
    return out
print()
print("Part Two:")
print(checkRange({k: (1,4000) for k in "xmas"}, workflows, "in"))
