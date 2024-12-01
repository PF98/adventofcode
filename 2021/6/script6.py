from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

RESET_COUNT = 6
NEWBORN_COUNT = 8

DAYS1 = 18
DAYS1 = 80

DAYS2 = 256

with open(FILE_NAME) as file:
    data = [int(n) for n in file.readline().split(",")]
    
    countAmounts = [0] * (NEWBORN_COUNT + 1) # can be from 0 to 8
    
    for d in data:
        countAmounts[d] += 1
    
    len1 = 0
    
    #print(f"Initial state: {', '.join(f'{i}->{d}' for i,d in enumerate(countAmounts))}")
    for i in range(DAYS2):
        zeros = countAmounts[0]
        countAmounts = countAmounts[1:] + [zeros]
        countAmounts[RESET_COUNT] += zeros
        
        if i+1 == DAYS1:
            len1 = sum(countAmounts)
        #print(f"After {i+1:2d} day{'s:' if i > 0 else ': '} {', '.join(f'{i}->{d}' for i,d in enumerate(countAmounts))}")
        pass
    
    
    print("Part One: How many lanternfish would there be after 80 days?")
    print(len1)
    
    
    print()
    print("Part Two: How many lanternfish would there be after 256 days?")
    print(sum(countAmounts))
    

    
    
