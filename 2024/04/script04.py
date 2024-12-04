FILE_NAME = "example"
FILE_NAME = "input"


WORD = "XMAS"

DIRECTIONS = [(dx,dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx,dy) != (0,0)]

with open(FILE_NAME) as file:
    field = [line.strip() for line in file]

H = len(field)
W = len(field[0])

tot = 0
for r in range(H):
    for c in range(W):
        for dx in (-1, 0, 1):
            if dx < 0 and c+1 < len(WORD):
                continue
            if dx > 0 and c > W - len(WORD):
                continue
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                if dy < 0 and r+1 < len(WORD):
                    continue
                if dy > 0 and r > H - len(WORD):
                    continue

                if all(field[r + i*dy][c + i*dx] == l for i,l in enumerate(WORD)):
                    tot += 1

print("Part One:")
print(tot)

tot = 0
for r,row in enumerate(field[1:-1], start=1):
    for c,cell in enumerate(row[1:-1], start=1):
        if cell != "A":
            continue

        for dx,dy in [(-1,-1),(-1,1)]:
            if sorted(field[r + i*dy][c + i*dx] for i in (-1,1)) != ["M","S"]:
                break
        else:
            tot += 1

print()
print("Part Two")
print(tot)
