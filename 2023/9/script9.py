FILE_NAME = "example"
FILE_NAME = "input"


with open(FILE_NAME) as file:
    lst = [tuple(int(bi) for bi in line.strip().split(" ")) for line in file]


tl = 0
tf = 0
for diff in lst:
    diffs = [diff]
    while any(d != 0 for d in diffs[-1]):
        diffs.append(tuple(b-a for a,b in zip(diffs[-1], diffs[-1][1:])))
    
    fe = 0
    le = 0
    for diff in reversed(diffs):
        le += diff[-1]
        fe = diff[0] - fe
    
    tl += le
    tf += fe

print("Part One:")
print(tl)

print()
print("Part Two:")
print(tf)
