from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    
    data = [tuple(int(n) for n in line.split("x")) for line in file]
    
    print("Part One:  How many total square feet of wrapping paper should they order?")
    print(sum(2*(l*w + w*h + h*l) + min(l*w, w*h, h*l) for l,w,h in data))
    
    print()
    print("Part Two: How many total feet of ribbon should they order?")
    print(sum(2 * sum(sorted([l,w,h])[:2]) + l*w*h for l,w,h in data))
