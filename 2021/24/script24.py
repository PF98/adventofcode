from functools import reduce
import re
import math
#from collections import defaultdict

class mem_dict(dict):
    DEFAULT_UPDATE = lambda w,z: [("w", w), ("x", 0), ("y", 0), ("z", z)]
    def __missing__(self, key):
        return int(key)
    
    def defaultfill(self, w, z):
        self.update(mem_dict.DEFAULT_UPDATE(w, z))
        
    

FILE_NAME = "example"
FILE_NAME = "input"


FUNCTION_MAP = {
    "add": lambda m, a, b: m.update([(a, m[a] + m[b])]),
    "mul": lambda m, a, b: m.update([(a, m[a] * m[b])]),
    "div": lambda m, a, b: m.update([(a, int(m[a] / m[b]))]), # truncating towards zero
    "mod": lambda m, a, b: m.update([(a, m[a] % m[b])]),
    "eql": lambda m, a, b: m.update([(a, 1 if m[a] == m[b] else 0)])
}


def runBlock(memory, block):
    for instruction in block:
        keyword, a, b = instruction.split(" ")
        func = FUNCTION_MAP[keyword]

        func(memory, a, b)
    
    return memory["z"]


class mem_z_dict(dict):
    def __setitem__(self, key, value):
        if key in self:
            #value = max(value, self[key]) # part 1
            minv, maxv = self[key]
            value = (min(value, minv), max(value, maxv)) # part 2
        else:
            value = (value, value)
        super().__setitem__(key, value)
    
    def __eq__(self, other):
        if len(self) != len(other):
            return False
        
        for key in self:
            if key not in other:
                return False
            
            if self[key] != other[key]:
                return False
            
        # all keys match and there is the same number of keys
        return True

STOP = 10

def applyBlockTuples(blockTuples):
    
    # maps the value of z to the biggest partial number to get there
    old_mem_z = mem_z_dict()
    old_mem_z[0] = 0
    
    for i, (div26, num6, num16) in enumerate(blockTuples):
        # need to integer divide every z by 26
        #if div26:
            #n_mem_z = mem_z_dict()
            #for z,num in mem_z[i].items():
                #n_mem_z[int(z / 26)] = num
            #mem_z[i] = n_mem_z
        
        
        mem_z = mem_z_dict()
        
        for w in range(1,10):
            for z, nums in old_mem_z.items():
                newNums = tuple(num * 10 + w for num in nums)
                old_z = z
                
                if div26:
                    z = int(z / 26)
                
                if (old_z % 26 + num6 != w):
                    # original: runs in 3 minutes
                    #out_z = z * 26 + w + num16
                    
                    # better (with help from solutions on the subreddit):
                    # if not div26, then z cannot decrease
                    # else we must choose the only option that allows z to significantly decrease: the other one
                    out_z = z * 26 + w + num16 if not div26 else None
                else:
                    out_z = z
                    
                if out_z is not None:
                    mem_z[out_z] = newNums[0]
                    mem_z[out_z] = newNums[1]
        
        old_mem_z = mem_z
        
        #print(i+1)
        #print(len(mem_z))
        #print()

        #if i >= STOP-1:
            #return mem_z
    return mem_z
        
def applyBlocks(blocks):
    mem_z = [mem_z_dict()] # starts with z = 0 with code 0
    mem_z[0][0] = 0
    
    
    for i,block in enumerate(blocks):
        memory = mem_dict()
        
        mem_z.append(mem_z_dict())
        
        for z,num in mem_z[i].items():
            for w in range(1,10):
                memory.defaultfill(w, z)
                new_z = runBlock(memory, block)
                mem_z[i+1][new_z] = num * 10 + w
        
        
        print()
        print(i+1)
        print(len(mem_z[i+1]))
        if i >= STOP-1:
            return mem_z




# notes on the data:
# - there are 14 "inp w" instruction, one for each digit of the model number, each beginning what i'll call a "block" of code
# - immediately after each "inp w", there is always a "mul x 0" instruction, which effectively renders the value of x after
#   each block pointless, since it will be reset to 0 before being used in the following block
# - next up are a series of 6 instruction which only update x (which starts at 0) and z (which holds the old value)
# - then comes "mul y 0", which once again renders the value of y in the previous block pointless => reset to zero
# - therefore after each block only the value of z needs to be memorized, since w, x and y all get overwritten before being
#   used


#SKIPPED = [0, 1, 4, 8]


with open(FILE_NAME) as file:
    data = [line.strip() for line in file]


blockStarts = [i for i,line in enumerate(data) if line == "inp w"] + [len(data)]

blocks = [data[s:e] for s,e in zip(blockStarts[:-1], blockStarts[1:])]

#out = [""] * len(blocks[0])
#print(out)
#W = 13
#for b in blocks:
    #for i,instr in enumerate(b):
        #out[i] += instr.ljust(W)
        
#for i in range(len(out)):
    #out[i] = f"{i+1:2d}. " + out[i]
    
    #if len(set(b[i] for b in blocks)) == 1:
        #out[i] += "all equal"
    #else:
        #out[i] += "!!! DIFFERENT !!!"
#out.insert(0, "    " + "".join(f"{i+1:02d} ".ljust(W, " ") for i in range(len(blocks))))
#for o in out:
    #print(o)
    
blockTuples = []
for block in blocks:
    div26 = (block[4] == "div z 26")
    num6 = int(block[5].split(" ")[-1])
    num16 = int(block[15].split(" ")[-1])
    
    blockTuples.append((div26, num6, num16))
    



mem_z = applyBlockTuples(blockTuples)

print("Part One: What is the largest model number accepted by MONAD?")
print(mem_z[0][1])

print()
print("Part Two: What is the smallest model number accepted by MONAD?")
print(mem_z[0][0])
