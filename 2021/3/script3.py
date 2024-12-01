from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

def commonBits(data, isMost, ifEqual = 0):
    return [
        (1 if isMost else 0) if 2 * cnt > len(data) else 
        ifEqual if 2 * cnt == len(data) 
        else (0 if isMost else 1)
        for cnt in reduce(lambda l1, l2 : [b1 + b2 for (b1, b2) in zip(l1, l2)], data)
    ]

def bitsToDec(bits):
    return reduce((lambda acc,b : acc * 2 + b), bits, 0)

with open(FILE_NAME) as file:
    data = [[int(b) for b in line if b != "\n"] for line in file]
    
    numLen = len(data[0])
    
    gammaBits = commonBits(data, isMost=True)
    
    gamma = bitsToDec(gammaBits)
    
    epsilonBits = [1-b for b in gammaBits]
    epsilon = bitsToDec(epsilonBits)
    
    print("Part One: What is the power consumption of the submarine?")
    print(gamma * epsilon)

    oxy = [[b for b in l] for l in data]
    co2 = [[b for b in l] for l in data]
    
    oxyDone = False
    co2Done = False
    bitPos = 0
    while True:
        
        
        if not oxyDone:
            oxyBit = 1 if (2 * len([1 for b in oxy if b[bitPos] == 1]) >= len(oxy)) else 0
            oxy = [l for l in oxy if l[bitPos] == oxyBit]
            if len(oxy) == 1:
                oxyDone = True
                oxy = oxy[0]
            
        if not co2Done:
            co2Bit = 1 if (2 * len([1 for b in co2 if b[bitPos] == 1]) < len(co2)) else 0
            #print(f"bitPos {bitPos}:")
            #print(f"-> co2Bit {co2Bit}")
            #print("  " + "\n  ".join(["".join(str(b) for b in l) for l in co2]))
            co2 = [l for l in co2 if l[bitPos] == co2Bit]
            if len(co2) == 1:
                co2Done = True
                co2 = co2[0]
        
        bitPos = (bitPos + 1) % numLen
        
        
        if oxyDone and co2Done:
            break
    
    oxy = bitsToDec(oxy)
    co2 = bitsToDec(co2)
    
    print()
    print("Part Two: What is the life support rating of the submarine?")
    print(oxy * co2)
    
    
    
    
    
    
    
