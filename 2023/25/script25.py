FILE_NAME = "example"
FILE_NAME = "input"


import math
import networkx as nx

DRAW = True
DRAW = False

if DRAW:
    import networkx as nx
    import matplotlib.pyplot as plt
    
class Node:
    def __init__(self, name, dest = None):
        self.name = name
        self.dest = set() if dest is None else set(dest)
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f"Node({self.name}, {self.dest})"

nodes = {}
with open(FILE_NAME) as file:
    for line in file:
        line = line.strip()
        
        node,dests = line.split(": ")
        dests = dests.split(" ")
        
        if node not in nodes:
            nodes[node] = Node(node, dests)
        else:
            nodes[node].dest.update(dests)
            
        for dest in dests:
            if dest not in nodes:
                nodes[dest] = Node(dest)
            nodes[dest].dest.add(node)
        
def showGraph(nodes):
    if not DRAW:
        return
    
    G = nx.Graph()
    
    nodeList = list(n.name for n in nodes.values())
    
    nodeNumbers = {nodes[n].name: i for i,n in enumerate(nodeList)}
    
    G.add_nodes_from(range(len(nodes)))
    for node in nodes:
        for dest in nodes[node].dest:
            if dest > node:
                continue
            
            G.add_edge(nodeNumbers[node], nodeNumbers[dest])
    
    pos = nx.spring_layout(G)
    
    nx.draw(G, pos=pos, labels = {i: n for i,n in enumerate(nodeList)}, font_color="w", font_weight="bold", font_size=8)
    plt.show()



#def contract(nodes):
    #nodeList = {n.name: i for n in enumerate(nodes.values())}
    #dist = [0] * len(nodes)
    #vis = [False] * len(nodes)
    
    #n = 
    
    #for i in range(1, 

#def stoerWagner(nodes):
    
    
    #bestCut = None
    #bestVec = None
    
    
G = nx.Graph()

nodeList = list(n.name for n in nodes.values())
nodeNumbers = {nodes[n].name: i for i,n in enumerate(nodeList)}

G.add_nodes_from(range(len(nodes)))
for node in nodes:
    for dest in nodes[node].dest:
        if dest > node:
            continue
        
        G.add_edge(nodeNumbers[node], nodeNumbers[dest])

#nx.draw(G, labels = {i: n for i,n in enumerate(nodeList)}, font_color="w", font_weight="bold", font_size=8)
#plt.show()

cut_value, partition = nx.stoer_wagner(G)
#print(f"{cut_value = }")
#print(f"{partition = }")

print("Part One:")
print(math.prod(map(len, partition)))
exit()




#TO_REMOVE = [("fmr", "zhg"), ("jct", "rgv"), ("crg", "krf")] if FILE_NAME == "input" else [("hfx", "pzl"), ("jqt", "nvd"), ("bvb", "cmg")]


#for f,t in TO_REMOVE:
    #nodes[f].dest.remove(t)
    #nodes[t].dest.remove(f)


showGraph(nodes)

groupings = {k: None for k in nodes}
group = 0
groupCounts = {}
# flood
while any(g is None for g in groupings.values()):
    tovisit = {next(k for k,g in groupings.items() if g is None)}
    groupCounts[group] = 0
    
    while tovisit:
        node = tovisit.pop()
        groupings[node] = group
        
        groupCounts[group] += 1
        
        for dest in nodes[node].dest:
            if groupings[dest] is None:
                tovisit.add(dest)
        
    group += 1
        

print("Part One:")
print(math.prod(groupCounts.values()))
