FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    lst = [tuple([int(n) for n in e.strip().split()] for e in line.strip().split(":")[1].split("|")) for line in file]

t = 0
for winners,card in lst:
    cnt = sum(1 for c in card if c in winners)
    
    t += 2**(cnt - 1) if cnt > 0 else 0


print("Part One:")
print(t)

amounts = {k:1 for k,_ in enumerate(lst, start=1)}

for i,(winners,card) in enumerate(lst, start=1):
    cnt = sum(1 for c in card if c in winners)

    for j in range(i + 1, i + cnt + 1):
        amounts[j] += amounts[i]
    

print()
print("Part Two:")
print(sum(amounts.values()))
