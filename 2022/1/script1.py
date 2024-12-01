FILE_NAME = "example"
FILE_NAME = "input"

from itertools import groupby

with open(FILE_NAME) as file:
    lst = [line.strip() for line in file]
    
    chunks = sorted(sum(int(n) for n in g) for k,g in groupby(lst, key=lambda x: len(x) > 0) if k)
    
    print("Part One: Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?")
    print(chunks[-1])
    
    print()
    print("Part Two: Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?")
    print(sum(chunks[-3:]))
