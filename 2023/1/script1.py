lFILE_NAME = "example1" # vaild for part one
FILE_NAME = "input"

with open(FILE_NAME) as file:
    lst = [[l for l in line.strip() if "0" <= l <= "9"] for line in file]
    
print("Part One:")
print(sum(int(numbers[0] + numbers[-1]) for numbers in lst))


#FILE_NAME = "example2" # valid for part two
#FILE_NAME = "input"

with open(FILE_NAME) as file:
    lst = [line.strip() for line in file]

NUMBERS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

t = 0
for line in lst:
    numbers = [(pos, int(l)) for pos,l in enumerate(line.strip()) if "0" <= l <= "9"]

    minindl = None
    minposl = None
    maxindr = None
    maxposr = None
    for ind,num in enumerate(NUMBERS):
        posl = line.find(num)
        posr = line.rfind(num)
        if posl >= 0 and (minposl is None or posl < minposl):
            minposl = posl
            minindl = ind
        if posr >= 0 and (maxposr is None or posr > maxposr):
            maxposr = posr
            maxindr = ind
    
    if numbers and (minposl is None or numbers[0][0] < minposl):
        minindl = numbers[0][1]
    if numbers and (maxposr is None or numbers[-1][0] > maxposr):
        maxindr = numbers[-1][1]
    
    t += 10*minindl + maxindr
        

print()
print("Part Two:")
print(t)
