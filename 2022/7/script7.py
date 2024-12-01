FILE_NAME = "example"
FILE_NAME = "input"

import re

from itertools import groupby

DISKSIZE =   70000000
NEEDEDSIZE = 30000000




INDENT = 2

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = int(size)
        
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return f"- {self.name} (file, size={self.size})"

class Folder:
    def __init__(self, name, parent = None):
        self.name = name
        self.subfolders = {}
        self.files = []
        
        self.parent = parent
        
        self.totalSize = 0
        
        self.addOrder = {}
        self.cnt = 0
        
    def addSubFolder(self, name):
        self.subfolders[name] = Folder(name, self)
        self.cnt += 1
        self.addOrder[name] = self.cnt

    def addFile(self, name, size):
        self.files.append(File(name, size))
        self.cnt += 1
        self.addOrder[name] = self.cnt
        
        p = self
        while p is not None:
            p.totalSize += int(size)
            p = p.parent
    
    def getSize(self):
        return self.totalSize
        #return sum(sf.getSize() for sf in self.subfolders.values()) + sum(f.size for f in self.files)
    
    def sumSizeIf(self, condition):
        return (self.totalSize if condition(self.totalSize) else 0) + sum(sf.sumSizeIf(condition) for sf in self.subfolders.values()) 
        
    def smallest(self, minSize):
        if self.totalSize < minSize:
            return None
        
        #print(f"smallest {self.name}: size = {self.totalSize} ({minSize})")
        minFolders = [sf.smallest(minSize) for sf in self.subfolders.values()]
        #print(f"{minFolders=}")
        
        minFolders = list(s for s in minFolders if s is not None)
        
        minFolder = min(minFolders) if len(minFolders) > 0 else None
        #print(f"{minFolder=}")
        return minFolder if minFolder is not None else (self.totalSize if self.totalSize >= minSize else None)
    
    def __str__(self):
        return repr(self)
    
    
    def __repr__(self):
        me = f"- {self.name} (dir, size={self.getSize()}) + parent = {self.parent.name if self.parent is not None else None}"
        
        allNames = sorted([*((self.addOrder[f.name], f, "file") for f in self.files), *((self.addOrder[sf.name], sf, "sf") for _,sf in self.subfolders.items())])
        
        
        strs = []
        for name, obj, typ in allNames:
            match typ:
                case "file":
                    strs.append(f"{INDENT * ' '}{obj}")
                case "sf":
                    strs.append((INDENT * ' ') + f"\n{INDENT * ' '}".join(repr(obj).split("\n")))
        
                
        return "\n".join([me, *strs])

class FileSystem:
    def __init__(self):
        self.fs = Folder("/")
        self.currentFolder = []
    
    def runCommand(self, cmd, lines):
        match cmd.split():
            case ["cd", folder]:
                self.changeDirectory(folder)
            case ["ls"]:
                self.listDirectory(lines)
                    
    def changeDirectory(self, folder):
        match folder:
            case "/":
                self.currentFolder = []
            case "..":
                del self.currentFolder[-1]
            case _:
                self.currentFolder.append(folder)

    def listDirectory(self, lines):
        cf = self.getFolder(self.currentFolder)
        for line in lines:
            
            match line.split():
                case ["dir", folder]:
                    cf.addSubFolder(folder)
                case [size, name]:
                    cf.addFile(name, size)
        
    
    def getFolder(self, path):
        f = self.fs
        for p in path:
            f = f.subfolders[p]
        return f
    
    
    def sumDirectories(self, condition):
        return self.fs.sumSizeIf(condition)
    
    def getSmallestFolder(self, minSize):
        return self.fs.smallest(minSize)
    
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return repr(self.fs)
        



with open(FILE_NAME) as file:
    
    splitCmds = []
    for line in file:
        line = line.strip()
        
        match line.split():
            case ["$", *cmd]:
                splitCmds.append([" ".join(cmd)])
            case _:
                splitCmds[-1].append(line)
                
    
    #print(splitCmds)
    
    currentFolder = [];
    
    fs = FileSystem()
    
    for cmd,*sublines in splitCmds:
        # cd
        fs.runCommand(cmd, sublines)
            
        #print(args)
    
    
    print("Part One: Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?")
    print(fs.sumDirectories(lambda s: s <= 100000))
    
    #print(f"total used: {fs.fs.totalSize}")
    #print(f"   un-used: {DISKSIZE - fs.fs.totalSize}")
    #print(f" to delete: {NEEDEDSIZE - (DISKSIZE - fs.fs.totalSize)}")
    
    folder = fs.getSmallestFolder(NEEDEDSIZE - (DISKSIZE - fs.fs.totalSize))
    
    print()
    print("Part Two: Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?")
    print(folder)
