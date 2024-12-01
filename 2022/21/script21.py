FILE_NAME = "example"
FILE_NAME = "input"

from dataclasses import dataclass

OPERATION = {
    "+": lambda a,b: a+b,
    "-": lambda a,b: a-b,
    "*": lambda a,b: a*b,
    "/": lambda a,b: a//b
}

# idea: dict(operation -> dict(ordinal child missing -> lambda))
REVERSE_OPERATION = {
    "+": (lambda res,ab: res-ab,)*2,
    "-": (
        lambda res,b: res+b,
        lambda res,a: a-res,
    ),
    "*": (lambda res,ab: res//ab,)*2,
    "/": (
        lambda res,b: res*b,
        lambda res,a: a//res,
    ),
}


@dataclass
class TreeNode:
    def __init__(self):
        self.parent = None

@dataclass
class TreeLeaf(TreeNode):
    num: int
    def __init__(self, num):
        self.num = num
        
@dataclass
class TreeBranch(TreeNode):
    operation: str
    def __init__(self, children, operation):
        self.children = children
        self.operation = operation
        
    def simplify(self):
        if all(isinstance(c, TreeLeaf) for c in self.children):
            a,b = self.children
            return TreeLeaf(OPERATION[self.operation](a.num, b.num))
        
        return self
    
    def climbBack(self, value):
        tb,tl = self.children
        
        branchpos = 0
        
        if isinstance(tb, TreeLeaf):
            tb,tl = tl,tb
            branchpos = 1
            
        operLambda = REVERSE_OPERATION[self.operation][branchpos]
        newValue = operLambda(value, tl.num)
        
        return tb.climbBack(newValue)
    
@dataclass
class TreeHuman(TreeNode):
    def __init__(self):
        pass
    
    def climbBack(self, value):
        return value

class Monkeys:
    def __init__(self, monkeys):
        self.monkeys = monkeys
        
    def getValue(self, name):
        m = self.monkeys[name]
        
        match m.split():
            case [ma, oper, mb]:
                return OPERATION[oper](self.getValue(ma), self.getValue(mb))
            
            case [num]:
                return int(num)
            
    def calculateTrees(self, name, human):
        m = self.monkeys[name].split()
        children = m[0::2]
        
        r1,r2 = (self.buildTree(child, human) for child in children)
        
        if isinstance(r1, TreeLeaf):
            r1,r2 = r2,r1
        
        # always returns TreeBranch, TreeLeaf
        return r1,r2
            
    def buildTree(self, name, human):
        if name == human:
            return TreeHuman()
        
        m = self.monkeys[name]
        match m.split():
            case [ma, oper, mb]:
                a = self.buildTree(ma, human)
                b = self.buildTree(mb, human)
                
                tb = TreeBranch((a,b), oper)
                tn = tb.simplify()
                
                a.parent = tn
                b.parent = tn
                
                return tn
            
            case [num]:
                return TreeLeaf(int(num))

with open(FILE_NAME) as file:
    monkeys = Monkeys(dict(line.strip().split(": ") for line in file))
    
    
    result = monkeys.getValue("root")
    
    print("Part One: However, your actual situation involves considerably more monkeys. What number will the monkey named root yell?")
    print(result)
    
    
    humanbranch, tl = monkeys.calculateTrees("root", "humn")
    
    
    
    print()
    print("Part Two: What number do you yell to pass root's equality test?")
    print(humanbranch.climbBack(tl.num))
