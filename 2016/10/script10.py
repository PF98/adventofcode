from functools import reduce
import re

FILE_NAME = "example"
FILE_NAME = "input"

COMPARED = [2, 5]
COMPARED = [17, 61]





MATCH1 = "value (\d+) goes to bot (\d+)"

BOT_OR_OUTPUT = "(bot|output) (\d+)"
MATCH2 = f"bot (\d+) gives low to {BOT_OR_OUTPUT} and high to {BOT_OR_OUTPUT}"


class Contents(dict):
    def __getitem__(self, key):
        if key not in self:
            self[key] = []
        
        return super().__getitem__(key)

class Status:
    def __init__(self):
        self.bots = {}


with open(FILE_NAME) as file:
    initialValues = [] # list of tuple(val, bot)
    givesTo = {} # map of fromBot => tuple(tuple(lowToBot, lowNum), tuple(highToBot, highNum))
    
    for line in file:
        m1 = re.match(MATCH1, line)
        if m1 is not None:
            initialValues.append(tuple(int(m1.group(n+1)) for n in range(2)))
            continue
        
        
        m2 = re.match(MATCH2, line)
        if m2 is not None:
            fr, lowNum, highNum = (int(m2.group(n+1)) for n in range(0, 5, 2)) # 0, 2, 4
            lowToBot, highToBot = (m2.group(n+1) == "bot" for n in range(1, 4, 2)) # 1, 3
            
            if fr in givesTo:
                print(fr)
                print("NO")
                exit()
            givesTo[fr] = ((lowToBot, lowNum), (highToBot, highNum))
    
    
#print(initialValues)
#print(givesTo)


contents = Contents()
twoNumbers = set()

for val, bot in initialValues:
    #print(val)
    #print(bot)
    contents[bot].append(val)
    if len(contents[bot]) == 2:
        twoNumbers.add(bot)


outputs = {}

out1 = None
while twoNumbers:
    newTwoNumbers = set()
    for fr in twoNumbers:
        if all(n in contents[fr] for n in COMPARED):
            #print(f"found: comparing values is bot {fr}")
            out1 = fr
        for i, ((toBot, num), val) in enumerate(zip(givesTo[fr], sorted(contents[fr]))):
            if not toBot:
                outputs[num] = val
            else:
                contents[num].append(val)
                if len(contents[num]) == 2:
                    newTwoNumbers.add(num)
                    
        del contents[fr]
    
    twoNumbers = newTwoNumbers



#print(outputs)





print("Part One: Based on your instructions, what is the number of the bot that is responsible for comparing value-61 microchips with value-17 microchips?")
print(out1)



print()
print("Part Two: What do you get if you multiply together the values of one chip in each of outputs 0, 1, and 2?")
print(reduce(lambda a,b: a*b, (outputs[n] for n in range(3))))
print(outputs[0])
print(outputs[1])
print(outputs[2])
print(outputs)
