from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

DIRECTIONS = {
    "^": lambda c : (c[0], c[1] - 1),
    "v": lambda c : (c[0], c[1] + 1),
    ">": lambda c : (c[0] + 1, c[1]),
    "<": lambda c : (c[0] - 1, c[1])
}

with open(FILE_NAME) as file:
    
    data = file.readline().strip()
    
    print("Part One: How many houses receive at least one present?")
    print(
        len(
            set(
                reduce(
                    lambda acc, ch : (DIRECTIONS[ch](acc[0]), [*acc[1], DIRECTIONS[ch](acc[0])]),
                    data,
                    ((0,0), [(0,0)])
                )[1]
            )
        )
    )
    
    print()
    print("Part Two: How many houses receive at least one present?")
    print(
        len(
            set(
                list(
                    reduce(
                        lambda acc, ch : (DIRECTIONS[ch](acc[0]), [*acc[1], DIRECTIONS[ch](acc[0])]),
                        data[::2],
                        ((0,0), [(0,0)])
                    )[1]
                )
                +
                list(
                    reduce(
                        lambda acc, ch : (DIRECTIONS[ch](acc[0]), [*acc[1], DIRECTIONS[ch](acc[0])]),
                        data[1::2],
                        ((0,0), [(0,0)])
                    )[1]
                )
            )
        )
    )
