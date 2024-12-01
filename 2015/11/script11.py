from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"


FORBIDDEN = [ord(c) for c in "iol"]
START = ord("a")
END = ord("z")

def increase(pwd):
    pwd = [ord(c) for c in pwd]
    old = [*pwd]
    for i,ch in enumerate(old):
        if ch in FORBIDDEN:
            while ch in FORBIDDEN:
                ch = ch + 1
                if ch > END:
                    ch = START
            pwd = old[:i] + [ch] + [START] * (len(pwd) - i - 1)
            break
    
    
    old = [*pwd]
    start = True
    while start or not isOk(pwd):
        start = False
        #print(f"Testing {''.join(chr(c) for c in pwd)}")
        s = True
        i = len(pwd) - 1
        while s or pwd[i] in FORBIDDEN:
            pwd[i] += 1
            s = False
            if pwd[i] > END:
                pwd[i] = START
                i -= 1
                s = True
    
    return "".join(chr(c) for c in pwd)
        


def isOk(pwd):
    if any(ch in FORBIDDEN for ch in pwd):
        return False
    
    ok1 = False
    ok2 = 0
    lastPair = -1
    for i in range(1,len(pwd)):
        if not ok1 and i > 1 and pwd[i-2]+1 == pwd[i-1] and pwd[i-1]+1 == pwd[i]:
            ok1 = True
            
        if ok2 < 2 and pwd[i-1] == pwd[i] and lastPair < i-1:
            #print(f"lastPair: {lastPair}, i: {i}, '{''.join(chr(c) for c in pwd[i-1:i+1])}'")
            ok2 += 1
            lastPair = i
            
        if ok1 and ok2 >= 2:
            return True
    
    return False

with open(FILE_NAME) as file:
    data = file.readline().strip()
    
    #data = "hijklmmn"
    
    #data = "abbceffg"
    #data = "abbcegjk"
    #data = "abcdefgh"
    #data = "abcdffaa"
    #data = "ghijklmn"
    np = increase(data)
    print(np)
    print(increase(np))
    #data = "ghjaabcc"
    #print(data)
        
    
    
    #print("Part One: Given Santa's current password (your puzzle input), what should his next password be?")
    #print(out1)
    
    
    
        
    #print()
    #print("Part Two: Now, starting again with the digits in your puzzle input, apply this process 50 times. What is the length of the new result?")
    #print(a)
    
