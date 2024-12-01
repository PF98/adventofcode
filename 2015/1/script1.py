from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    
    data = file.readline().strip()
    
    print("Part One: To what floor do the instructions take Santa?")
    print(sum(1 if ch == "(" else -1 for ch in data))
    
    print()
    print("Part Two: What is the position of the character that causes Santa to first enter the basement?")
    print(reduce(lambda acc,diff : acc if acc[0] else (acc[1] + diff[0] < 0, acc[1]+diff[0], diff[1]), ((1 if ch == "(" else -1, i+1) for i,ch in enumerate(data)), (False, 0, None))[2])
