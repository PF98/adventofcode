from functools import reduce

FILE_NAME = "example1"
FILE_NAME = "example2"
FILE_NAME = "example3"
FILE_NAME = "input"


START_NODE = "start"
END_NODE = "end"



def countPaths(nodes, links, selected, endnode, depth, visited = []):
    #indent = '│   ' * (depth)
    #arrowout =  "└─> "
    #arrowin = "<── "
    
    #print(f"{indent}{arrowout}call on \"{selected}\" with visited = [{','.join(visited)}]")
    
    if selected == endnode:
        #print(f"{indent}{arrowin}return: {1}, [{selected}]")
        return 1,[[selected]]
    
    newVisited = [*visited]
    if not selected.isupper():
        newVisited.append(selected)
        
    # check all paths
    allpaths = []
    count = 0
    for node in links[selected]:
        # skip visited nodes
        if node in visited:
            continue
                
        newcount,newpaths = countPaths(nodes, links, node, endnode, depth + 1, newVisited)
        
        count += newcount
        allpaths += newpaths
        
    allpaths = [[selected, *p] for p in allpaths]
        
    #print(f"{indent}{arrowin}return: {count}, ", end="")
    #print(allpaths)
    return count,allpaths



def countPaths2(nodes, links, selected, startnode, endnode, depth, visited = {}):
    #indent = '│   ' * (depth)
    #arrowout =  "└─> "
    #arrowin = "<── "
    
    #print(f"{indent}{arrowout}call on \"{selected}\" with visited = ", end="")
    #print(visited)
    
    # this is the recursion end point, which also stops the end node from being visited twice
    if selected == endnode:
        #print(f"{indent}{arrowin}return: {1}, [{selected}]")
        return 1
        #return 1,[[selected]]
    
    newVisited = {k: visited[k] for k in visited}
    if not selected.isupper():
        if not selected in newVisited:
            newVisited[selected] = 0
            
        newVisited[selected] += 1
        
    # check all paths
    #allpaths = []
    count = 0
    
    smallNodeTwice = any(newVisited[v] == 2 for v in newVisited)
    
    for node in links[selected]:
        # skip visited nodes if a small node has already been visited twice
        
        # if the node has already been visited at least once and any node has been visited twice: continue
        if node in visited and smallNodeTwice:
            continue
        
        # startnode is the only node that can't be visited twice
        if node == startnode:
            continue

        newcount = countPaths2(nodes, links, node, startnode, endnode, depth + 1, newVisited)
        #newcount,newpaths = countPaths2(nodes, links, node, startnode, endnode, depth + 1, newVisited)
        
        count += newcount
        #allpaths += newpaths
        
    #allpaths = [[selected, *p] for p in allpaths]
        
    #print(f"{indent}{arrowin}return: {count}, ", end="")
    #print(allpaths)
    return count
    #return count,allpaths



nodes = []
links = {}

with open(FILE_NAME) as file:
    
    for line in file:
        fr,to = line[:-1].split("-")
        
        if not fr in links:
            links[fr] = []
        if not to in links:
            links[to] = []
            
        links[fr].append(to)
        links[to].append(fr)
        
        
    count,allpaths = countPaths(nodes, links, START_NODE, END_NODE, 0)
    count2 = countPaths2(nodes, links, START_NODE, START_NODE, END_NODE, 0)
    #count2,allpaths2 = countPaths2(nodes, links, START_NODE, START_NODE, END_NODE, 0)
    
    #print(count2)
    #print("\n".join(",".join(str(n) for n in p) for p in allpaths2))
    
    print("Part One: How many paths through this cave system are there that visit small caves at most once?")
    print(count)
    
    print()
    print("Part Two: how many paths through this cave system are there?")
    print(count2)
    

    
    
