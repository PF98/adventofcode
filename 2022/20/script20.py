FILE_NAME = "example"
FILE_NAME = "input"

from dataclasses import dataclass

#@dataclass
class Node:
    #num: int
    def __init__(self, num):
        self.num = num
        self.prv = None
        self.nxt = None
        
    def __str__(self):
        return str(self.num)
        return f"({self.prv.num} <- {self.num} -> {self.nxt.num})"
    def __repr__(self):
        return str(self)

def extractPositions(nodes, positions, zeropos):
    n = nodes[zeropos]
    
    mod = len(nodes)
    
    positions = list(p % mod for p in positions)
    
    founds = [None] * len(positions)
    for i in range(mod):
        if i in positions:
            founds[positions.index(i)] = n.num
        
        n = n.nxt
        if all(f is not None for f in founds):
            break
        
    return founds

def printlst(start):
    n = start
    lst = []
    while True:
        lst.append(n)
        n = n.nxt
        if n == start:
            break

    print(lst)
    
with open(FILE_NAME) as file:
    nodes = [Node(int(line.strip())) for line in file]
    
    zeropos = None
    
    for i,node in enumerate(nodes):
        node.prv = nodes[i - 1]
        node.nxt = nodes[(i + 1) % len(nodes)]
        
        if node.num == 0:
            zeropos = i
    
    #nodes[0].num = -7
    
    #printlst(nodes[0])
    
    for node in nodes:
        #print(f"Node{node}")

        # remove "node": set node.nxt as the successor of node.prv
        # and node.prv as the predecessor of node.nxt
        node.prv.nxt = node.nxt
        node.nxt.prv = node.prv
        
        #print("temporary: ", end="")
        #printlst(node.nxt)
        #print(node.nxt.prv.nxt)
        
        # move right "node.num" times
        nextnode = node.prv
        for _ in range(node.num % (len(nodes) - 1)):
            nextnode = nextnode.nxt
        
        # "node" must be placed right of "nextnode"
        # node has nextnode.nxt to its right
        # and nextnode to its left
        node.nxt = nextnode.nxt
        node.prv = nextnode
        
        nextnode.nxt.prv = node
        nextnode.nxt = node
        #printlst(nodes[0])
        #input()
    #printlst(nodes[0])
    
    ep = extractPositions(nodes, [1000*(i+1) for i in range(3)], zeropos)
    
    print("Part One: Mix your encrypted file exactly once. What is the sum of the three numbers that form the grove coordinates?")
    print(sum(ep))
    
    
    #exit()

    
    mod = len(nodes) - 1
    # reset the list
    for i,node in enumerate(nodes):
        node.prv = nodes[i - 1]
        node.nxt = nodes[(i + 1) % len(nodes)]
        
                            
        node.num *= 811589153
        
        node.modnum = node.num % mod
        
    #print("Initial arrangement:")
    #printlst(nodes[0])
    #print()
    
    # mixing
    for r in range(10):
        print(f"{r:2d}/10", end="\r")
        for node in nodes:

            # remove "node": set node.nxt as the successor of node.prv
            # and node.prv as the predecessor of node.nxt
            node.prv.nxt = node.nxt
            node.nxt.prv = node.prv
            
            # move right "node.num" times
            nextnode = node.prv
            #for _ in range(node.num):
            for _ in range(node.modnum):
                nextnode = nextnode.nxt
            
            # "node" must be placed right of "nextnode"
            # node has nextnode.nxt to its right
            # and nextnode to its left
            node.nxt = nextnode.nxt
            node.prv = nextnode
            
            nextnode.nxt.prv = node
            nextnode.nxt = node
            
        #print(f"After {r+1} round{'s' if r > 0 else ''} of mixing:")
        #printlst(nodes[zeropos])
        #input()
        
    
    ep = extractPositions(nodes, [1000*(i+1) for i in range(3)], zeropos)
    print(" "*10)
    
    print("Part Two: Apply the decryption key and mix your encrypted file ten times. What is the sum of the three numbers that form the grove coordinates?")
    print(sum(ep))
