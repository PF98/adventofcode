from functools import reduce
import re
import math
import random

FILE_NAME = "example"
FILE_NAME = "input"


# IDEA FOR PART 2 STOLEN FROM https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/cy4kpms/?utm_source=reddit&utm_medium=web2x&context=3 BECAUSE IT WAS DUMB


class TreeNode:
    def __init__(self):
        self.values = []
        self.children = {}

    def add(self, to, fr):
        #print(f"adding '{to}', '{fr}'")
        if len(to) == 0:
            self.values.append(fr)
            return
        
        if to[0] not in self.children:
            self.children[to[0]] = TreeNode()
        
        self.children[to[0]].add(to[1:], fr)
        
    def get(self, to):
        if len(to) == 0:
            return self.values
        
        return self.children[to[0]].get(to[1:])
    
    def match(self, mol, depth = 0):
        #print(f"calling match with mol = {mol}, depth = {depth}")
        matches = []
        
        if len(self.values) > 0:
            matches.append((depth, self.values))
            
        if depth < len(mol) and mol[depth] in self.children:
            matches += self.children[mol[depth]].match(mol, depth+1)
            
        return matches
    
    def stringa(self, depth = None):
        
        out = ('|   ' if depth is None else '') + f"TreeNode with values = {self.values}, children = {[ch for ch in self.children]}, containing:\n"
        nd = (depth+1) if depth is not None else 2
        rec = ""
        for n in self.children:
            rec += f"{'|   ' * (nd)}[{n}] " + self.children[n].stringa(nd)
        out += rec
        return out
            

class BackRepl:
    def __init__(self):
        self.tree = TreeNode()
        
    def add(self, to, fr):
        self.tree.add(to, fr)
        
    def get(self, to):
        self.tree.get(to)
        
    def matches(self, mol, start):
        return self.tree.match(mol, start)
        
    def __str__(self):
        return "BackRepl containing:\n" + self.tree.stringa()




cache = {}

def goBackTo(mol, backRepl, to, depth = 0):
    #print(f"{'¦   ' * depth}calling goBackTo on {mol} to get to {to}")
    if mol in cache:
        return cache[mol]
    
    if mol == to:
        #print(f"{'¦   ' * depth} <- returning {0}")
        cache[mol] = 0
        return 0
    
    
    minSteps = None
    for i,ch in enumerate(mol):
        matches = backRepl.matches(mol, i)
        #print(f"{'¦   ' * depth}-> matches for i = {i} (mol[i:] = {mol[i:]}) => {matches}")
        
        for matchEnd, toList in reversed(matches):
            for toOption in toList:
                if toOption == "e" and (i > 0 or matchEnd < len(mol)):
                    #print(f"{'¦   ' * depth}EEEEE: {i},{matchEnd}")
                    continue
                    
                newMol = mol[:i] + toOption + mol[matchEnd:]
                steps = goBackTo(newMol, backRepl, to, depth+1)
                if steps is not None and (minSteps is None or steps < minSteps):
                    minSteps = steps
        pass
    
    
    out = minSteps+1 if minSteps is not None else minSteps
    #print(f"{'¦   ' * depth} <- returning {out}")
    cache[mol] = out
    return out

def linearBack(mol, backRepl, to):
    
    cnt = 0
    while True:
        maxLen = None
        match = None
        for i in range(len(mol),0,-1):
            i = i-1
            ch = mol[i]
            matches = backRepl.matches(mol, i)
            if len(matches) == 0:
                continue
            matchEnd, toList = matches[-1]
            leng = matchEnd - i
            
            if maxLen is None or leng < maxLen:
                maxLen = leng
                match = (i, matchEnd, toList)
        
        
        if maxLen is None:
            break
        
        i, matchEnd, toList = match
        mol = mol[:i] + toList[0] + mol[matchEnd:]
        cnt += 1
    return cnt,mol


def randomBack(molecule, repl, end):
    cnt = 0
    shuf = 0
    mol = molecule
    while len(mol) > 1:
        start = mol
        for fr, toList in repl.items():
            for to in toList:
                while to in mol:
                    cnt += mol.count(to)
                    mol = mol.replace(to, fr)
                
        if start == mol:
            l = list(repl.items())
            
            for f,t in l:
                random.shuffle(t)
                
            random.shuffle(l)
            repl = dict(l)
            cnt = 0
            mol = molecule
            shuf += 1
            
    
    return shuf, cnt, mol

with open(FILE_NAME) as file:
    data = [line.strip() for line in file]
    
    repls = [l.split(" => ") for l in data[:-2]]
    molecule = data[-1]
    
    backRepl = BackRepl()
    
    revRepl = {}
    
    replDict = {}
    for fr,to in repls:
        if fr not in replDict:
            replDict[fr] = []
        if to not in revRepl:
            revRepl[to] = []
            
        revRepl[to].append(fr)
        replDict[fr].append(to)
        
        
        backRepl.add(to, fr)
            
    #print(list(k for k in replDict))
    #print(molecule)
    
    allMolecules = set()
    for i,ch in enumerate(molecule):
        for k in replDict:
            if molecule.startswith(k, i):
                for m in replDict[k]:
                    allMolecules.add(molecule[:i] + m + molecule[i+len(k):])
    
    print("Part One: How many distinct molecules can be created?")
    print(len(allMolecules))
    
    
    
    #print(backRepl)
    #for i in range(len(molecule)):
        #print(f"{i}: {backRepl.matches(molecule, i)}")
    #exit()
    #amount = goBackTo(molecule, backRepl, "e")
    #amount = linearBack(molecule, backRepl, "e")
    shuf, cnt, mol = randomBack(molecule, replDict, "e")
    
    
    print()
    print("Part Two: In your grid of 100x100 lights, given your initial configuration, but with the four corners always in the on state, how many lights are on after 100 steps?")
    #print(shuf)
    print(cnt)
    #print(mol)
