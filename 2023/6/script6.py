FILE_NAME = "example"
FILE_NAME = "input"

import math

with open(FILE_NAME) as file:
    times,dists = ([int(n) for n in line.strip().split(":")[1].split(" ") if n.strip()] for line in file)


tot = 1

# total distance: c*(t - c) = ct - c^2
# valids: tc - c^2 > d
#         c^2 - tc + d < 0
# delta = t^2 - 4d
# solutions: c1,2 = (t +- sqrt(t^2 - 4d)) / 2
# therefore (t - sqrt(t^2 - 4d)) / 2 < c < (t + sqrt(t^2 - 4d)) / 2
for t,d in zip(times,dists):
    sqdelta = math.sqrt(t**2 - 4*d)
    start = int((t - sqdelta) / 2) + 1
    end = math.ceil((t + sqdelta) / 2) - 1
    
    tot *= (end - start + 1)
    
    

print("Part One:")
print(tot)

t = int("".join(str(v) for v in times))
d = int("".join(str(v) for v in dists))
sqdelta = math.sqrt(t**2 - 4*d)
start = int((t - sqdelta) / 2) + 1
end = math.ceil((t + sqdelta) / 2) - 1

print()
print("Part Two:")
print(end - start + 1)
