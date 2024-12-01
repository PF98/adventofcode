from enum import Enum


class E(Enum):
    A = 1
    B = 2
    C = 3
    
    _ignore_ = ["_lst"]
    
    _lst = None
    
    def get(key):
        if E._lst is None:
            E._lst = list(Enum)
            
        return E._lst[key]
    
    def __getitem__(key):
        return list(E)[key]
    
    
a = E.A


print(list(E))

print(E.get(0))
print(E.get(1))
print(E.get(2))
print(E.get(4))
