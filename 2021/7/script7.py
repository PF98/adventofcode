from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"


with open(FILE_NAME) as file:
    data = [int(n) for n in file.readline().split(",")]
    
    minFuel1 = None
    minFuel2 = None
    for i in range(min(data), max(data) + 1):
        fuel1 = sum([abs(d - i) for d in data])
        
        if minFuel1 is None or fuel1 < minFuel1:
            minFuel1 = fuel1
            
            
        fuel2 = sum([(abs(d-i) * (abs(d-i) + 1)) // 2 for d in data])
        
        if minFuel2 is None or fuel2 < minFuel2:
            minFuel2 = fuel2
    
    
    
    print("Part One: How much fuel must they spend to align to that position?")
    print(minFuel1)
    
    
    print()
    print("Part Two: How much fuel must they spend to align to that position?")
    print(minFuel2)
    

    
    
