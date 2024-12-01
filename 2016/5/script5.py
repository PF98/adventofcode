from functools import reduce
import hashlib

FILE_NAME = "example"
FILE_NAME = "input"


REPEATS = 8


with open(FILE_NAME) as file:
    doorID = file.readline().strip()

done2 = False
out2 = [None] * REPEATS
out = ""
str0to9 = "".join(str(i) for i in range(10))
i = 0
while True:
    string = f"{doorID}{i}"
    res = hashlib.md5(string.encode()).hexdigest()
    
    if res.startswith("0" * 5):
        char = res[5]
        print(i)
        print(res)
        print(f"out : {out}")
        print(f"out2: {out2}")
        print()
        if len(out) < REPEATS:
            out += char
        
        if not done2 and char in str0to9 and 0 <= int(char) < REPEATS and out2[int(char)] is None:
            pos = int(char)
            char = res[6]
            out2[pos] = char
            
            done2 = all(e is not None for e in out2)
            
        
        if len(out) == REPEATS and done2:
            break
    
    i += 1


print("Part One: Given the actual Door ID, what is the password?")
print(out)



print()
print("Part Two: Given the actual Door ID and this new method, what is the password?")
print("".join(out2))
