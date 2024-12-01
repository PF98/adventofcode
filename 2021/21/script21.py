from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"


BOARD_SIZE = 10
WINNING_SCORE1 = 1000

WINNING_SCORE2 = 21

class DeterministicDice:
    def __init__(self, size):
        self.size = size
        self.cnt = 0
        self.totalThrows = 0
    
    def get(self, throws):
        self.totalThrows += throws
        #out = [None] * throws
        out = 0
        for i in range(throws):
            if self.cnt >= self.size:
                self.cnt = 0
            self.cnt += 1
            #out[i] = self.cnt
            out += self.cnt
            
        return out



DIRAC3 = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]

cache = {}
def diracStep(pos, scores, turn, winningScore):
    key = (*pos, *scores, turn)
    if key in cache:
        return cache[key]
    
    
    winnerCnt = [0] * len(pos)
    
    for dice, amount in DIRAC3:
        npos = (pos[turn] + dice) % BOARD_SIZE
        nscore = scores[turn] + (npos + 1)
        
        if nscore >= winningScore:
            winnerCnt[turn] += amount
        else:
            recPos = [*pos]
            recPos[turn] = npos
            recScores = [*scores]
            recScores[turn] = nscore
            
            newWinnerCnt = diracStep(recPos, recScores, 1-turn, winningScore)
            
            newWinnerCnt = [amount * e for e in newWinnerCnt]
            
            winnerCnt = [a+b for a,b in zip(winnerCnt, newWinnerCnt)]
    
    cache[key] = winnerCnt
    
    return winnerCnt



def diracGame(pos, win):
    return diracStep(pos, [0] * len(pos), 0, win)



with open(FILE_NAME) as file:
    
    
    players = [int(line.strip().split(": ")[1])-1 for line in file]
    #print(players)
    
    
    positions = [*players]
    scores = [0] * len(players)
    
    
    d100 = DeterministicDice(100)

    loserPoints = None
    totalThrows = None
    while True:
        for p in range(len(players)):
            dice = d100.get(3)
            positions[p] += dice % BOARD_SIZE
            positions[p] %= BOARD_SIZE
            
            scores[p] += (positions[p]+1)
            
            #print(f"Player {p+1} rolls {dice} and moves to space {positions[p]+1} for a total score of {scores[p]}.")
            
            
            if scores[p] >= WINNING_SCORE1:
                loserPoints = scores[1 - p]
                totalThrows = d100.totalThrows
                break
            
        if loserPoints is not None:
            break
                
    
    
    
    print("Part One: Play a practice game using the deterministic 100-sided die. The moment either player wins, what do you get if you multiply the score of the losing player by the number of times the die was rolled during the game?")
    print(loserPoints * totalThrows)
    
    
    out = diracGame(players, WINNING_SCORE2)
    
    
    print()
    print("Part Two: Using your given starting positions, determine every possible outcome. Find the player that wins in more universes; in how many universes does that player win?")
    print(max(out))
