from functools import reduce

FILE_NAME = "example"
FILE_NAME = "input"


class Board:
    def __init__(self, numbersData):
        self.numbers = reduce(lambda a, b : a + b, [[int(n) for n in line.split(" ") if len(n) > 0] for line in numbersData])
        self.size = len(numbersData)
        self.complete = False
        self.checkCount = {
            "h": [0] * len(numbersData),
            "v": [0] * len(numbersData),
        }
        
    def __str__(self):
        return f"{str(self.checkCount)} - {str(self.numbers)}"
    
    def completed(self):
        return self.complete
    
    def mark(self, number):
        found = -1
        for index, num in enumerate(self.numbers):
            if num == number:
                found = index
                break
        
        if found == -1:
            return False
        
        self.numbers[found] = -1
        row = (index // self.size)
        col = index - self.size * row
        self.checkCount["h"][row] += 1
        self.checkCount["v"][col] += 1
        
        #print(f"  |-> trovato in {row},{col}")
        
        completed_h = (self.checkCount["h"][row] == self.size)
        completed_v = (self.checkCount["v"][col] == self.size)
        
        self.complete = completed_h or completed_v
        
        return sum(n for n in self.numbers if n >= 0) if (self.complete) else False


BINGO_SIZE = 5

with open(FILE_NAME) as file:
    data = [line for line in file]
    
    draws = [int(num) for num in data[0].split(",")]
    data = data[1:]
    
            
            
    
    
    boards = [Board(chunk[1:]) for chunk in [data[i:i+BINGO_SIZE+1] for i in range(0, len(data), BINGO_SIZE+1)]]
    
    #print(boards[0].checkCount)
    
    firstFound = False
    lastFound = False
    
    for num in draws:
        #print(f"drawn: {num}")
        for board in boards:
            if board.completed():
                #print(f"  DONE! {str(board)}")
                continue
            
            afterMark = board.mark(num)
            #print(f"  GOING {str(board)}")
            
            if afterMark is not False:
                if lastFound is False:
                    firstFound = afterMark * num
                    
                lastFound = afterMark * num
        
    print("Part One: What will your final score be if you choose that board?")
    print(firstFound)
    
    print()
    print("Part Two: Once it wins, what would its final score be?")
    print(lastFound)
    
    
    
    
    
