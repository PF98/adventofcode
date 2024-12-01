FILE_NAME = "example"
FILE_NAME = "input"

from enum import Enum, auto
from itertools import groupby
from functools import reduce
import math

class MonkeyOperation(Enum):
    PRODUCT = auto()
    SUM = auto()
    
    def __call__(self, a, b, old):
        (a,b) = (e.getValue(old) for e in (a,b))
        match self:
            case self.PRODUCT:
                return a * b
            case self.SUM:
                return a + b
            

MONKEY_OPERATION_MAP = {
    "+": MonkeyOperation.SUM,
    "*": MonkeyOperation.PRODUCT,
}


class MonkeyOperationParameter:
    def __init__(self):
        pass
    
    def get(param):
        match param:
            case "old":
                return MOP_old()
            case num:
                return MOP_number(int(num))
    
    def getValue(self, old):
        pass
    
class MOP_number(MonkeyOperationParameter):
    def __init__(self, num):
        self.num = num
    
    def getValue(self, old):
        return self.num
    
class MOP_old(MonkeyOperationParameter):
    def __init__(self):
        pass
    
    def getValue(self, old):
        return old
    

class Monkey:
    number : int
    startingItems : list[int]
    items : list[int]
    operationType : MonkeyOperation
    operationParameters : list[MonkeyOperationParameter]
    testDiv : int
    testRes : dict[bool, int]
    
    mod : int
    
    inspects : int
    
    def __init__(self):
        self.inspects = 0
        self.testRes = {}
    
    def setItems(self, lst):
        self.items = lst
        self.startingItems = lst.copy()
    
    def calcOperation(self, old):
        return self.operationType(*self.operationParameters, old) % self.mod
        
    def throwObject(self, worry, monkeys):
        monkeys[self.testRes[worry % self.testDiv == 0]].items.append(worry)
        self.inspects += 1
        
    def reset(self):
        self.inspects = 0
        self.items = self.startingItems.copy()
        
    def __str__(self):
        return f"Monkey {self.number} ({self.inspects:3d}): {', '.join(str(n) for n in self.items)}"


ROUNDS = 20
ROUNDS2 = 10000

with open(FILE_NAME) as file:
    lst = [line.strip() for line in file]
    
    chunks = list(list(g) for k,g in groupby(lst, key=lambda x: len(x) > 0) if k)
    
    monkeys = []
    for monkeylst in chunks:
        m = Monkey()
        for line in monkeylst:
            match line.split():
                case ["Monkey", num]:
                    m.number = int(num[:-1])
                case ["Starting", "items:", *items]:
                    m.setItems([int(i) for i in "".join(items).split(",")])
                case ["Operation:", "new", "=", m1, oper, m2]:
                    m.operationType = MONKEY_OPERATION_MAP[oper]
                    m.operationParameters = [MonkeyOperationParameter.get(term) for term in [m1, m2]]
                case ["Test:", "divisible", "by", num]:
                    m.testDiv = int(num)
                case ["If", boolean, "throw", "to", "monkey", num]:
                    b = (boolean[:-1] == "true")
                    
                    m.testRes[b] = int(num)
        
        monkeys.append(m)
    
    mod = math.lcm(*(m.testDiv for m in monkeys))
    for m in monkeys:
        m.mod = mod
    
    #print(f"At the beginning, the monkeys are holding items with these worry levels:")
    #print("\n".join(str(m) for m in monkeys))
    #print()
    
    
    for i in range(ROUNDS):
        for m in monkeys:
            items = m.items
            m.items = []
            for item in items:
                worry = m.calcOperation(item)
                worry //= 3
                m.throwObject(worry, monkeys)
        
        #print(f"After round {i+1}, the monkeys are holding items with these worry levels:")
        #print("\n".join(str(m) for m in monkeys))
        #print()
    
    
    print("Part One: What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?")
    print(reduce(lambda a,b: a*b, sorted(m.inspects for m in monkeys)[-2:]))

    
    for m in monkeys:
        m.reset()
    
    for i in range(ROUNDS2):
        for m in monkeys:
            items = m.items
            m.items = []
            for item in items:
                worry = m.calcOperation(item)
                m.throwObject(worry, monkeys)
            
            #print(f"  {m.number} done! (len = {len(items)})")
            
        if i+1 in [1,20] or (i+1) % 1000 == 0:
            print(f"== After round {i+1} ==")
            print("\n".join(f"Monkey {m.number} ispected items {m.inspects} times. (len = {len(m.items)})" for m in monkeys))
            print()
        
    
    print()
    print("Part Two: Starting again from the initial state in your puzzle input, what is the level of monkey business after 10000 rounds?")
    print(reduce(lambda a,b: a*b, sorted(m.inspects for m in monkeys)[-2:]))
