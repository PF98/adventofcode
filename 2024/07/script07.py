FILE_NAME = "example"
FILE_NAME = "input"

# tuples of: reverse operation, check
OPERATORS = [
    # multiplication
    (
        lambda res, t: res // t,
        lambda res, t: res % t == 0
    ),
    # sum
    (
        lambda res, t: res - t,
        lambda res, t: True
    ),
]

with open(FILE_NAME) as file:
    lines = [(int(tot), *(int(v) for v in lst.split())) for tot,lst in (line.strip().split(": ") for line in file)]



def check_operators(res, terms, i = -1):
    t = terms[i]
    
    if -i == len(terms):
        return res == t
    
    for rev_op, check in OPERATORS:
        if not check(res, t):
            continue
        
        if check_operators(rev_op(res, t), terms, i - 1):
            return True
    
    return False



print("Part One:")
print(sum(res for res,*terms in lines if check_operators(res, terms)))

# add the concatenation operator "||", as a (reverse operation, check)
OPERATORS.append((
    lambda res, t: int(str(res)[:-len(str(t))]), # reverse operation
    lambda res, t: str(res).endswith(str(t)), # check
))


print()
print("Part Two:")
print(sum(res for res,*terms in lines if check_operators(res, terms)))
