from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"

def f(N):
    l = (N//4+1) # trial and error
    sums = [1] * l
    maxVal = 1
    for n in range(2, l):
        for i in range(n, l, n):
            sums[i-1] += n

        if sums[n-1] >= N:
            #print(sums)
            return n
        
def f2(N):
    l = (N//40+1) # trial and error
    sums = [1] * l
    maxVal = 1
    for n in range(2, l):
        for i in range(n, min(n*50, l)+1, n):
            sums[i-1] += n * 11

        if sums[n-1] >= N:
            #print(sums)
            return n
    
with open(FILE_NAME) as file:
    N0 = int(file.readline())
    N = N0 // 10
    
    #N = 14
            
            
    print("Part One: What is the lowest house number of the house to get at least as many presents as the number in your puzzle input?")
    print(f(N))
    
    print()
    print("Part Two: With these changes, what is the new lowest house number of the house to get at least as many presents as the number in your puzzle input?")
    print(f2(N0))
