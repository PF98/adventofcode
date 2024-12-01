FILE_NAME = "example"
FILE_NAME = "input"

from functools import reduce
import itertools

with open(FILE_NAME) as file:
    lst = [line.strip() for line in file]
lst.append("")

# condizioni:
# m >= 0
# n - m >= 0
# m < l
# n - m < l
# 
# quindi 0 <= m < l
#        m <= n < m + l
# qundi in realtà 0 <= n < 2l
# e fissato n, allora n-l < m <= n
# quindi max(0, n-l+1) <= m < min(l, n-1)
def convolve(numbers):
    l = len(numbers)
    
    out = []
    for n in range(1, 2*l - 1, 2):
        #print(n, range(max(0, n-l+1), min(2*l, n)))
        conv = sum(abs(numbers[m] - numbers[n - m]) for m in range(max(0, n-l+1), min(l, n)))
        
        if conv == 0:
            out.append((n+1)//2)
    
    #print(numbers)
    
    return out



tot = 0

rows = []
cols = []
for row in lst:
    # 
    if not row:
        #print(rows, cols)
        
        # convolution
        rcs = convolve(rows)
        ccs = convolve(cols)
        
        if rcs:
            if len(rcs) == 1:
                tot += 100*rcs[0]
            else:
                print(f"{rcs = }")
                raise Exception()
        if ccs:
            if len(ccs) == 1:
                tot += ccs[0]
            else:
                print(f"{ccs = }")
                raise Exception()
            
        
        rows = []
        cols = []
        
        continue
    
    if not cols:
        cols = [0]*len(row)
    
    rows.append(reduce(lambda acc,c: 2*acc + (1 if c == "#" else 0), row, 0))
    
    for i,c in enumerate(row):
        cols[i] = 2*cols[i] + (1 if c == "#" else 0)
    
    
print("Part One:")
print(tot)
#exit()


# tries changing all of the nodes until a smudge is found

tot = 0

rows = []
cols = []
for row in lst:
    # 
    if not row:
        #print(rows, cols)
        rc = 0
        cc = 0
        
        rcs = convolve(rows)
        ccs = convolve(cols)
        
        if rcs:
            if len(rcs) == 1:
                rc, = rcs
            else:
                print(f"{rcs = }")
                raise Exception()
        if ccs:
            if len(ccs) == 1:
                cc, = ccs
            else:
                print(f"{ccs = }")
                raise Exception()
            
        
        
        
        for r in range(len(rows)):
            for c in range(len(cols)):
                # switch the first element
                rows[r] ^= (1 << (len(cols) - 1 - c))
                cols[c] ^= (1 << (len(rows) - 1 - r))
                
                rcns = convolve(rows)
                ccns = convolve(cols)
                
                if not rcns:
                    rcns.append(0)
                if not ccns:
                    ccns.append(0)
                
                found = False
                
                for rcn in rcns:
                    for ccn in ccns:
                        if (rcn > 0 or ccn > 0) and (rcn != rc or ccn != cc):
                            if rcn != rc:
                                tot += 100*rcn
                            else:
                                tot += ccn
                            #print(f"found smudge at {r = }, {c = }: {rcn = }, {ccn = } (from {rcns = }, {ccns = }) before it had {rc = }, {cc = }")
                            found = True
                if found: 
                    break
                
                # switch back
                rows[r] ^= (1 << (len(cols) - 1 - c))
                cols[c] ^= (1 << (len(rows) - 1 - r))
            else:
                continue
            break
        else:
            raise Exception()
                #input()
                
        # convolution
        #tot += 100 * convolve(rows)
        #tot += convolve(cols)
        
        
        rows = []
        cols = []
        
        continue
    
    if not cols:
        cols = [0]*len(row)
    
    rows.append(reduce(lambda acc,c: 2*acc + (1 if c == "#" else 0), row, 0))
    
    for i,c in enumerate(row):
        cols[i] = 2*cols[i] + (1 if c == "#" else 0)
    

print()
print("Part Two:")
print(tot)
