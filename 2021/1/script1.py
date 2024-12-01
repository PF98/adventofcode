FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    numbers = [int(line) for line in file];
    print("Part One: How many measurements are larger than the previous measurement?")
    print(len([1 for (current, prev) in zip(numbers[1:], numbers[:-1]) if current > prev]))
    
    print()
    print("Part Two: How many sums are larger than the previous sum?")
    print(len([1 for (current, prev3) in zip(numbers[3:], numbers[:-3]) if current > prev3]))
