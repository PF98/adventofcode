from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

VOWELS = "aeiou"
FORBIDDEN = ["ab", "cd", "pq", "xy"]

with open(FILE_NAME) as file:
    
    data = [line.strip() for line in file]
    
    print("Part One: How many strings are nice?")
    print(
        sum(
            1 if 
                sum(1 for c in string if c in VOWELS) >= 3
            and
                reduce(lambda acc,c : acc if acc == True else (True if acc == c else c), string) == True
            and
                all(f not in string for f in FORBIDDEN)
            else 0 
            for string in data
        )
    )
    
    print()
    print("Part Two: How many strings are nice under these new rules?")
    cnt = 0
    for string in data:
        
        # test 1: two letter string repeating non overlapping
        ok1 = False
        ok2 = False
        for i,ch in enumerate(string):
            
            if not ok1 and i > 0:
                pair = string[i-1:i+1]
            
                if pair in string[i+1:]:
                    ok1 = True
                    
            if not ok2 and i > 1:
                if string[i-2] == string[i]:
                    ok2 = True
            
            if ok1 and ok2:
                cnt += 1
                break
        
        
        
        
        
        
        
    print(cnt)
    
