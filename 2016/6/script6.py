from functools import reduce
from collections import Counter
import hashlib

FILE_NAME = "example"
FILE_NAME = "input"



with open(FILE_NAME) as file:
    data = [line.strip() for line in file]

size = len(data[0])

out = ""
out2 = ""

for i in range(size):
    string = [d[i] for d in data]
    counter = Counter(string)
    
    (letter, _),*_,(letterLeast,_) = counter.most_common()
    
    out += letter
    out2 += letterLeast


print("Part One: Given the recording in your puzzle input, what is the error-corrected version of the message being sent?")
print(out)



print()
print("Part Two: Given the recording in your puzzle input and this new decoding methodology, what is the original message that Santa is trying to send?")
print(out2)
