from functools import reduce
import re
import math


FILE_NAME = "example1"
FILE_NAME = "example2"
FILE_NAME = "example3"
FILE_NAME = "example4"
FILE_NAME = "example5"
FILE_NAME = "example6"
FILE_NAME = "example7"
FILE_NAME = "input"


def bitsToDec(bits):
    return reduce(lambda acc, b : acc * 2 + b, bits, 0)


VERSION_LENGTH = 3
TYPE_ID_LENGTH = 3

LITERAL_BLOCK_LENGTH = 5


LTID0_LENGTH = 15
LTID1_LENGTH = 11

class Packet:
    LITERAL = 4
    OPERATORS = {
        # SUM
        0: lambda subpackets : sum(sp.value() for sp in subpackets),
        # PRODUCT
        1: lambda subpackets : reduce(lambda a,b : a*b, (sp.value() for sp in subpackets), 1),
        # MINIMUM
        2: lambda subpackets : min(sp.value() for sp in subpackets),
        # MAXIMUM
        3: lambda subpackets : max(sp.value() for sp in subpackets),
        # LITERAL
        4: lambda content : content,
        # GREATER THAN
        5: lambda subpackets : 1 if subpackets[0].value() > subpackets[1].value() else 0,
        # LESS THAN
        6: lambda subpackets : 1 if subpackets[0].value() < subpackets[1].value() else 0,
        # EQUAL TO
        7: lambda subpackets : 1 if subpackets[0].value() == subpackets[1].value() else 0,
    }
    STRINGS = {
        # SUM
        0: lambda subpackets : f"({' + '.join(sp.expr() for sp in subpackets)})",
        # PRODUCT
        1: lambda subpackets : f"({' * '.join(sp.expr() for sp in subpackets)})",
        # MINIMUM
        2: lambda subpackets : f"min([{', '.join(sp.expr() for sp in subpackets)}])",
        # MAXIMUM
        3: lambda subpackets : f"max([{', '.join(sp.expr() for sp in subpackets)}])",
        # LITERAL
        4: lambda content : str(content),
        # GREATER THAN
        5: lambda subpackets : f"({' > '.join(sp.expr() for sp in subpackets)})",
        # LESS THAN
        6: lambda subpackets : f"({' < '.join(sp.expr() for sp in subpackets)})",
        # EQUAL TO
        7: lambda subpackets : f"({' == '.join(sp.expr() for sp in subpackets)})",
    }
    NAMES = {
        0: "sum",
        1: "product",
        2: "minimum",
        3: "maximum",
        4: "literal",
        5: "greater than",
        6: "less than",
        7: "equal to"
    }
    
    def __init__(self, version, typeID, content):
        self.version = version
        self.typeID = typeID
        self.content = content
    
    def __str__(self):
        return f"Packet object: {{version = {self.version}, typeID = {self.typeID} (\"{self.NAMES[self.typeID]}\"), content = {str(self.content) if self.typeID == self.LITERAL else f'[{len(self.content)} packets]'}}}"


    def sumVersionNumbers(self):
        if self.typeID == self.LITERAL:
            return self.version
        else:
            return self.version + sum(sp.sumVersionNumbers() for sp in self.content)

    def value(self):
        return self.OPERATORS[self.typeID](self.content)
    
    
    def expr(self):
        return self.STRINGS[self.typeID](self.content)



    
    

# returns Packet, length
def parsePacket(bits):
    i = 0
    version = bitsToDec(bits[i:i+VERSION_LENGTH]) # first 3 bits: version
    i += VERSION_LENGTH
    
    typeID = bitsToDec(bits[i:i+TYPE_ID_LENGTH]) # next 3 bits: type ID
    i += TYPE_ID_LENGTH
    
    # LITERAL type
    if typeID == Packet.LITERAL:
        numBits = []
        while True:
            startBit = bits[i]
            group = bits[i+1 : i+LITERAL_BLOCK_LENGTH]
            
            numBits += group
            
            i += LITERAL_BLOCK_LENGTH
            
            if startBit == 0:
                break
        num = bitsToDec(numBits)
        #print(f"packet type ID {typeID}, content \"{num}\"")
        
        
        return Packet(version, typeID, num), i
        
    # OPERATORS:
    else:
        # every operator contains a length type id
        lentypeID = bits[i]
        i += 1
        
        subpackets = []
        
        if lentypeID == 0:
            # length of the subpackets: keep parsing until reached
            subpLen = bitsToDec(bits[i : i+LTID0_LENGTH])
            i += LTID0_LENGTH
            
            
            totalLen = 0
            while totalLen < subpLen:
                packet,length = parsePacket(bits[i:])
                
                i += length
                
                totalLen += length
                subpackets.append(packet)
                
        elif lentypeID == 1:
            # number of subpackets: keep parsing until reached
            subpCnt = bitsToDec(bits[i : i+LTID1_LENGTH])
            i += LTID1_LENGTH
            
            subpackets = []
            
            totalCnt = 0
            while totalCnt < subpCnt:
                packet,length = parsePacket(bits[i:])
                
                i += length
                
                totalCnt += 1
                subpackets.append(packet)
            
        return Packet(version, typeID, subpackets), i

with open(FILE_NAME) as file:
    
    msg = file.readline().strip()
    bits = reduce(lambda acc, e : (acc + [int(b) for b in e]), (f"{int(n, 16):04b}" for n in msg), [])
    
    packet,length = parsePacket(bits)
    
    #print(f"msg : {msg}")
    
    #print(f"bits: {''.join(str(i) for i in bits)}")
    #print(packet)
    #print(length)
    
    
    
    
    
    print("Part One: what do you get if you add up the version numbers in all packets?")
    print(packet.sumVersionNumbers())
    #print(packet)
    
    
    print()
    print("Part Two: What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission?")
    print(packet.value())
    
    #print(packet.expr())
    #print(int(eval(packet.expr())))
    
