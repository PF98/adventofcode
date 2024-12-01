FILE_NAME = "example_1"
FILE_NAME = "example_2"
FILE_NAME = "input"


from collections import defaultdict
import itertools

modules = {}
memories = {}

inputs = defaultdict(list)
with open(FILE_NAME) as file:
    for line in file:
        line = line.strip()
        
        module,dests = line.split(" -> ")
        dests = tuple(dests.split(", "))
        
        if module[0] == "%" or module[0] == "&":
            typ = module[0]
            name = module[1:]
            modules[name] = (typ, dests)
            # flip flop: initially off
            if typ == "%":
                memories[name] = False
        # broadcaster
        else:
            name = module
            modules[name] = (name, dests)
            
        for dest in dests:
            inputs[dest].append(name)
    

for module,inps in inputs.items():
    if module not in modules or modules[module][0] != "&":
        continue
    
    memories[module] = {k: False for k in inps}




lows = 0
highs = 0

for _ in range(1000):
    # start with a low pulse to the broadcaster, from the button
    pulses = [("broadcaster", False, "button")]

    while pulses:
        newPulses = []
        
        for module,level,source in pulses:
            if level:
                highs += 1
            else:
                lows += 1
            
            if module not in modules:
                continue
            
            typ,dests = modules[module]
            # broadcaster: relay the same pulse, no memory required
            if typ == "broadcaster":
                newPulses.extend((dest, level, module) for dest in dests)
            # flip flop: only flip its exit if it receives a low pulse
            elif typ == "%":
                if level == False:
                    stored = memories[module]
                    memories[module] = not stored
                    newPulses.extend((dest, not stored, module) for dest in dests)
            # conjunction module: only sends a low pulse if all memories from its 
            # inputs are high, otherwise it sends a high pulse
            else: # typ == "&"
                memories[module][source] = level
                # all the inputs are high -> sends low
                newLevel = not all(memories[module].values())
                newPulses.extend((dest, newLevel, module) for dest in dests)
                    
        pulses = newPulses
    
    
    
    
    

print("Part One:")
print(lows * highs)



# basic structure for my input: rx only has lg as an input
active = inputs["rx"][0]
# lg is a conjunction module with 4 inputs (vg, nb, vc, ls)
actives = inputs[active]
# each of those conjunction modules has each one input:
actives = [inputs[a][0] for a in actives]
# each of those is a counter, whose period i'm going to calculate here


# the counter gets to the end, switching the output of one of the "actives" 
# when all of the bits in "determiner" are set.
# feedback is used to reset all of the other bits, effectively restarting the 
# counter and keeping the period in a correct status

out = 1
for module in actives:
    loopers = set()

    toCheck = set(inputs[module])
    
    while toCheck:
        e = toCheck.pop()
        loopers.add(e)
        
        for b in inputs[e]:
            if b != "broadcaster" and b != module and b not in loopers:
                toCheck.add(b)
    
    nodes = []
    feedback = []
    determiner = []
    
    node = "broadcaster"
    depth = 0
    
    while node != module:
        nextnode = None
        for nxt in modules[node][1]:
            if nxt in loopers:
                nextnode = nxt
                break
        if nextnode is None:
            break
        #print(nextnode)
            
        nodes.append(nextnode)
        if module in inputs[nextnode]:
            feedback.append(depth)
        if module in modules[nextnode][1]:
            determiner.append(depth)
            
        node = nextnode
        depth += 1
    
    number = int("".join(reversed(["1" if bit in determiner else "0" for bit in range(len(nodes))])), 2)
    out *= number

print()
print("Part Two:")
print(out)
