FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    lines = [line.strip().split("|") for line in file if line.strip()]

rules = {}
updates = []
for line in lines:
    # rule
    if len(line) == 2:
        f,t = (int(v) for v in line)
        if f not in rules:
            rules[f] = set()
        rules[f].add(t)
    else:
        updates.append([int(v) for v in line[0].split(",")])

def reorder(u, rules):
    # select the first element which contains all of the others in its rule
    for e in u:
        if e not in rules:
            continue

        if all(v in rules[e] for v in u if v != e):
            return [e, *reorder([v for v in u if v != e], rules)]

    return u

tot = 0
tot2 = 0
for update in updates:
    for i1,l1 in enumerate(update):
        for l2 in update[i1+1:]:
            if l1 not in rules or l2 not in rules[l1]:
                break
        else:
            continue
        break
    else:
        tot += update[len(update)//2]
        continue

    # incorrectly ordered
    new_update = reorder(update, rules)
    tot2 += new_update[len(update)//2]

print("Part One:")
print(tot)

print()
print("Part Two:")
print(tot2)
