from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"

CORRUPT_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

CHAR_MATCHES = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}


AUTOCOMPLETE_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}


with open(FILE_NAME) as file:
    corruptScore = 0
    autocompleteScores = []
    for data in file:
        
        stack = []
        corrupted = False
        for i,ch in enumerate(data[:-1]):
            if ch in CHAR_MATCHES:
                stack.append(ch)
                continue
            
            if len(stack) == 0 or CHAR_MATCHES[stack.pop()] != ch:
                corruptScore += CORRUPT_POINTS[ch]
                corrupted = True
                break
        
        if not corrupted:
            autocompleteScores.append(reduce(lambda acc,ch : 5*acc + AUTOCOMPLETE_POINTS[CHAR_MATCHES[ch]], stack[::-1], 0))
        
    
    autocompleteScores.sort()
    
    print("Part One: What is the total syntax error score for those errors?")
    print(corruptScore)
    
    print()
    print("Part Two: What is the middle score?")
    print(autocompleteScores[len(autocompleteScores) // 2])
    

    
    
