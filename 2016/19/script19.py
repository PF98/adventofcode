from functools import reduce
import re
import math


FILE_NAME = "example"
FILE_NAME = "input"


with open(FILE_NAME) as file:
    length = int(file.readline())

#length = 243


lst = list(range(0, length, 2))
rest = (length % 2)
while len(lst) > 1:
    newRest = ((len(lst)-rest) % 2)
    lst = lst[rest::2]
    rest = newRest
    #print(rest)
    #print(lst)
    
print("Part One: With the number of Elves given in your puzzle input, which Elf gets all the presents?")
print(lst[0]+1)

#for length in range(2, 3**5+2):
    #lst = list(range(length))
    #turn = 0
    #ins = length
    ##print(lst)
    #while len(lst) > 1:
        ##print(len(lst), end="\r")
        
        #toRemove = (turn + len(lst) // 2);
        #if toRemove >= len(lst):
            #toRemove -= len(lst)
        #else:
            #turn += 1
            
        #lst.pop(toRemove)
        #turn = turn % len(lst)
        
        ##print()
        ##print(f"{turn} ({lst[turn]})")
        ##print(lst)
    ##print()
    ##print("Part Two: With this new disc, and counting again starting from time=0 with the configuration in your puzzle input, what is the first time you can press the button to get another capsule?")
    ##print(lst[0]+1)
    
    #print(f"{length: 4} => {lst[0] + 1}")
    
    #n = math.ceil(math.log(length, 3))
    #k = length - 3**(n-1)
    #if 2 * k > length:
        #k += max(0, 2*k - length)
    #print(f"     => {k}: ", end="")
    #print("!!!!!!!!!!" if k != (lst[0] + 1) else "")
    
    
    
    
# empirical observations for part 2:
# for l <= 3^n:
# 3^(n-1)+1: 1
# 3^(n-1)+2: 2
# 3^(n-1)+3: 3
# ....
# 3^(n-1)+k: k
# ...
# 3^(n-1)

n = math.ceil(math.log(length, 3))
k = length - 3**(n-1)
#if 2 * k > length:
k += max(0, 2*k - length)
    
print()
print("Part Two: With the number of Elves given in your puzzle input, which Elf now gets all the presents?")
print(k)
