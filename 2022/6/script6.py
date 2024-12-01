FILE_NAME = "example"
FILE_NAME = "input"

from itertools import groupby

Ls = [4,14]


with open(FILE_NAME) as file:
    lst = [line.strip() for line in file]
    
    first = True
    
    for line in lst:
        if first:
            first = False
        else:
            print("-" * len("Part Two: How many characters need to be processed before the first start-of-message marker is detected?"))
        founds = [None] * 2;
        lineLen = len(line)
        for i,l in enumerate(line):
            for j,L in enumerate(Ls):
                if founds[j] is None and i + L < lineLen and len(set(line[i:i+L])) == L:
                    founds[j] = i + L
                    
                    if all(f is not None for f in founds):
                        break
            else:
                #print(f"continuing at {i=}")
                continue
            #print(f"breaking at {i=}")
            break
        
        print("Part One: How many characters need to be processed before the first start-of-packet marker is detected?")
        print(founds[0])
        
        
        print()
        print("Part Two: How many characters need to be processed before the first start-of-message marker is detected?")
        print(founds[1])
    
    
