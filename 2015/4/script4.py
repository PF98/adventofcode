from functools import reduce
import hashlib

FILE_NAME = "example"
FILE_NAME = "input"


with open(FILE_NAME) as file:
    
    data = file.readline().strip()
    n = 0
    out5 = None
    out6 = None
    while True:
        res = hashlib.md5(f"{data}{n}".encode()).hexdigest()
        if out5 is None and res.startswith("0" * 5):
            out5 = n
        if res.startswith("0" * 6):
            out6 = n
            break
        
        n += 1
    
    print("Part One: Find the first number that produces a hash that begins with five zeroes")
    print(out5)
    
    print()
    print("Part Two: Now find one that starts with six zeroes.")
    print(out6)
    
