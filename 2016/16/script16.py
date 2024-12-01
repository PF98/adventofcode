from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"


LENGTH = 20
LENGTH = 272
LENGTH = 35651584

with open(FILE_NAME) as file:
    data = file.readline().strip()

while len(data) < LENGTH:
    data += "0" + "".join("1" if d == "0" else "0" for d in reversed(data))
data = data[:LENGTH]

print("data")

checksum = None
while checksum == None or len(checksum) % 2 == 0:
    if checksum is None:
        checksum = data
        
    checksum = "".join("1" if c1 == c2 else "0" for c1,c2 in zip(checksum[::2], checksum[1::2]))
    
print(checksum);

    

#print("Part One: What is the first time you can press the button to get a capsule?")
#print(calcDiscs(data))


#print()
#print("Part Two: With this new disc, and counting again starting from time=0 with the configuration in your puzzle input, what is the first time you can press the button to get another capsule?")
#print(calcDiscs(data))

# 23:26
# 23:27
