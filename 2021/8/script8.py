from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"


LIGHTS = [
#    a  b  c  d  e  f  g
    [1, 1, 1, 0, 1, 1, 1], # 0
    [0, 0, 1, 0, 0, 1, 0], # 1
    [1, 0, 1, 1, 1, 0, 1], # 2
    [1, 0, 1, 1, 0, 1, 1], # 3
    [0, 1, 1, 1, 0, 1, 0], # 4
    [1, 1, 0, 1, 0, 1, 1], # 5
    [1, 1, 0, 1, 1, 1, 1], # 6
    [1, 0, 1, 0, 0, 1, 0], # 7
    [1, 1, 1, 1, 1, 1, 1], # 8
    [1, 1, 1, 1, 0, 1, 1]  # 9
]

LENGTHS = [sum(num) for num in LIGHTS]




# be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe

CHARS = [chr(ord("a") + i) for i in range(7)]

with open(FILE_NAME) as file:
    lines = [line[:-1] for line in file]
    
    count1478 = 0 # they use 2, 4, 3 and 7 segments respectively
    
    countsum = 0
    
    for line in lines:
        left, right = [s.split(" ") for s in line.split(" | ")]
        ljoin = "".join(left)
        left_orig = [l for l in left]
        
        count1478 += sum(1 for word in right if len(word) in [2,4,3,7])
        
        occurrences = [sum(1 for c in "".join(left) if c == ch) for ch in CHARS]
    
        options = [[i for i,l in enumerate(LENGTHS) if l == len(word)] for word in left]
        segments = [[ch for ch in CHARS if occurrences[ord(ch) - ord("a")] == sum(bit)] for bit in zip(*LIGHTS)]
        
        
        for i,opt in enumerate(options):
            if len(opt) == 1:
                #print(f"  Confirmed index {i}: value {opt[0]} for word {left[i]}")
                num = opt[0]
                word = left[i]
                
                bits = [i for i,b in enumerate(LIGHTS[num]) if b > 0]
                #print(f"    bits: {bits}")
                for bit in bits:
                    segments[bit] = [s for s in segments[bit] if s in word]
        
        toremove = [slist[0] for slist in segments if len(slist) == 1]
        segments = [[s for s in slist if (s not in toremove or len(slist) == 1)] for slist in segments]

        
        for i,o in enumerate(options):
            o[:] = [num for num in o if all((segments[j][0] in left[i]) for j,s in enumerate(LIGHTS[num]) if s == 1)]        
            
        #print("\nThen: ")
        #print(f"options: {options}")
        #print(f"segments: {segments}")
        #print(f"occurrences: {occurrences}")
        
        result_map = {"".join(sorted(left[i])):o[0] for i,o in enumerate(options)}
        
        countsum += reduce(lambda a,b : 10*a + b, [result_map["".join(sorted(word))] for word in right], 0)
        
    
    print("Part One: In the output values, how many times do digits 1, 4, 7, or 8 appear?")
    print(count1478)
    
    print()
    print("Part Two: What do you get if you add up all of the output values?")
    print(countsum)
    

    
    
