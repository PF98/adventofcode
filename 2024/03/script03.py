FILE_NAME = "example1"
FILE_NAME = "example2"
FILE_NAME = "input"

import re
import math

with open(FILE_NAME) as file:
    memory = "".join(line.strip() for line in file)

regex = re.compile(r"mul\((\d\d?\d?),(\d\d?\d?)\)")

print("Part One:")
print(sum(math.prod(int(e) for e in m) for m in regex.findall(memory)))

regex = re.compile(r"(mul\((\d\d?\d?),(\d\d?\d?)\)|do(?:n't)?\(\))")

active = True
tot = 0
for instr,*args in regex.findall(memory):
    if instr.startswith("don't"):
        active = False
    elif instr.startswith("do"):
        active = True
        continue

    if not active:
        continue

    tot += math.prod(int(e) for e in args)

print()
print("Part Two")
print(tot)
